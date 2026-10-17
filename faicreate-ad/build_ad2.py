#!/usr/bin/env python3
"""FAI CREATE CINEMATIC AD — beat-based build.
Usage: python3 build_ad2.py <beats|clips|trans|concat|video|audio|mux|all>
"""
import os
import re
import subprocess
import sys

FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
FPS = 30
VENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", str(FPS)]

# VO start times (s); vo9 starts early at 113.6 with atempo 1.03
VO_DELAYS = [0, 12, 27, 43, 60, 76, 93, 106, 113.6]

# scene beats: (file, dur, motion, tap_t, tap_x, tap_y)
SCENES = [
    [("video/s1a.png", 4.0, "push", None),
     ("video/s1b.png", 4.0, "push", None),
     ("build/ui/card_hero.png", 4.5, "push_slow", None)],                       # 11.5
    [("build/ui/ui_home.png", 5.0, "still", 2.2, 540, 1400),
     ("build/ui/ui_tools.png", 5.0, "still", 2.0, 540, 1127),
     ("build/ui/card_tools.png", 5.5, "push_slow", None)],                      # 14.5
    [("build/ui/ui_image1.png", 5.0, "still", None),
     ("build/ui/ui_image2.png", 5.0, "still", None),
     ("video/s3_result.png", 6.5, "reveal", None)],                             # 15.5
    [("build/ui/ui_img2vid.png", 5.0, "still", 2.0, 540, 770),
     ("video/s4c.png", 6.0, "push", None),
     ("build/ui/card_story.png", 6.5, "push_slow", None)],                      # 16.5
    [("build/ui/ui_storyfilm.png", 8.5, "still", None),
     ("build/ui/ui_music.png", 7.5, "still", None)],                            # 15.5
    [("video/s6a.png", 5.5, "push", None),
     ("build/ui/ui_ads.png", 5.5, "still", 2.0, 540, 1471),
     ("video/s6b.png", 6.5, "push", None)],                                     # 16.5
    [("build/ui/ui_lang.png", 4.5, "still", 2.0, 540, 751),
     ("video/s7b.png", 4.5, "push", None),
     ("build/ui/ui_gaming.png", 4.5, "still", None)],                           # 12.5
    [("build/ui/ui_account.png", 3.5, "still", 1.6, 540, 1081),
     ("build/ui/ui_plans.png", 4.5, "still", 2.0, 540, 1651)],                  # 7.5
    [("video/scene09.png", 6.0, "push_slow", None)],                            # 6.0
]
EXPECTED = [11.5, 14.5, 15.5, 16.5, 15.5, 16.5, 12.5, 7.5, 6.0]
WM_BEATS = {"video/s1a.png", "video/s1b.png", "video/s3_result.png", "video/s4c.png",
            "video/s6a.png", "video/s6b.png", "video/s7b.png"}
TRANS = ["fade", "smoothleft", "circleopen", "smoothright", "fade",
         "dissolve", "smoothleft", "fade"]

def run(args, label):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2500:])
        raise SystemExit(f"FAILED: {label}")
    print(f"== {label} == ok")

def ff_dur(path):
    r = subprocess.run([FF, "-i", path], capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))

def beat_path(si, bi):
    return f"build/b{si:02d}{bi}.mp4"

