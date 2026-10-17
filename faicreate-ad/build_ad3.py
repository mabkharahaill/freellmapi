#!/usr/bin/env python3
"""FAI CREATE CINEMATIC AD v3 — beat-based build with real phone-UI composites.
Modes: assets? none | beats | clips | joins | concat | video | audio | mux | all

Architecture (v2's replay-free fix):
  scene clips = beats joined by 0.5s internal xfades (len = RAW[si])
  final = seg01 + blend01 + seg02 + ... + seg09  where
    seg_k = scene k minus head 0.5 (k>1) and/or tail 0.5 (k<9)
    blend_k = xfade(last 0.5 of scene k, first 0.5 of scene k+1)  -> 0.5s
  => exactly 120.0s, VO boundaries at 12/27/43/60/76/93/106/114, no replays.
"""
import os
import re
import subprocess
import sys

FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
FPS = 30
VENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", str(FPS)]
BD = "build3"
os.makedirs(BD, exist_ok=True)

VO_DELAYS = [0, 12, 27, 43, 60, 76, 93, 106, 113.6]
RAW = [12.0, 15.5, 16.5, 17.5, 16.5, 17.5, 13.5, 8.5, 6.5]

# (mode, src, dur, motion, extras)
SCENES = [
    [("cine", "video/v3_studio_wide.png", 5.0, "push", {"wm": 1}),
     ("cine", "video/v3_face_close.png", 4.5, "drift", {"wm": 1}),
     ("phone", "b1c_home", 3.5, "phone", {})],
    [("phone", "b2a_home_tap", 5.0, "phone", {}),
     ("phone", "b2b_tools", 5.0, "phone", {}),
     ("cine", "video/v3_studio_wide.png", 6.5, "drift2", {"wm": 1})],
    [("phone", "b3a_type", 5.0, "phone", {}),
     ("phone", "b3b_create", 5.0, "phone", {}),
     ("cine", "video/v3_riyadh_night.png", 7.5, "reveal", {"wm": 1})],
    [("phone", "b4a_vid", 5.0, "phone", {}),
     ("cine", "video/v3_supercar.png", 6.5, "push_fast", {"wm": 1}),
     ("cine", "video/v3_supercar.png", 7.0, "slow_push", {"wm": 1, "streak": 1})],
    [("phone", "b5a_story", 5.5, "phone", {}),
     ("cine", "video/v3_storyboard.png", 6.0, "push", {"wm": 1}),
     ("cine", "video/v3_music.png", 6.0, "drift", {"wm": 1})],
    [("phone", "b6a_ads", 5.5, "phone", {}),
     ("cine", "video/v3_perfume.png", 6.5, "push", {"wm": 1}),
     ("cine", "video/v3_face_close.png", 6.5, "drift2", {"wm": 1})],
    [("phone", "b7a_lang", 4.5, "phone", {}),
     ("cine", "video/s7b.png", 6.0, "push", {"wm": 1}),
     ("phone", "b7c_game", 4.0, "phone", {})],
    [("phone", "b8a_acct", 3.5, "phone", {}),
     ("phone", "b8b_plans_ext", 5.5, "phone", {})],
    [("cine", "video/v3_endring.png", 6.5, "slow_push", {"badge": 1})],
]
BLEND_TRANS = ["smoothleft", "fade", "smoothup", "circleopen", "fade",
               "radial", "smoothright", "fade"]


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
    return f"{BD}/b{si:02d}{bi}.mp4"


def zexpr(motion, fr):
    p = f"min(max(on/{fr},0),1)"
    if motion == "push":
        return f"1+0.09*{p}"
    if motion == "push_fast":
        return f"1+0.14*{p}"
    if motion == "slow_push":
        return f"1+0.05*{p}"
    if motion == "drift":
        return f"1+0.05*{p}"
    if motion == "drift2":
        return f"1+0.06*{p}"
    if motion == "reveal":
        return f"1.12-0.12*{p}"
    if motion == "phone":
        return f"1+0.035*{p}"
    raise ValueError(motion)


def xyexpr(motion):
    if motion == "drift":
        return ("x='iw/2-(iw/zoom)/2+10*sin(on*0.05)'",
                "y='ih/2-(ih/zoom)/2'")
    if motion == "drift2":
        return ("x='iw/2-(iw/zoom)/2-12*sin(on*0.04)'",
                "y='ih/2-(ih/zoom)/2'")
    if motion == "phone":
        return ("x='iw/2-(iw/zoom)/2+3*sin(on*0.55)'",
                "y='ih/2-(ih/zoom)/2+2*sin(on*0.37)'")
    return ("x='iw/2-(iw/zoom)/2'", "y='ih/2-(ih/zoom)/2'")


