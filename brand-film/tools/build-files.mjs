#!/usr/bin/env node
/**
 * Mabkhra Haill — brand film file builder.
 *
 *   node tools/build-files.mjs [--fps=25|30|both] [--workshop] [--gate-b=cleared]
 *                              [--gate-c] [--out=generated]
 *
 * Reads tools/film-data.mjs and writes the frame-exact deliverable set into
 * generated/: EDL (CSV + readable), caption timing, VO budget, SRTs, QA report.
 * Exits non-zero if any QA check fails, so it can be wired into CI later.
 *
 * Timeline model
 * `film-data.mjs` holds the client's nominal 2:22 grid. Two optional inserts sit
 * on that grid (the workshop beat at 102.5 s, the Gate C Amazon/Noon card at
 * 111.5 s). Everything after an insert shifts by its length; elements that live
 * *inside* an insert declare `inInsert` and do not shift by their own insert.
 */

import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { FILM, ASSETS, SCENES, GATES, LINKS, DELIVERABLES } from './film-data.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '..');

/* ---------------------------------------------------------------- args */

const args = process.argv.slice(2);
const arg = (name, fallback = null) => {
  const hit = args.find((a) => a === `--${name}` || a.startsWith(`--${name}=`));
  if (!hit) return fallback;
  const [, value] = hit.split('=');
  return value === undefined ? true : value;
};

const OPTIONS = {
  fps: arg('fps', 'both'),
  workshop: Boolean(arg('workshop', false)),
  gateB: arg('gate-b', 'default'),
  gateC: Boolean(arg('gate-c', false)),
  out: resolve(root, String(arg('out', 'generated'))),
};

const FADE_FRAMES = 8;              // 8 f = 0.32 s at 25 fps
const MIN_CAPTION_SECONDS = 2.0;
const MIN_URL_CAPTION_SECONDS = 2.8;
const MIN_HOLD_SECONDS = 0.25;
const MIN_SHOT_SECONDS = 2.0;
const PRODUCT_MIN_SECONDS = 2.2;
const VO_TAIL_SECONDS = 0.4;

const problems = [];
const warnings = [];
const notes = [];
const fail = (m) => problems.push(m);
const warn = (m) => warnings.push(m);
const note = (m) => notes.push(m);

/* ------------------------------------------------- insert / shift model */

const INSERTS = [
  { tag: 'workshop', start: 102.5, seconds: 2.5, enabled: OPTIONS.workshop },
  { tag: 'gate-c', start: 111.5, seconds: 4.4, enabled: OPTIONS.gateC },
].filter((i) => i.enabled);

/**
 * Shift applied to a nominal time.
 *   kind 'start' — the element begins after the insert, so an insert starting
 *                  exactly at t counts.
 *   kind 'end'   — the element ends where the insert begins, so only inserts
 *                  that start strictly before t count, unless this element is
 *                  the one that carries the insert (`contains`).
 * Insert-part elements (`ownInsert`) never shift by their own insert.
 */
const offset = (t, kind, ownInsertTag = null, containsTag = null) =>
  INSERTS.filter((i) => {
    if (ownInsertTag && i.tag === ownInsertTag) return false;
    if (kind === 'start') return i.start <= t;
    return i.start < t || containsTag === i.tag;
  }).reduce((sum, i) => sum + i.seconds, 0);

const ownInsert = (el) => el.inInsert ?? (el.optional === 'workshop' ? 'workshop' : null);
const shiftedStart = (el) => el.start + offset(el.start, 'start', ownInsert(el));
const shiftedEnd = (el, containsTag = null) => el.end + offset(el.end, 'end', ownInsert(el), containsTag);
/** The last shot of a scene is the one that carries that scene's optional insert. */
const containsFor = (scene, index) => (index === scene.shots.length - 1 ? scene.contains ?? null : null);
const sceneEnd = (scene) => shiftedEnd(scene.shots[scene.shots.length - 1], scene.contains ?? null);

/* --------------------------------------------------------- active set */