# ---------------- beats ----------------
def render_beat(si, bi, spec):
    f, dur, motion, tap_t = spec[0], spec[1], spec[2], spec[3]
    tap_x = spec[4] if len(spec) > 4 else None
    tap_y = spec[5] if len(spec) > 5 else None
    out = beat_path(si, bi)
    frames = int(round(dur * FPS))
    args = [FF, "-y", "-loop", "1", "-framerate", str(FPS), "-t", f"{dur:.3f}", "-i", f]
    inputs = 1
    fc = ""
    if motion == "still":
        fc += "[0:v]format=rgba[b];"
    else:
        fr = int(round(dur * FPS))
        z = {"push": f"1+0.09*min(max(on/{fr},0),1)",
             "push_slow": f"1+0.045*min(max(on/{fr},0),1)",
             "reveal": f"1.12-0.12*min(max(on/{fr},0),1)"}[motion]
        chain = (f"[0:v]scale=1296:2304:force_original_aspect_ratio=increase,"
                 f"crop=1296:2304,zoompan=z='{z}':d=1:"
                 f"x='iw/2-(iw/zoom)/2':y='ih/2-(ih/zoom)/2':"
                 f"s=1080x1920:fps={FPS}")
        if motion == "reveal":
            chain += ",fade=t=in:st=0:d=0.45:color=black"
        chain += ",eq=saturation=1.05:contrast=1.03,format=rgba[b];"
        fc += chain
    node = "b"
    if f in WM_BEATS:
        args += ["-i", "build/wm_badge170.png"]
        fc += f"[{node}][{inputs}:v]overlay=48:110[{node}w];"
        node += "w"
        inputs += 1
    if si == 8:  # final scene: big brand badge
        # -loop 1 -framerate is REQUIRED: a bare single-frame PNG input has one
        # frame at t=0, so the alpha fade-in only ever sees t=0 (alpha=0) and
        # overlay holds that fully-transparent frame forever -> badge invisible
        args += ["-loop", "1", "-framerate", str(FPS), "-i", "build/logo_badge640.png"]
        fc += (f"[{inputs}:v]format=rgba,fade=t=in:st=0.4:d=0.9:alpha=1[{node}l];"
               f"[{node}][{node}l]overlay=220:560[{node}g];")
        node += "g"
        inputs += 1
    if tap_t is not None:
        t0 = tap_t - 0.7
        yexpr = f"{tap_y - 420}+320*min(max((t-{t0:.3f})/0.7,0),1)"
        args += ["-i", "build/dot.png", "-framerate", str(FPS),
                 "-i", "build/ripple/ripple_%02d.png"]
        fc += (f"[{inputs}:v]format=rgba[{node}d];"
               f"[{inputs + 1}:v]format=rgba,setpts=PTS+{tap_t:.3f}/TB[{node}r];"
               f"[{node}][{node}d]overlay=x='{tap_x - 100}':y='{yexpr}':"
               f"enable='gte(t,{t0 - 0.1:.3f})'[{node}a];"
               f"[{node}a][{node}r]overlay={tap_x - 260}:{tap_y - 260}:"
               f"enable='gte(t,{tap_t:.3f})',format=yuv420p[v]")
        inputs += 2
    else:
        fc += f"[{node}]format=yuv420p[v]"
    args += ["-filter_complex", fc, "-map", "[v]", "-frames:v", str(frames)] + VENC + [out]
    run(args, f"beat {si}{bi} {os.path.basename(f)} {dur}s")
    assert abs(ff_dur(out) - dur) < 0.15, (out, ff_dur(out), dur)

# ---------------- scene clips ----------------
def make_clip(si):
    beats = SCENES[si]
    out = f"build/clip{si + 1:02d}.mp4"
    args = [FF, "-y"]
    for bi in range(len(beats)):
        args += ["-i", beat_path(si, bi)]
    n = len(beats)
    fc = ""
    if n == 1:
        fc = "[0:v]format=yuv420p[v]"
    else:
        acc = "0:v"
        acc_dur = beats[0][1]
        for k in range(1, n):
            off = acc_dur - 0.5
            nxt = f"x{k}" if k < n - 1 else "v"
            fc += (f"[{acc}][{k}:v]xfade=transition=fade:duration=0.5:"
                   f"offset={off:.3f}[{nxt}];")
            acc, acc_dur = nxt, acc_dur + beats[k][1] - 0.5
        fc = fc.rstrip(";")
    args += ["-filter_complex", fc, "-map", "[v]"] + VENC + [out]
    run(args, f"clip {si + 1}")
    assert abs(ff_dur(out) - EXPECTED[si]) < 0.2, (out, ff_dur(out), EXPECTED[si])

# ---------------- transitions + concat ----------------
def make_trans(k):
    out = f"build/trans{k + 1:02d}.mp4"
    run([FF, "-y", "-i", f"build/clip{k + 1:02d}.mp4", "-i", f"build/clip{k + 2:02d}.mp4",
         "-filter_complex",
         f"[0:v]trim=start={EXPECTED[k] - 0.5:.3f}:end={EXPECTED[k]:.3f},setpts=PTS-STARTPTS,fps=30[a];"
         f"[1:v]trim=start=0:end=0.5,setpts=PTS-STARTPTS,fps=30[b];"
         f"[a][b]xfade=transition={TRANS[k]}:duration=0.5:offset=0,format=yuv420p[v]",
         "-map", "[v]"] + VENC + [out], f"trans {k + 1}")
    assert abs(ff_dur(out) - 0.5) < 0.15, (out, ff_dur(out))

