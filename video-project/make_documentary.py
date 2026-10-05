#!/usr/bin/env python3
"""Build the RaazNama AI pyramids documentary from locally generated assets.

Requires the three voice tracks created with Arena speech and the image assets in
../video-assets.  The only external runtime dependency is the local ffmpeg binary
installed under .video-tools by the build session.
"""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECT = ROOT / "video-project"
ASSETS = ROOT / "video-assets"
RENDER = PROJECT / "render"
FFMPEG = Path(os.environ.get(
    "FFMPEG_BIN", ROOT / ".video-tools/node_modules/@ffmpeg-installer/linux-x64/ffmpeg"
))
FPS = 30
WIDTH, HEIGHT = 1280, 720
TOTAL = 306.0


def run(cmd: list[str]) -> None:
    print("+", " ".join(str(x) for x in cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def ass_time(seconds: float) -> str:
    centis = round(max(seconds, 0) * 100)
    cs = centis % 100
    seconds = centis // 100
    sec = seconds % 60
    minutes = (seconds // 60) % 60
    hours = seconds // 3600
    return f"{hours}:{minutes:02d}:{sec:02d}.{cs:02d}"


def srt_time(seconds: float) -> str:
    millis = round(max(seconds, 0) * 1000)
    ms = millis % 1000
    seconds = millis // 1000
    sec = seconds % 60
    minutes = (seconds // 60) % 60
    hours = seconds // 3600
    return f"{hours:02d}:{minutes:02d}:{sec:02d},{ms:03d}"


def wrap_caption(text: str, width: int = 52) -> str:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        proposal = f"{current} {word}".strip()
        if current and len(proposal) > width:
            lines.append(current)
            current = word
        else:
            current = proposal
    if current:
        lines.append(current)
    # Keep captions clean and readable: two concise lines maximum.
    if len(lines) > 2:
        lines = [" ".join(words[: len(words) // 2]), " ".join(words[len(words) // 2 :])]
    return "\\N".join(lines)


def ass_escape(text: str) -> str:
    return text.replace("\\", r"\\").replace("{", r"\{").replace("}", r"\}")


def subtitle_events() -> list[tuple[float, float, str]]:
    """Time paragraph subtitles proportionally within each paced voice segment."""
    parts = [
        PROJECT / "voice-part-01.txt",
        PROJECT / "voice-part-02.txt",
        PROJECT / "voice-part-03.txt",
    ]
    # final start time after intro and two intentional breathing spaces
    starts = [6.0, 111.73, 197.47]
    durations = [101.73, 81.73, 81.09]
    events: list[tuple[float, float, str]] = []
    for path, start, duration in zip(parts, starts, durations):
        paras = [p.strip().replace("\n", " ") for p in path.read_text(encoding="utf-8").split("\n\n") if p.strip()]
        # A small per-paragraph allowance reflects the natural pauses in TTS.
        weights = [len(p) + 26 + 12 * sum(p.count(c) for c in ".?!…") for p in paras]
        scale = duration / sum(weights)
        cursor = start
        for p, weight in zip(paras, weights):
            end = cursor + weight * scale
            events.append((cursor, end, p))
            cursor = end
    return events


def write_subtitles() -> None:
    subtitles = subtitle_events()
    ass = """[Script Info]
Title: RaazNama AI — Misr Ke Pyramids Ke 5 Hairan Kun Raaz
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
ScaledBorderAndShadow: yes
WrapStyle: 0

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Subtitle,DejaVu Sans,31,&H00FFFFFF,&H000000FF,&HDC05080B,&H64000000,-1,0,0,0,100,100,0,0,1,2.6,1.1,2,92,92,42,1
Style: Eyebrow,DejaVu Sans,17,&H00E8BC67,&H000000FF,&H90000000,&H64000000,-1,0,0,0,100,100,2,0,1,1.2,0.7,8,60,60,40,1
Style: Title,DejaVu Serif,51,&H00F8E6C4,&H000000FF,&HCF090B10,&H64000000,-1,0,0,0,100,100,1,0,1,2.0,1.0,5,68,68,0,1
Style: Topic,DejaVu Sans,34,&H00F5D38C,&H000000FF,&HCD06080C,&H64000000,-1,0,0,0,100,100,1.2,0,1,2.0,1.0,8,62,62,55,1
Style: TopicSmall,DejaVu Sans,19,&H00FFFFFF,&H000000FF,&HCD06080C,&H64000000,-1,0,0,0,100,100,1.0,0,1,1.5,0.8,8,62,62,97,1
Style: Watermark,DejaVu Sans,16,&H99FFFFFF,&H000000FF,&H90000000,&H64000000,-1,0,0,0,100,100,0,0,1,1.0,0.5,9,35,35,27,1
Style: Endcard,DejaVu Sans,29,&H00F7D994,&H000000FF,&HCE06080C,&H64000000,-1,0,0,0,100,100,1.0,0,1,1.8,1.0,5,60,60,0,1
Style: EndSmall,DejaVu Sans,18,&H00FFFFFF,&H000000FF,&HCF06080C,&H64000000,0,0,0,0,100,100,1.0,0,1,1.2,0.7,5,60,60,75,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    lines = [ass]
    # Discreet, persistent channel bug.
    lines.append(f"Dialogue: 0,{ass_time(0)},{ass_time(TOTAL)},Watermark,,0,0,0,,RAAZNAMA AI  |  راز نامہ")
    # Opening title treatment.
    lines += [
        f"Dialogue: 2,{ass_time(0.55)},{ass_time(10.8)},Eyebrow,,0,0,0,,ANCIENT EGYPT  •  EVIDENCE-LED HISTORY",
        f"Dialogue: 2,{ass_time(1.2)},{ass_time(10.8)},Title,,0,0,0,,MISR KE PYRAMIDS KE\\N5 HAIRAN KUN RAAZ",
        f"Dialogue: 2,{ass_time(11.2)},{ass_time(16.2)},Topic,,0,0,0,,Ek safar… hazaron saal pehle",
    ]
    topics = [
        (40.0, 53.0, "RAAZ #5", "PATHARON KA WAZAN"),
        (96.0, 109.0, "RAAZ #4", "HAIRAT ANGEEZ PRECISION"),
        (124.0, 137.0, "RAAZ #3", "ANDAR CHHUPE RAASTE"),
        (166.0, 179.0, "RAAZ #2", "PYRAMID ITNA SMOOTH THA?"),
        (208.0, 221.0, "RAAZ #1", "AAKHIR BANAYA KYUN GAYA?"),
    ]
    for st, en, top, small in topics:
        lines.append(f"Dialogue: 2,{ass_time(st)},{ass_time(en)},Topic,,0,0,0,,{top}")
        lines.append(f"Dialogue: 2,{ass_time(st)},{ass_time(en)},TopicSmall,,0,0,0,,{small}")
    # CTA begins during the narrated closing and remains through the end card.
    lines += [
        f"Dialogue: 2,{ass_time(244.0)},{ass_time(276.0)},Endcard,,0,0,0,,RAAZNAMA AI KO SUBSCRIBE KAREIN",
        f"Dialogue: 2,{ass_time(276.0)},{ass_time(TOTAL)},Endcard,,0,0,0,,SUBSCRIBE  |  RAAZNAMA AI",
        f"Dialogue: 2,{ass_time(288.0)},{ass_time(TOTAL)},EndSmall,,0,0,0,,Ancient Civilizations  •  Hidden History  •  New Mysteries",
    ]
    for start, end, text in subtitles:
        lines.append(
            f"Dialogue: 1,{ass_time(start)},{ass_time(end)},Subtitle,,0,0,0,,{wrap_caption(ass_escape(text))}"
        )
    (RENDER / "subtitles.ass").write_text("\n".join(lines) + "\n", encoding="utf-8")

    srt_lines: list[str] = []
    for index, (start, end, text) in enumerate(subtitles, 1):
        srt_lines += [str(index), f"{srt_time(start)} --> {srt_time(end)}", wrap_caption(text).replace("\\N", "\n"), ""]
    (RENDER / "raaznama-pyramids-subtitles.srt").write_text("\n".join(srt_lines), encoding="utf-8")


def make_audio() -> None:
    slow_paths = []
    for index in range(1, 4):
        source = PROJECT / "audio" / f"voice-{index:02d}.mp3"
        output = RENDER / f"voice-{index:02d}-paced.wav"
        run([
            str(FFMPEG), "-y", "-i", str(source), "-filter:a",
            "atempo=0.75,aresample=48000,aformat=channel_layouts=stereo,volume=1.08",
            "-c:a", "pcm_s16le", str(output),
        ])
        slow_paths.append(output)

    # 6 sec opening atmosphere, 4 sec conceptual breaths between the voice chunks,
    # and a 27.45 sec branded end-card/music bed. Final trim guarantees 05:06.
    narration = RENDER / "narration.wav"
    run([
        str(FFMPEG), "-y",
        "-f", "lavfi", "-t", "6", "-i", "anullsrc=r=48000:cl=stereo",
        "-i", str(slow_paths[0]),
        "-f", "lavfi", "-t", "4", "-i", "anullsrc=r=48000:cl=stereo",
        "-i", str(slow_paths[1]),
        "-f", "lavfi", "-t", "4", "-i", "anullsrc=r=48000:cl=stereo",
        "-i", str(slow_paths[2]),
        "-f", "lavfi", "-t", "27.45", "-i", "anullsrc=r=48000:cl=stereo",
        "-filter_complex", "[0:a][1:a][2:a][3:a][4:a][5:a][6:a]concat=n=7:v=0:a=1,atrim=duration=306,asetpts=N/SR/TB[a]",
        "-map", "[a]", "-c:a", "pcm_s16le", str(narration),
    ])

    music = RENDER / "suspense-bed.wav"
    # Original, deliberately understated minor drone: no third-party music or licensing uncertainty.
    expr = (
        "0.22*sin(2*PI*65.4064*t)*(0.70+0.30*sin(2*PI*0.014*t))"
        "+0.12*sin(2*PI*97.9989*t)*(0.62+0.38*sin(2*PI*0.021*t))"
        "+0.055*sin(2*PI*155.5635*t)*(0.50+0.50*sin(2*PI*0.085*t))"
        "+0.020*sin(2*PI*261.626*t)*(0.50+0.50*sin(2*PI*0.10*t))"
    )
    run([
        str(FFMPEG), "-y", "-f", "lavfi", "-i", f"aevalsrc={expr}:s=48000:d={TOTAL}",
        "-filter:a", "aformat=channel_layouts=stereo,volume=0.16,afade=t=in:st=0:d=3,afade=t=out:st=294:d=12",
        "-c:a", "pcm_s16le", str(music),
    ])
    mix = RENDER / "final-audio.m4a"
    run([
        str(FFMPEG), "-y", "-i", str(narration), "-i", str(music),
        "-filter_complex", "[0:a]volume=1.45[n];[1:a]volume=1.0[m];[n][m]amix=inputs=2:duration=first,alimiter=limit=0.95[a]",
        "-map", "[a]", "-c:a", "aac", "-b:a", "160k", str(mix),
    ])


def make_video() -> None:
    # Each still receives a slow push-in and a gentle fade through black.  This avoids
    # static slideshow pacing while keeping the visual grammar calm and documentary-like.
    scenes = [
        ("01-giza-dawn.png", 15), ("09-giza-map.png", 15), ("01-giza-dawn.png", 12),
        ("03-stone-block-detail.png", 14), ("02-ancient-builders.png", 14), ("03-stone-block-detail.png", 14),
        ("12-ancient-planning.png", 14), ("04-cardinal-stars.png", 14), ("10-ancient-surveying.png", 14),
        ("05-pyramid-interior.png", 14), ("05-pyramid-interior.png", 14), ("06-muon-scan.png", 14),
        ("05-pyramid-interior.png", 14), ("07-white-casing.png", 14), ("11-limestone-casing.png", 14),
        ("07-white-casing.png", 14), ("08-khufu-complex.png", 14), ("13-royal-tomb-complex.png", 14),
        ("08-khufu-complex.png", 14), ("14-giza-night.png", 14), ("14-giza-night.png", 14),
        ("14-giza-night.png", 12),
    ]
    inputs: list[str] = []
    graph: list[str] = []
    labels: list[str] = []
    for idx, (name, duration) in enumerate(scenes):
        inputs += ["-framerate", str(FPS), "-loop", "1", "-t", str(duration), "-i", str(ASSETS / name)]
        fade_out_start = max(0.0, duration - 0.65)
        # The tiny drift differs per scene, so the motion does not look mechanically identical.
        speed = 0.00012 + (idx % 4) * 0.000035
        pan_x = 2 + (idx % 3) * 4
        pan_y = 1 + (idx % 2) * 3
        graph.append(
            f"[{idx}:v]scale={WIDTH}:{HEIGHT},zoompan=z='min(zoom+{speed:.6f},1.075)':"
            f"x='iw/2-(iw/zoom/2)+sin(on/55)*{pan_x}':y='ih/2-(ih/zoom/2)+cos(on/61)*{pan_y}':"
            f"d=1:s={WIDTH}x{HEIGHT}:fps={FPS},fade=t=in:st=0:d=0.65,fade=t=out:st={fade_out_start:.2f}:d=0.65,format=yuv420p[v{idx}]"
        )
        labels.append(f"[v{idx}]")
    graph.append("".join(labels) + f"concat=n={len(scenes)}:v=1:a=0[base]")
    graph.append("[base]setsar=1,ass=video-project/render/subtitles.ass,format=yuv420p[final]")
    silent_video = RENDER / "visuals.mp4"
    run([
        str(FFMPEG), "-y", *inputs, "-filter_complex", ";".join(graph), "-map", "[final]",
        "-t", str(TOTAL), "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(silent_video),
    ])
    final = RENDER / "RaazNamaAI_Misr_Ke_Pyramids_Ke_5_Raaz_720p.mp4"
    run([
        str(FFMPEG), "-y", "-i", str(silent_video), "-i", str(RENDER / "final-audio.m4a"),
        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
        "-t", str(TOTAL), "-movflags", "+faststart", str(final),
    ])


def main() -> None:
    if not FFMPEG.exists():
        raise SystemExit(f"ffmpeg missing: {FFMPEG}")
    RENDER.mkdir(parents=True, exist_ok=True)
    write_subtitles()
    make_audio()
    make_video()
    print(f"\nDone: {RENDER / 'RaazNamaAI_Misr_Ke_Pyramids_Ke_5_Raaz_720p.mp4'}")


if __name__ == "__main__":
    main()