const gateActive = (el) => {
  const g = el.condition ?? el.conditional ?? el.optional ?? el.gate ?? null;
  if (!g) return true;
  if (g === 'gate-b-default') return OPTIONS.gateB !== 'cleared';
  if (g === 'gate-b-cleared') return OPTIONS.gateB === 'cleared';
  if (g === 'gate-c') return OPTIONS.gateC;
  if (g === 'workshop') return OPTIONS.workshop;
  if (g === 'gate-h') return true; // badge stays until real photography replaces the mock-up
  if (g === 'gate-i-linktree') return true; // V12d is an alt; the K3 Linktree line renders until Gate I clears
  return true;
};

const scenes = SCENES.map((scene) => ({
  ...scene,
  shots: scene.shots.filter(gateActive),
  captions: scene.captions.filter(gateActive),
  vo: scene.vo.filter(gateActive),
}));

const runtimeSeconds = FILM.masterSeconds + INSERTS.reduce((s, i) => s + i.seconds, 0);
const runtimeLimit = FILM.masterSeconds + FILM.runtimeToleranceSeconds;

/* ------------------------------------------------------ helpers / fmt */

const countWords = (s) => s.trim().split(/\s+/).filter(Boolean).length;
const pad = (n, w = 2) => String(n).padStart(w, '0');
const tc = (frames, fps) => {
  const f = frames % fps;
  const secs = Math.floor(frames / fps);
  return `${pad(Math.floor(secs / 3600))}:${pad(Math.floor((secs % 3600) / 60))}:${pad(secs % 60)}:${pad(f)}`;
};
const srtTime = (frames, fps) => {
  const ms = Math.round((frames / fps) * 1000);
  return `${pad(Math.floor(ms / 3600000))}:${pad(Math.floor((ms % 3600000) / 60000))}:${pad(Math.floor((ms % 60000) / 1000))},${pad(ms % 1000, 3)}`;
};
const fx = (s) => Number(s.toFixed(2));
const q = (s) => `"${String(s).replace(/"/g, "'").replace(/\n/g, ' / ')}"`;

/* ---------------------------------------------------- structure checks */

let cursor = 0;
for (const scene of scenes) {
  const start = shiftedStart(scene);
  if (fx(start) !== fx(cursor)) fail(`[structure] ${scene.id} starts at ${fx(start)} s but the previous scene ends at ${fx(cursor)} s`);
  if (fx(shiftedStart(scene.shots[0])) !== fx(start)) fail(`[structure] ${scene.id}: first shot starts at ${fx(shiftedStart(scene.shots[0]))} s, scene starts at ${fx(start)} s`);
  const sEnd = sceneEnd(scene);
  for (const [i, shot] of scene.shots.entries()) {
    const next = scene.shots[i + 1];
    const shotEnd = shiftedEnd(shot, containsFor(scene, i));
    const expectedEnd = next ? shiftedStart(next) : sEnd;
    if (fx(shotEnd) !== fx(expectedEnd)) fail(`[structure] ${scene.id}/${shot.id}: ends at ${fx(shotEnd)} s, expected ${fx(expectedEnd)} s (gap or overlap)`);
    const dur = shotEnd - shiftedStart(shot);
    const min = shot.minSeconds ?? (scene.id === 'S4' ? PRODUCT_MIN_SECONDS : MIN_SHOT_SECONDS);
    if (dur < min - 1e-9) fail(`[duration] ${scene.id}/${shot.id} = ${dur.toFixed(2)} s, below the ${min} s minimum`);
  }
  cursor = sEnd;
}
if (fx(cursor) !== fx(runtimeSeconds)) fail(`[structure] timeline ends at ${fx(cursor)} s but the runtime is ${fx(runtimeSeconds)} s`);
if (runtimeSeconds > runtimeLimit + 1e-9) {
  fail(`[runtime] ${runtimeSeconds.toFixed(1)} s exceeds the ${runtimeLimit.toFixed(1)} s ceiling (2:22 ±3 s)`);
} else if (runtimeSeconds > FILM.masterSeconds + 1e-9) {
  note(`[runtime] the enabled options add ${(runtimeSeconds - FILM.masterSeconds).toFixed(1)} s → ${runtimeSeconds.toFixed(1)} s; headroom left ${(runtimeLimit - runtimeSeconds).toFixed(1)} s`);
}