def concat_base():
    lines = []
    for k in range(8):
        lines += [f"file 'clip{k + 1:02d}.mp4'", f"file 'trans{k + 1:02d}.mp4'"]
    lines += ["file 'clip09.mp4'"]  # last scene has no trailing transition
    with open("build/concat2.txt", "w") as fh:
        fh.write("\n".join(lines) + "\n")
    run([FF, "-y", "-f", "concat", "-safe", "0", "-i", "build/concat2.txt",
         "-c", "copy", "build/base2_video.mp4"], "concat base")

def video_final():
    run([FF, "-y", "-i", "build/base2_video.mp4",
         "-vf", "fade=t=in:st=0:d=0.5,fade=t=out:st=119.35:d=0.65,format=yuv420p",
         "-an"] + VENC + ["build/base2_final.mp4"], "fades")
    run([FF, "-y", "-i", "build/base2_final.mp4",
         "-framerate", str(FPS), "-i", "build/substrack/frame_%04d.png",
         "-filter_complex",
         "[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[v]",
         "-map", "[v]"] + VENC + ["build/video_final.mp4"], "subtitles")
    assert abs(ff_dur("build/video_final.mp4") - 120.0) < 0.2

# ---------------- audio ----------------
def audio_mix():
    durs = []
    for i in range(1, 10):
        d = ff_dur(f"audio/vo{i}.mp3")
        durs.append(d)
        if i == 9:
            assert 113.6 + d / 1.03 <= 119.95, (i, d, 113.6 + d / 1.03)
        else:
            assert d <= VO_DELAYS[i] - VO_DELAYS[i - 1], (i, d)
    args = [FF, "-y"]
    for i in range(1, 10):
        args += ["-i", f"audio/vo{i}.mp3"]
    args += ["-i", "audio/music.wav", "-i", "build/sfx.wav"]
    delays = ""
    for i in range(8):
        delays += f"[{i}:a]adelay={int(VO_DELAYS[i] * 1000)}:all=1[v{i}];"
    delays += "[8:a]atempo=1.03,adelay=113600:all=1[v8];"
    fc = (delays + "".join(f"[v{i}]" for i in range(9)) +
          "amix=inputs=9:normalize=0:dropout_transition=0[voice];"
          "[9:a]volume=0.82[bed];"
          "[voice]asplit=2[vk][vv];"
          "[bed][vk]sidechaincompress=threshold=0.055:ratio=6:attack=18:release=380:makeup=1.0[duck];"
          "[vv]volume=1.28[vo2];"
          "[10:a]volume=0.85[sv];"
          "[duck][vo2][sv]amix=inputs=3:normalize=0[loud];"
          "[loud]loudnorm=I=-14:TP=-1.5:LRA=11,apad=whole_dur=120[aout]")
    args += ["-filter_complex", fc, "-map", "[aout]", "-c:a", "pcm_s16le",
             "build/final_mix2.wav"]
    run(args, "audio mix (vo+music+sfx)")
    assert abs(ff_dur("build/final_mix2.wav") - 120.0) < 0.2

def mux():
    vd = ff_dur("build/video_final.mp4")
    ad = ff_dur("build/final_mix2.wav")
    assert abs(vd - 120.0) < 0.2 and abs(ad - 120.0) < 0.2, (vd, ad)
    # no -shortest: both streams are verified 120.0s; it would silently
    # truncate any mismatch instead of failing here
    run([FF, "-y", "-i", "build/video_final.mp4", "-i", "build/final_mix2.wav",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
         "FAI_CREATE_CINEMATIC_AD_120S_1080x1920.mp4"], "mux")
    d = ff_dur("FAI_CREATE_CINEMATIC_AD_120S_1080x1920.mp4")
    assert abs(d - 120.0) < 0.2, d
    print("FINAL", d, "s")

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("all", "beats"):
        for si, beats in enumerate(SCENES):
            for bi, spec in enumerate(beats):
                render_beat(si, bi, spec)
    if mode in ("all", "clips"):
        for si in range(9):
            make_clip(si)
    if mode in ("all", "trans"):
        for k in range(8):
            make_trans(k)
        concat_base()
    if mode in ("all", "video"):
        video_final()
    if mode in ("all", "audio"):
        audio_mix()
    if mode in ("all", "mux"):
        mux()

if __name__ == "__main__":
    main()
