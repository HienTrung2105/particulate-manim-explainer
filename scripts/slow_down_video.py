"""Kéo dài video full preview từ ~7.3 phút thành ~10 phút.

- Video: decode -> re-encode (libx264) với PTS được scale (chạy chậm).
- Audio: decode -> time-stretch giữ pitch (librosa) -> encode AAC.

Usage:
    .venv/bin/python scripts/slow_down_video.py
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np
import av

SRC = "output/review/particulate_full_preview_with_voice_v04.mp4"
DST = "output/review/particulate_full_preview_with_voice_v04_10min.mp4"

TARGET_SECONDS = 10 * 60  # 600 s


def get_duration(path: str) -> float:
    with av.open(path) as c:
        return float(c.duration / av.time_base)


def main() -> None:
    src_dur = get_duration(SRC)
    factor = src_dur / TARGET_SECONDS  # ~0.729 -> chạy chậm
    print(f"source duration = {src_dur:.2f}s ({src_dur/60:.2f} min)")
    print(f"speed factor    = {factor:.4f}")
    print(f"target duration = {TARGET_SECONDS:.2f}s (10 min)")

    # ==== AUDIO: time-stretch giữ pitch ====
    print("decoding audio ...")
    with av.open(SRC) as cin:
        astream = cin.streams.audio[0]
        ac = astream.codec_context
        sr = ac.sample_rate
        resampler = av.AudioResampler(format="fltp", layout="mono", rate=sr)
        chunks: list[np.ndarray] = []
        for frame in cin.decode(astream):
            for rf in resampler.resample(frame):
                chunks.append(rf.to_ndarray()[0].astype(np.float32))
        audio = np.concatenate(chunks) if chunks else np.zeros(sr, np.float32)
    print(f"  decoded: {audio.shape[0]/sr:.2f}s")

    import librosa

    print("time-stretching audio (giữ pitch) ...")
    y_slow = librosa.effects.time_stretch(audio, rate=factor)
    print(f"  stretched: {y_slow.shape[0]/sr:.2f}s")

    # ==== MUX ====
    print("muxing ...")
    out = av.open(DST, "w")

    aout = out.add_stream("aac", rate=sr)
    aout.layout = "mono"
    aout.bit_rate = 128_000

    with av.open(SRC) as cin:
        vstream = cin.streams.video[0]
        vs = cin.streams.video[0]
        vout = out.add_stream("libx264", rate=25)
        vout.width = vstream.codec_context.width
        vout.height = vstream.codec_context.height
        vout.pix_fmt = "yuv420p"
        vout.time_base = vs.time_base
        vout.options = {"preset": "veryfast", "crf": "18"}

        # Audio trước: ghi theo từng chunk
        frame_size = sr  # 1s
        for i in range(0, y_slow.shape[0], frame_size):
            seg = y_slow[i : i + frame_size].astype(np.float32)
            aframe = av.AudioFrame.from_ndarray(
                seg[None, :], format="fltp", layout="mono"
            )
            aframe.sample_rate = sr
            aframe.pts = i
            aframe.time_base = Fraction(1, sr)
            for pkt in aout.encode(aframe):
                out.mux(pkt)

        # Video sau: decode từng frame, scale PTS (giữ nguyên time_base gốc)
        for frame in cin.decode(vs):
            old_pts = float(frame.pts) if frame.pts is not None else 0
            new_pts = int(round(old_pts / factor))
            frame.pts = new_pts
            # frame.time_base đã là vs.time_base (1/12800) từ decoder
            for pkt in vout.encode(frame):
                out.mux(pkt)

        # flush
        for pkt in aout.encode(None):
            out.mux(pkt)
        for pkt in vout.encode(None):
            out.mux(pkt)

    out.close()

    print(f"DONE -> {DST}")
    print(f"new duration = {get_duration(DST):.2f}s ({get_duration(DST)/60:.2f} min)")


if __name__ == "__main__":
    main()