/* ------------------------------------------------------- caption checks */

const allCaptions = scenes.flatMap((s) => s.captions.map((c) => ({ ...c, scene: s.id, sceneRef: s })));
for (const c of allCaptions) {
  const s = shiftedStart(c);
  const e = shiftedEnd(c);
  const dur = e - s;
  const hasUrl = /\.com|\.sa|\.ee|@/.test(c.ar) || Boolean(c.secondLineLatin);
  const min = hasUrl && c.kind !== 'disclaimer-badge' ? MIN_URL_CAPTION_SECONDS : MIN_CAPTION_SECONDS;
  if (dur < min - 1e-9) fail(`[caption] ${c.id} (${c.scene}) = ${dur.toFixed(2)} s, below the ${min} s minimum${hasUrl ? ' (carries a URL/handle)' : ''}`);
  const fade = (FADE_FRAMES * 2) / c.sceneRef ? (FADE_FRAMES * 2) / 25 : 0;
  if (dur - fade < MIN_HOLD_SECONDS) fail(`[caption] ${c.id}: only ${(dur - fade).toFixed(2)} s of full-opacity hold after both 8-frame fades`);
  const sceneStart = shiftedStart(c.sceneRef);
  const sEnd = sceneEnd(c.sceneRef);
  if (s < sceneStart - 1e-9 || e > sEnd + 1e-9) fail(`[caption] ${c.id} runs outside its scene (${fx(s)}–${fx(e)} vs ${fx(sceneStart)}–${fx(sEnd)})`);
}
for (const [i, c] of allCaptions.entries()) {
  for (const d of allCaptions.slice(i + 1)) {
    if (c.scene !== d.scene) continue;
    if (c.start < d.end - 1e-9 && d.start < c.end - 1e-9) {
      const exclusiveGates = (c.condition || c.conditional) && (d.condition || d.conditional) && (c.condition ?? c.conditional) !== (d.condition ?? d.conditional);
      const badgeOverLabel = [c.kind, d.kind].some((k) => k === 'disclaimer-badge' || k === 'micro-label');
      if (!exclusiveGates && !badgeOverLabel) warn(`[caption] ${c.id} and ${d.id} overlap in ${c.scene} — confirm this is intentional`);
    }
  }
}

/* ---------------------------------------------------------- VO checks */

const voRows = [];
let voSeconds = 0;
for (const scene of scenes) {
  const lines = scene.vo.filter((v) => v.kind === 'primary');
  for (const [i, v] of lines.entries()) {
    const next = lines[i + 1];
    const windowEnd = next ? shiftedStart(next) : sceneEnd(scene);
    const window = windowEnd - shiftedStart(v) - VO_TAIL_SECONDS;
    const words = countWords(v.ar);
    const needed = words / FILM.arPaceWordsPerSecond;
    voSeconds += needed;
    if (needed > window) fail(`[vo] ${v.id} needs ${needed.toFixed(1)} s at ${FILM.arPaceWordsPerSecond} w/s but has ${window.toFixed(1)} s before the next cue`);
    else if (window - needed < 0.3) warn(`[vo] ${v.id} slack is only ${(window - needed).toFixed(2)} s — a slow read will collide with the next cue`);
    for (const mark of v.syncMarks ?? []) if (mark.target < v.start) fail(`[vo] ${v.id}: sync mark "${mark.word}" sits before the line's in-point`);
    voRows.push({ scene: scene.id, id: v.id, briefLine: v.briefLine, in: shiftedStart(v), words, needed, window, slack: window - needed, ar: v.ar });
  }
}
const voDensity = voSeconds / runtimeSeconds;
note(`[vo] primary narration ≈ ${voSeconds.toFixed(1)} s of speech = ${(voDensity * 100).toFixed(0)}% of a ${runtimeSeconds.toFixed(1)} s runtime`);
if (voDensity > 0.7) warn(`[vo] narration covers ${(voDensity * 100).toFixed(0)}% of runtime — weigh this against "silence between sections is desirable"`);

/* ------------------------------------------------------- asset checks */