# ---------------- beats ----------------
def render_beat(si, bi, spec):
    mode, f, dur, motion, extra = spec
    out = beat_path(si, bi)
    frames = int(round(dur * FPS))
    if mode == "phone":
        args = [FF, "-y", "-framerate", str(FPS),
                "-i", f"build/comp3/{f}/frame_%04d.png"]
    else:
        args = [FF, "-y", "-loop", "1", "-framerate", str(FPS),
                "-t", f"{dur:.3f}", "-i", f]
    inputs = 1
    z = zexpr(motion, frames)
    xe, ye = xyexpr(motion)
    eqv = "eq=saturation=1.02:contrast=1.01" if mode == "phone" else "eq=saturation=1.05:contrast=1.03"
    fc = (f"[0:v]scale=1296:2304:force_original_aspect_ratio=increase,crop=1296:2304,"
          f"zoompan=z='{z}':d=1:{xe}:{ye}:s=1080x1920:fps={FPS},"
          f"{eqv},format=rgba[b];")
    node = "b"
    if extra.get("wm") and si != 8:
        args += ["-i", "build/wm_badge170.png"]
        fc += f"[{node}][{inputs}:v]overlay=48:110[{node}w];"
        node += "w"
        inputs += 1
    if extra.get("streak"):
        args += ["-i", "build/streak3.png"]
        fc += (f"[{node}][{inputs}:v]overlay=x='-2160+3240*min(max((t-0.8)/2.2,0),1)'"
               f":y=0[{node}s];")
        node += "s"
        inputs += 1
    if extra.get("badge"):
        # real FAI CREATE logo inside the neon ring (ring center 540,924 @1080p)
        args += ["-loop", "1", "-framerate", str(FPS), "-i", "build/logo_badge640.png"]
        fc += (f"[{inputs}:v]scale=440:-2,format=rgba,"
               f"fade=t=in:st=0.5:d=0.9:alpha=1[{node}l];"
               f"[{node}][{node}l]overlay=320:704[{node}g];")
        node += "g"
        inputs += 1
    if motion == "reveal":
        fc += f"[{node}]fade=t=in:st=0:d=0.45:color=black[{node}f];"
        node += "f"
    fc += f"[{node}]format=yuv420p[v]"
    args += ["-filter_complex", fc, "-map", "[v]", "-frames:v", str(frames)] + VENC + [out]
    run(args, f"beat {si}{bi} {mode}/{os.path.basename(f)} {dur}s")
    assert abs(ff_dur(out) - dur) < 0.15, (out, ff_dur(out), dur)


# ---------------- scene clips ----------------
def make_clip(si):
    beats = SCENES[si]
    out = f"{BD}/clip{si + 1:02d}.mp4"
    args = [FF, "-y"]
    for bi in range(len(beats)):
        args += ["-i", beat_path(si, bi)]
    n = len(beats)
    fc = ""
    if n == 1:
        fc = "[0:v]format=yuv420p[v]"
    else:
        acc = "0:v"
        acc_dur = beats[0][2]
        for k in range(1, n):
            off = acc_dur - 0.5
            nxt = f"x{k}" if k < n - 1 else "v"
            fc += (f"[{acc}][{k}:v]xfade=transition=fade:duration=0.5:"
                   f"offset={off:.3f}[{nxt}];")
            acc, acc_dur = nxt, acc_dur + beats[k][2] - 0.5
        fc = fc.rstrip(";")
    args += ["-filter_complex", fc, "-map", "[v]"] + VENC + [out]
    run(args, f"clip {si + 1}")
    assert abs(ff_dur(out) - RAW[si]) < 0.2, (out, ff_dur(out), RAW[si])


