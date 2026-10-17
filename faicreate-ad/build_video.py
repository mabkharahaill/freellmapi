#!/usr/bin/env python3
"""Assemble the 120s FAI CREATE ad: scene clips -> transitions -> subtitles -> audio -> mux.
All ffmpeg calls use argument lists (no shell) to avoid quoting issues."""
import json
import os
import re
import subprocess
import sys

import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

B = [0, 12, 27, 43, 60, 76, 93, 106, 114, 120]  # scene boundaries
F = 0.5  # transition duration
FPS = 30


def clip_dur(i):
    return (B[i + 1] - B[i] - F) if i < 8 else (B[9] - B[8])


def ff_dur(path):
    out = subprocess.run([FF, "-i", path], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", out)
    h, mn, s = m.groups()
    return int(h) * 3600 + int(mn) * 60 + float(s)


def run(args, label):
    print(f"== {label} ==")
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        raise SystemExit(f"FAILED: {label}")
    print("ok")


PANS = [
    ("144*t/{D}", "128"),
    ("72", "256*t/{D}"),
    ("144-144*t/{D}", "128"),
    ("72", "230-170*t/{D}"),
    ("144*t/{D}", "128"),
    ("72", "256*t/{D}"),
    ("144-144*t/{D}", "128"),
    ("72", "256-256*t/{D}"),
]
TRANS = ["fade", "smoothleft", "circleopen", "smoothright", "fade", "dissolve", "smoothleft", "fade"]
VENC = ["-c:v", "libx264", "-preset", "medium", "-r", str(FPS), "-pix_fmt", "yuv420p"]


def build_clips():
    os.makedirs("build", exist_ok=True)
    for i in range(1, 10):
        d = clip_dur(i - 1)
        out = f"build/clip0{i}.mp4"
        if i == 9:
            frames = int(round(d * FPS))
            zoom_step = 0.138 / frames
            fc = (
                f"[0:v]scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
                f"zoompan=z='1+{zoom_step:.6f}*in':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2'"
                f":d={frames}:s=1080x1920:fps={FPS},"
                f"eq=saturation=1.05:contrast=1.03,format=yuv420p[bg];"
                f"[1:v]fade=t=in:st=0.35:d=0.9:alpha=1[logo];"
                f"[bg][logo]overlay=220:560,format=yuv420p[v]"
            )
            args = [FF, "-y", "-framerate", str(FPS), "-i", "video/scene09.png",
                    "-framerate", str(FPS), "-loop", "1", "-t", f"{d:.3f}", "-i", "build/logo_badge640.png",
                    "-filter_complex", fc, "-map", "[v]"] + VENC + ["-crf", "18", out]
        else:
            xe, ye = PANS[i - 1]
            fade_in = "fade=t=in:st=0:d=0.35," if i == 1 else ""
            fc = (
                f"[0:v]scale=1224:2176:force_original_aspect_ratio=increase,crop=1224:2176,"
                f"crop=1080:1920:x='{xe.format(D=round(d, 3))}':y='{ye.format(D=round(d, 3))}',"
                f"eq=saturation=1.05:contrast=1.03,format=yuv420p[bg];"
                f"[1:v]fade=t=in:st=0:d=0.7:alpha=1[wm];"
                f"[bg][wm]overlay=48:110,{fade_in}format=yuv420p[v]"
            )
            args = [FF, "-y", "-framerate", str(FPS), "-loop", "1", "-t", f"{d:.3f}",
                    "-i", f"video/scene0{i}.png",
                    "-framerate", str(FPS), "-loop", "1", "-t", f"{d:.3f}", "-i", "build/wm_badge170.png",
                    "-filter_complex", fc, "-map", "[v]"] + VENC + ["-crf", "18", out]
        run(args, f"clip {i}")
    for i in range(1, 10):
        got = ff_dur(f"build/clip0{i}.mp4")
        exp = clip_dur(i - 1)
        assert abs(got - exp) < 0.15, (i, got, exp)
    print("clips ok")
    build_transitions()


def build_transitions():
    for k in range(1, 9):
        a = f"build/clip0{k}.mp4"
        b = f"build/clip0{k + 1}.mp4"
        out = f"build/trans0{k}.mp4"
        dsa = clip_dur(k - 1) - F
        fc = (f"[0:v][1:v]xfade=transition={TRANS[k - 1]}:duration={F}:offset=0,"
              f"format=yuv420p[v]")
        run([FF, "-y", "-ss", f"{dsa:.3f}", "-t", str(F), "-i", a,
             "-t", str(F), "-i", b,
             "-filter_complex", fc, "-map", "[v]"] + VENC + ["-crf", "18", out],
            f"transition {k}")


def cue_timing(voice_durs):
    from sub_render import CUES
    by_scene = {}
    for i, (sc, text) in enumerate(CUES, 1):
        by_scene.setdefault(sc, []).append((i, text))
    result = []
    for sc in sorted(by_scene):
        cues = by_scene[sc]
        D = voice_durs[sc - 1]
        start = B[sc - 1] + 0.15
        total_chars = sum(len(t) for _, t in cues)
        t = start
        for k, (idx, text) in enumerate(cues):
            ratio = len(text) / total_chars
            span = D * ratio
            a = t + 0.05
            if k == len(cues) - 1:
                b = min(start + D + 0.55, B[sc] - 0.25)
            else:
                b = min(a + span - 0.12, start + D)
            result.append((idx, max(start, a), max(b, a + 0.6)))
            t += span
    return result


def assemble(voice_durs):
    # --- pass 1: concat clips + transitions ---
    order = []
    for k in range(1, 10):
        order.append(f"build/clip0{k}.mp4")
        if k < 9:
            order.append(f"build/trans0{k}.mp4")
    with open("build/concat.txt", "w") as f:
        f.write("\n".join(f"file '{os.path.basename(p)}'" for p in order))
    run([FF, "-y", "-f", "concat", "-safe", "0", "-i", "build/concat.txt",
         "-c", "copy", "build/base.mp4"], "pass1 concat")
    got = ff_dur("build/base.mp4")
    assert abs(got - 120.0) < 0.2, got
    run([FF, "-y", "-i", "build/base.mp4",
         "-vf", "fade=t=out:st=119.35:d=0.65"] + VENC + ["-crf", "18", "build/base2.mp4"],
        "pass1b fadeout")

    # --- pass 2: subtitle track (pre-baked RGBA sequence) ---
    run([FF, "-y", "-i", "build/base2.mp4",
         "-framerate", str(FPS), "-i", "build/substrack/frame_%04d.png",
         "-filter_complex", "[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[v]",
         "-map", "[v]"] + VENC + ["-crf", "18", "build/video_subs.mp4"], "pass2 subtitles")

    # --- pass 3: (lockup text is baked into the subtitle track) ---
    run([FF, "-y", "-i", "build/video_subs.mp4",
         "-c:v", "copy", "build/video_final.mp4"], "pass3 copy")
    print("video ok, dur", ff_dur("build/video_final.mp4"))


def mix_audio(voice_durs):
    for i, d in enumerate(voice_durs):
        seg = B[i + 1] - B[i]
        if i == 8:
            limit = (120.0 - 113.6) * 1.03  # starts early, slightly sped up
        else:
            limit = seg - 0.3
        assert d < limit, (i + 1, d, seg)
    args = [FF, "-y"]
    for i in range(1, 10):
        args += ["-i", f"audio/vo{i}.mp3"]
    args += ["-i", "audio/music.wav"]
    delays = ""
    for i in range(9):
        if i == 8:
            delays += "[8:a]atempo=1.03,adelay=113600:all=1[v8];"
        else:
            delays += f"[{i}:a]adelay={int(B[i] * 1000)}:all=1[v{i}];"
    fc = (delays +
          "".join(f"[v{i}]" for i in range(9)) +
          "amix=inputs=9:normalize=0:dropout_transition=0[voice];"
          "[9:a]volume=0.82[bed];"
          "[voice]asplit=2[vk][vv];"
          "[bed][vk]sidechaincompress=threshold=0.055:ratio=6:attack=18:release=380:makeup=1.0[duck];"
          "[vv]volume=1.28[vo2];"
          "[duck][vo2]amix=inputs=2:normalize=0[loud];"
          "[loud]loudnorm=I=-14:TP=-1.5:LRA=11,apad=whole_dur=120[aout]")
    args += ["-filter_complex", fc, "-map", "[aout]", "-c:a", "pcm_s16le", "build/final_mix.wav"]
    run(args, "audio mix")
    print("audio ok")


def mux():
    run([FF, "-y", "-i", "build/video_final.mp4", "-i", "build/final_mix.wav",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
         "-shortest", "FAI_Create_Ad_120s_1080x1920.mp4"], "mux")
    print("FINAL", ff_dur("FAI_Create_Ad_120s_1080x1920.mp4"), "s")


def main():
    step = sys.argv[1] if len(sys.argv) > 1 else "all"
    voice_durs = [ff_dur(f"audio/vo{i}.mp3") for i in range(1, 10)]
    print("voice durations:", [round(d, 2) for d in voice_durs])
    if step in ("clips", "all"):
        build_clips()
    if step in ("assemble", "all"):
        assemble(voice_durs)
    if step in ("audio", "all"):
        mix_audio(voice_durs)
    if step in ("mux", "all"):
        mux()


if __name__ == "__main__":
    main()