const usedAssets = new Set(scenes.flatMap((s) => s.shots.flatMap((sh) => sh.asset.split('|').flatMap((a) => a.split('+')))));
const known = new Set(ASSETS.map((a) => a.id));
for (const a of usedAssets) if (!known.has(a)) fail(`[asset] a shot references unknown asset id ${a}`);
const blocking = ASSETS.filter((a) => a.status === 'required' && usedAssets.has(a.id));
note(`[asset] ${ASSETS.filter((a) => a.status === 'supplied').length} supplied · ${blocking.length} required and missing · ${ASSETS.length} ids in the manifest`);

/* ------------------------------------------------------------ writers */

mkdirSync(OPTIONS.out, { recursive: true });
const write = (name, body) => writeFileSync(join(OPTIONS.out, name), body.endsWith('\n') ? body : `${body}\n`);

const edlCsv = (fps) => {
  const rows = ['scene,brief_scene,shot,asset,nominal_start_s,nominal_end_s,start_tc,end_tc,start_frame,end_frame,duration_s,duration_f,direction'];
  for (const scene of scenes) {
    for (const shot of scene.shots) {
      const sf = Math.round(shiftedStart(shot) * fps);
      const ef = Math.round(shiftedEnd(shot, containsFor(scene, shot && scene.shots.indexOf(shot))) * fps);
      rows.push([scene.id, scene.briefScene, shot.id, shot.asset, shot.start.toFixed(2), shot.end.toFixed(2), tc(sf, fps), tc(ef, fps), sf, ef, ((ef - sf) / fps).toFixed(2), ef - sf, q(shot.direction)].join(','));
    }
  }
  return rows.join('\n');
};

const captionCsv = (fps) => {
  const rows = ['scene,id,kind,nominal_start_s,nominal_end_s,start_tc,end_tc,start_frame,end_frame,duration_s,contains_url,arabic,english,latin_line_2,status'];
  for (const c of allCaptions) {
    const sf = Math.round(shiftedStart(c) * fps);
    const ef = Math.round(shiftedEnd(c) * fps);
    const hasUrl = /\.com|\.sa|\.ee|@/.test(c.ar) || Boolean(c.secondLineLatin);
    rows.push([c.scene, c.id, c.kind, c.start.toFixed(2), c.end.toFixed(2), tc(sf, fps), tc(ef, fps), sf, ef, ((ef - sf) / fps).toFixed(2), hasUrl ? 'yes' : 'no', q(c.ar), q(c.en ?? ''), c.secondLineLatin ?? '', gateLabel(c)].join(','));
  }
  return rows.join('\n');
};

const gateLabel = (el) => {
  const g = el.condition ?? el.conditional ?? el.optional ?? el.gate ?? null;
  if (!g) return 'in-cut';
  if (g === 'gate-b-default') return 'in-cut (Gate B default)';
  if (g === 'gate-b-cleared') return 'GATE b ALTERNATE';
  if (g === 'gate-c') return 'GATE c ALTERNATE';
  if (g === 'workshop') return 'OPTIONAL workshop';
  if (g === 'gate-h') return 'badge until Gate H clears';
  return `gated: ${g}`;
};

const voCsv = () => {
  const rows = ['scene,id,brief_line,in_s,words,seconds_at_3wps,window_s,slack_s,status,arabic'];
  // Every line in the script is listed, including the ones this option set does not place,
  // because they still have to be recorded in the session.
  for (const scene of SCENES) {
    for (const v of scene.vo) {
      const r = voRows.find((x) => x.id === v.id);
      let status;
      if (r) status = 'placed';
      else if (v.kind === 'alt') status = `ALTERNATE — record and hold · ${(v.condition ?? 'no gate').replace(/^gate-/, 'Gate ').replace(/\b\w/g, (c) => c.toUpperCase())}`;
      else status = `GATED — not placed in this option set (${v.condition})`;
      rows.push([
        scene.id, v.id, v.briefLine, fx(r ? r.in : v.start), countWords(v.ar),
        (countWords(v.ar) / FILM.arPaceWordsPerSecond).toFixed(2),
        r ? r.window.toFixed(2) : '', r ? r.slack.toFixed(2) : '', status, q(v.ar),
      ].join(','));
    }
  }
  return rows.join('\n');
};