# ---------------- scene joins (no replay) ----------------
def make_blend(k):
    out = f"{BD}/bl{k + 1:02d}.mp4"
    run([FF, "-y", "-i", f"{BD}/clip{k + 1:02d}.mp4", "-i", f"{BD}/clip{k + 2:02d}.mp4",
         "-filter_complex",
         f"[0:v]trim=start={RAW[k] - 0.5:.3f}:end={RAW[k]:.3f},setpts=PTS-STARTPTS,fps=30[a];"
         f"[1:v]trim=start=0:end=0.5,setpts=PTS-STARTPTS,fps=30[b];"
         f"[a][b]xfade=transition={BLEND_TRANS[k]}:duration=0.5:offset=0,format=yuv420p[v]",
         "-map", "[v]"] + VENC + [out], f"blend {k + 1}")
    assert abs(ff_dur(out) - 0.5) < 0.15, (out, ff_dur(out))


def make_seg(si):
    out = f"{BD}/seg{si + 1:02d}.mp4"
    args = [FF, "-y", "-i", f"{BD}/clip{si + 1:02d}.mp4"]
    if si == 0:
        args += ["-t", f"{RAW[0] - 0.5:.3f}"]
    elif si == 8:
        args += ["-ss", "0.5"]
    else:
        args += ["-ss", "0.5", "-t", f"{RAW[si] - 1.0:.3f}"]
    args += ["-map", "0:v"] + VENC + [out]
    run(args, f"seg {si + 1}")
    want = RAW[si] - (0.5 if si > 0 else 0) - (0.5 if si < 8 else 0)
    assert abs(ff_dur(out) - want) < 0.2, (out, ff_dur(out), want)


def concat_base():
    lines = []
    for k in range(8):
        lines += [f"file 'seg{k + 1:02d}.mp4'", f"file 'bl{k + 1:02d}.mp4'"]
    lines += [f"file 'seg09.mp4'"]
    with open(f"{BD}/concat3.txt", "w") as fh:
        fh.write("\n".join(lines) + "\n")
    run([FF, "-y", "-f", "concat", "-safe", "0", "-i", f"{BD}/concat3.txt",
         "-c", "copy", f"{BD}/base3_video.mp4"], "concat base")
    d = ff_dur(f"{BD}/base3_video.mp4")
    assert abs(d - 120.0) < 0.2, d
    print("BASE VIDEO", d, "s")


# ---------------- video final ----------------
def video_final():
    run([FF, "-y", "-i", f"{BD}/base3_video.mp4",
         "-vf", "fade=t=in:st=0:d=0.5,fade=t=out:st=119.35:d=0.65,format=yuv420p",
         "-an"] + VENC + [f"{BD}/base3_final.mp4"], "fades")
    run([FF, "-y", "-i", f"{BD}/base3_final.mp4",
         "-framerate", str(FPS), "-i", "build/substrack/frame_%04d.png",
         "-filter_complex",
         "[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[v]",
         "-map", "[v]"] + VENC + [f"{BD}/video3_final.mp4"], "subtitles")
    d = ff_dur(f"{BD}/video3_final.mp4")
    assert abs(d - 120.0) < 0.2, d
    print("VIDEO FINAL", d, "s")


# ---------------- audio ----------------
def audio_mix():
    durs = []
    for i in range(1, 10):
        d = ff_dur(f"audio/vo{i}.mp3")
        durs.append(d)
        if i == 9:
            assert 113.6 + d / 1.03 <= 119.95, (i, d)
        else:
            assert d <= VO_DELAYS[i] - VO_DELAYS[i - 1], (i, d)
    args = [FF, "-y"]
    for i in range(1, 10):
        args += ["-i", f"audio/vo{i}.mp3"]
    args += ["-i", "audio/music.wav", "-i", "build/sfx3.wav"]
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
             f"{BD}/final_mix3.wav"]
    run(args, "audio mix (vo+music+sfx3)")
    d = ff_dur(f"{BD}/final_mix3.wav")
    assert abs(d - 120.0) < 0.2, d
    print("AUDIO MIX", d, "s")


def mux():
    vd = ff_dur(f"{BD}/video3_final.mp4")
    ad = ff_dur(f"{BD}/final_mix3.wav")
    assert abs(vd - 120.0) < 0.2 and abs(ad - 120.0) < 0.2, (vd, ad)
    run([FF, "-y", "-i", f"{BD}/video3_final.mp4", "-i", f"{BD}/final_mix3.wav",
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
    if mode in ("all", "joins"):
        for k in range(8):
            make_blend(k)
        for si in range(9):
            make_seg(si)
    if mode in ("all", "concat"):
        concat_base()
    if mode in ("all", "video"):
        video_final()
    if mode in ("all", "audio"):
        audio_mix()
    if mode in ("all", "mux"):
        mux()


if __name__ == "__main__":
    main()
