#!/usr/bin/env node
/**
 * Mabkhra Haill — link directory probe.
 *
 *   node brand-film/tools/probe-links.mjs           # human-readable report
 *   node brand-film/tools/probe-links.mjs --json    # machine-readable
 *   node brand-film/tools/probe-links.mjs --only=instagram,x,tiktok
 *
 * Follows redirects and reports the final URL, so a link that "works" but lands
 * somewhere else — a country gate, a login wall, a personal profile — is caught.
 * Run it from a machine with open network access (Gate I). Nothing is written
 * to disk unless --json is combined with --out=<file>.
 *
 * Reads the directory from tools/film-data.mjs so the film and the probe can
 * never disagree about what the brand's addresses are.
 */

import { writeFileSync } from 'node:fs';
import { FILM, LINKS } from './film-data.mjs';

const args = process.argv.slice(2);
const has = (name) => args.includes(`--${name}`);
const value = (name) => {
  const hit = args.find((a) => a.startsWith(`--${name}=`));
  return hit ? hit.split('=')[1] : null;
};

const only = value('only')?.split(',').map((s) => s.trim().toLowerCase()).filter(Boolean);
const wantJson = has('json');
const out = value('out');

const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36';

const labelOf = (link) => link.labelAr;

/** A link is only "clean" when it resolves 2xx without being bounced somewhere unexpected. */
async function probe(link) {
  const url = link.url.replace(/^mailto:/, '');
  if (link.url.startsWith('mailto:')) {
    return { status: 'manual', http: null, final: link.url, note: 'mailto — send a test mail from an external account' };
  }
  if (!link.url) {
    return { status: 'held', http: null, final: '', note: 'held pending owner verification' };
  }
  try {
    const res = await fetch(url, { redirect: 'follow', headers: { 'user-agent': UA, 'accept-language': 'ar,en' } });
    const final = res.url;
    const moved = final.replace(/\/$/, '') !== url.replace(/\/$/, '');
    const gate = /select-country|login|signin|accounts\.|\/checkpoint/i.test(final);
    return {
      status: res.ok && !gate ? (moved ? 'redirected' : 'ok') : res.ok ? 'gated' : 'failed',
      http: res.status,
      final,
      note: gate ? 'landed on a gate/login wall — a viewer would see this, not the store' : moved ? `redirects to ${final}` : '',
    };
  } catch (error) {
    return { status: 'error', http: null, final: '', note: String(error.message ?? error) };
  }
}

/* Preflight: distinguish "the links are broken" from "this machine has no network".
   Without it, an offline sandbox reports twelve false failures. */
async function online() {
  for (const probeUrl of ['https://example.com/', 'https://www.cloudflare.com/']) {
    try {
      const res = await fetch(probeUrl, { method: 'HEAD', redirect: 'follow' });
      if (res.status < 500) return true;
    } catch {
      /* try the next one */
    }
  }
  return false;
}

const targets = LINKS.filter((l) => !only || only.some((k) => `${l.labelAr} ${l.url}`.toLowerCase().includes(k)));
if (!(await online())) {
  console.error('\nNo outbound network from this machine — nothing was actually probed.');
  console.error('The link directory cannot be verified from here. Run this from a networked machine');
  console.error('(or a CI runner), or check the URLs by hand in a browser.\n');
  process.exit(2);
}

const results = [];
for (const link of targets) {
  const result = await probe(link);
  results.push({ label: labelOf(link), url: link.url, burned: Boolean(link.burn), ...result });
}

const failing = results.filter((r) => !['ok', 'redirected'].includes(r.status));

if (wantJson) {
  const body = JSON.stringify({ brand: FILM.brand, probedAt: new Date().toISOString(), results }, null, 2);
  if (out) {
    writeFileSync(out, `${body}\n`);
    console.error(`wrote ${out}`);
  } else {
    console.log(body);
  }
} else {
  console.log(`\n${FILM.brand} — link directory probe · ${new Date().toISOString().slice(0, 16).replace('T', ' ')}\n`);
  for (const r of results) {
    const mark = r.status === 'ok' ? '✅' : r.status === 'redirected' ? '↪️ ' : r.status === 'gated' ? '⚠️ ' : r.status === 'manual' || r.status === 'held' ? '•  ' : '❌';
    console.log(`${mark} ${r.label.padEnd(24)} ${r.status.padEnd(11)} ${r.http ?? ''}  ${r.burned ? '(burned)' : ''}`);
    if (r.final && r.final !== r.url) console.log(`     → ${r.final}`);
    if (r.note) console.log(`     ${r.note}`);
  }
  console.log(`\n${results.length - failing.length}/${results.length} clean · ${failing.length} need attention`);
  console.log('A link that resolves but lands on a country gate or a login wall counts as needing attention.\n');
}

if (failing.length) process.exitCode = 1;