const timelineMd = (fps) => {
  const out = [
    `# Mabkhra Haill — master timeline (${fps} fps, frame-exact)`,
    '',
    `Runtime **${runtimeSeconds.toFixed(1)} s** · ${FILM.aspect} · ${FILM.audio} · master grid ${FILM.masterSeconds.toFixed(1)} s ±${FILM.runtimeToleranceSeconds} s`,
    '',
    `Option set: fps=${fps} · workshop=${OPTIONS.workshop} · gate-b=${OPTIONS.gateB} · gate-c=${OPTIONS.gateC}`,
    '',
  ];
  for (const scene of scenes) {
    out.push(`## ${scene.id} — ${scene.labelAr} / ${scene.labelEn} · brief ${scene.briefScene}`, '');
    out.push(`\`${tc(Math.round(shiftedStart(scene) * fps), fps)}\` → \`${tc(Math.round(sceneEnd(scene) * fps), fps)}\``, '');
    out.push('| Shot | Asset | In | Out | Dur | Direction |', '|---|---|---|---|---|---|');
    for (const [i, shot] of scene.shots.entries()) {
      const s = shiftedStart(shot);
      const e = shiftedEnd(shot, containsFor(scene, i));
      out.push(`| **${shot.id}** | ${shot.asset} | \`${tc(Math.round(s * fps), fps)}\` | \`${tc(Math.round(e * fps), fps)}\` | ${(e - s).toFixed(2)} s | ${shot.direction} |`);
    }
    if (scene.captions.length) {
      out.push('', '| Caption | Kind | In | Out | Dur | Arabic | Latin line 2 | Status |', '|---|---|---|---|---|---|---|---|');
      for (const c of scene.captions) {
        const s = shiftedStart(c);
        const e = shiftedEnd(c);
        out.push(`| ${c.id} | ${c.kind} | \`${tc(Math.round(s * fps), fps)}\` | \`${tc(Math.round(e * fps), fps)}\` | ${(e - s).toFixed(2)} s | ${c.ar.replace(/\n/g, ' / ')} | ${c.secondLineLatin ?? '—'} | ${gateLabel(c)} |`);
      }
    }
    if (scene.vo.length) {
      out.push('', '| VO | Brief line | In | Words | Budget @3 w/s | Sync marks | Status |', '|---|---|---|---|---|---|---|');
      for (const v of scene.vo) {
        const s = shiftedStart(v);
        const marks = (v.syncMarks ?? []).map((m) => `${m.word} @ \`${tc(Math.round((m.target + offset(m.target, 'end', ownInsert(v))) * fps), fps)}\``).join(' · ') || '—';
        out.push(`| ${v.id} | ${v.briefLine} | \`${tc(Math.round(s * fps), fps)}\` | ${countWords(v.ar)} | ${(countWords(v.ar) / FILM.arPaceWordsPerSecond).toFixed(2)} s | ${marks} | ${gateLabel(v)} |`);
      }
    }
    out.push('');
  }
  return out.join('\n');
};

const srt = (lang, fps) => {
  const out = [];
  let n = 0;
  for (const scene of scenes) {
    for (const v of scene.vo.filter((x) => x.kind === 'primary')) {
      const s = shiftedStart(v);
      const dur = Math.max(countWords(v.ar) / FILM.arPaceWordsPerSecond, 1.2);
      n += 1;
      out.push(String(n), `${srtTime(Math.round(s * fps), fps)} --> ${srtTime(Math.round((s + dur) * fps), fps)}`, lang === 'ar' ? v.ar : v.en, '');
    }
  }
  return out.join('\n');
};

