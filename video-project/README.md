# RaazNama AI — *Misr Ke Pyramids Ke 5 Hairan Kun Raaz*

Production source for the finished faceless documentary.

## Deliverable

- **Export:** `render/RaazNamaAI_Misr_Ke_Pyramids_Ke_5_Raaz_720p.mp4`
- **Format:** 1280×720, 16:9, H.264/AAC, 30 fps
- **Runtime:** 05:06
- **Captions:** burned into the video and supplied separately as `render/raaznama-pyramids-subtitles.srt`
- **Voice:** male Urdu/Hindustani narration, paced for a calm documentary delivery
- **Audio:** original low-level suspense drone under the narration; no third-party music was used

## Build

The generated stills, speech tracks and rendered media are intentionally ignored by Git because they are large. After placing them in `../video-assets/` and `audio/`, render with:

```bash
python3 video-project/make_documentary.py
```

The renderer expects the local ffmpeg binary at `.video-tools/node_modules/@ffmpeg-installer/linux-x64/ffmpeg` (or `FFMPEG_BIN` may be set to another binary). It produces the final video, subtitle assets and intermediate media under `video-project/render/`.

## Editorial guardrails

- Uses a mainstream archaeological framing: the Giza pyramids are presented as monumental royal tomb complexes, and the Great Pyramid is associated with Khufu.
- Construction logistics are presented as the subject of active research, not as proof of a supernatural explanation.
- The modern scan section says that unknown spaces have been evidenced; it does **not** claim that their purpose is known.
- The casing-stone sequence depicts the well-established white Tura-limestone exterior as a historical reconstruction.

## Research references used for the editorial framing

1. ScanPyramids Mission, *Discovery of a big void in Khufu’s Pyramid by observation of cosmic-ray muons* (Nature, 2017), https://doi.org/10.1038/nature24647
2. Mark Lehner, *The Complete Pyramids*, Thames & Hudson, 1997.
3. Harvard University Giza Project, site research archive: https://giza.fas.harvard.edu/
