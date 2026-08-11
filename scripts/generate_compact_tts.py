"""Generate compact voiced previews by removing the static tail of each beat."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np
import soundfile as sf
from generate_tts import SAMPLE_RATE, SCENES, fit_audio, parse_srt
from vieneu import Vieneu

LEAD_IN = 0.10
BETWEEN_BEATS = 0.25
REVISION = "v04"


def render_compact_scene(
    root: Path,
    scene: str,
    tts: object,
    voice_lines: list[str],
) -> Path:
    cues = parse_srt(root / "subtitles" / f"{scene}.vi.srt")
    if len(cues) != len(voice_lines):
        raise ValueError(f"{scene}: voice script and subtitle cue counts differ")

    audio_segments: list[np.ndarray] = []
    clip_ranges: list[tuple[float, float]] = []
    for index, (cue, text) in enumerate(zip(cues, voice_lines, strict=True), start=1):
        print(f"  cue {index:02d}/{len(cues):02d}: {text}", flush=True)
        generated = np.asarray(
            tts.infer(text, voice="Phạm Tuyên", style="tu_nhien"), dtype=np.float32
        ).reshape(-1)
        beat_duration = cue.end - cue.start
        available = beat_duration - LEAD_IN - BETWEEN_BEATS
        generated = fit_audio(generated, available)
        segment_duration = min(
            beat_duration,
            LEAD_IN + len(generated) / SAMPLE_RATE + BETWEEN_BEATS,
        )
        lead = np.zeros(int(LEAD_IN * SAMPLE_RATE), dtype=np.float32)
        tail_length = max(
            0,
            int(segment_duration * SAMPLE_RATE) - len(lead) - len(generated),
        )
        audio_segments.append(
            np.concatenate((lead, generated, np.zeros(tail_length, dtype=np.float32)))
        )
        clip_ranges.append((cue.start, cue.start + segment_duration))

    master_audio = np.concatenate(audio_segments)
    peak = float(np.max(np.abs(master_audio)))
    if peak > 0.94:
        master_audio *= 0.94 / peak

    audio_path = root / "assets" / "audio" / f"{scene}_vo_{REVISION}.wav"
    output_path = root / "output" / "review" / f"{scene}_preview_with_voice_{REVISION}.mp4"
    source_video = root / "output" / "review" / f"{scene}_preview.mp4"
    sf.write(audio_path, master_audio, SAMPLE_RATE, subtype="PCM_24")

    filters = []
    labels = []
    for index, (start, end) in enumerate(clip_ranges):
        label = f"v{index}"
        filters.append(f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS[{label}]")
        labels.append(f"[{label}]")
    filters.append(f"{''.join(labels)}concat=n={len(labels)}:v=1:a=0[outv]")

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(source_video),
            "-i",
            str(audio_path),
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[outv]",
            "-map",
            "1:a:0",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "23",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(output_path),
        ],
        check=True,
    )
    print(f"  duration: {len(master_audio) / SAMPLE_RATE:.2f}s", flush=True)
    return output_path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    scripts = json.loads((root / "scripts" / "tts_vi_v04.json").read_text(encoding="utf-8"))
    tts = Vieneu(backend="onnx")
    for scene, _class_name in SCENES:
        print(scene, flush=True)
        render_compact_scene(root, scene, tts, scripts[scene])


if __name__ == "__main__":
    main()