const qaReport = (builds) => {
  const row = (set, seconds) => `| ${set} | ${seconds.toFixed(1)} s | ${seconds <= runtimeLimit ? 'yes' : '**no**'} |`;
  return [
    '# QA report — generated',
    '',
    `Generated ${new Date().toISOString().slice(0, 10)} from \`tools/film-data.mjs\`. Re-run \`node tools/build-files.mjs\` after any timing edit.`,
    '',
    `Options: fps=${OPTIONS.fps} · workshop=${OPTIONS.workshop} · gate-b=${OPTIONS.gateB} · gate-c=${OPTIONS.gateC}`,
    '',
    `**Runtime ${runtimeSeconds.toFixed(1)} s** (ceiling ${runtimeLimit.toFixed(1)} s) · **${problems.length} failures · ${warnings.length} warnings**`,
    '',
    '## Failures', '',
    problems.length ? problems.map((p) => `- ${p}`).join('\n') : '- none', '',
    '## Warnings', '',
    warnings.length ? warnings.map((w) => `- ${w}`).join('\n') : '- none', '',
    '## Notes', '',
    notes.length ? notes.map((x) => `- ${x}`).join('\n') : '- none', '',
    '## Frame quantisation (nominal half-second grid → whole frames)', '',
    '| fps | times falling between frames | worst rounding error |', '|---|---|---|',
    ...builds.map(({ fps, drift, fractional }) => `| ${fps} | ${fractional} | ${drift.toFixed(3)} f (${(drift / fps).toFixed(3)} s) |`), '',
    '## Runtime by option set', '',
    '| Option set | Runtime | Inside 2:22 ±3 s |', '|---|---|---|',
    row('Base master', FILM.masterSeconds),
    row('+ workshop beat (2.5 s)', FILM.masterSeconds + 2.5),
    row('+ Gate B free-shipping line (1.8 s)', FILM.masterSeconds + 1.8),
    row('+ Gate C Amazon/Noon card (4.4 s)', FILM.masterSeconds + 4.4),
    row('+ workshop + Gate B (4.3 s)', FILM.masterSeconds + 4.3),
    row('+ Gate B + Gate C (6.2 s)', FILM.masterSeconds + 6.2),
    row('+ every optional element (8.7 s)', FILM.masterSeconds + 8.7), '',
    '## Asset status', '',
    '| Status | Count |', '|---|---|',
    ...['supplied', 'required', 'not-in-package'].map((s) => `| ${s} | ${ASSETS.filter((a) => a.status === s).length} |`), '',
    'Referenced by shots but not supplied:', '',
    blocking.map((a) => `- \`${a.id}\` — ${a.name}`).join('\n') || '- none', '',
  ].join('\n');
};

/* ------------------------------------------------------------ execute */

const fpsList = OPTIONS.fps === 'both' ? FILM.fpsOptions : [Number(OPTIONS.fps)];
const fpsPrimary = fpsList[0];
const builds = [];
for (const fps of fpsList) {
  let maxDrift = 0;
  let fractional = 0;
  for (const scene of scenes) {
    for (const shot of scene.shots) {
      for (const t of [shot.start, shot.end]) {
        const d = Math.abs(t * fps - Math.round(t * fps));
        if (d > 0.0001) { fractional += 1; maxDrift = Math.max(maxDrift, d); }
      }
    }
  }
  builds.push({ fps, drift: maxDrift, fractional });
  write(`edl-${fps}fps.csv`, edlCsv(fps));
  write(`timeline-${fps}fps.md`, timelineMd(fps));
  write(`caption-timing-${fps}fps.csv`, captionCsv(fps));
}
write('vo-budget.csv', voCsv());
write('captions-ar.srt', srt('ar', fpsPrimary));
write('captions-en.srt', srt('en', fpsPrimary));
write('asset-manifest.csv', ['id,asset,type,status,note', ...ASSETS.map((a) => [a.id, q(a.name), a.type, a.status, q(a.note ?? '')].join(','))].join('\n'));
write('qa-report.md', qaReport(builds));

console.log(`Mabkhra Haill — build ${problems.length === 0 ? 'PASSED' : 'FAILED'}`);
console.log(`runtime ${runtimeSeconds.toFixed(1)} s (ceiling ${runtimeLimit.toFixed(1)} s) · failures ${problems.length} · warnings ${warnings.length}`);
for (const p of problems) console.log(`  FAIL  ${p}`);
for (const w of warnings) console.log(`  warn  ${w}`);
for (const n of notes) console.log(`  note  ${n}`);
console.log(`wrote ${OPTIONS.out.replace(`${root}/`, '')}/`);
if (problems.length) process.exitCode = 1;
