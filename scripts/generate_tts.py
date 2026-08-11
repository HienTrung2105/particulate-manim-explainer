"""Generate timed Vietnamese voice-over masters and voiced review videos.

Run with the dedicated VieNeu environment::

    .venv-tts/bin/python scripts/generate_tts.py
"""

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import imageio_ffmpeg
import librosa
import numpy as np
import soundfile as sf
from vieneu import Vieneu

SAMPLE_RATE = 48_000
LEAD_IN_SECONDS = 0.20
TAIL_SECONDS = 0.30

SPEECH_REPLACEMENTS: tuple[tuple[str, str], ...] = (
    ("Part là bộ phận", "A part là một thành phần"),
    ("Hunyuan3D", "Hunyuan three D"),
    ("hướng nghiên cứu", "research direction"),
    ("cấu trúc động học", "kinematic structure"),
    ("ràng buộc chuyển động", "motion constraints"),
    ("phạm vi chuyển động", "motion range"),
    ("khớp quay", "revolute joint"),
    ("bộ phận", "part"),
    ("khớp", "joint"),
    ("trục", "axis"),
    ("hướng", "direction"),
    ("kiểu", "type"),
    ("làm cha", "is parent"),
    ("làm con", "is child"),
    ("là cha", "is parent"),
    ("là con", "is child"),
    ("bản quét 3D", "three D scan"),
    ("3D", "three D"),
    ("XYZ", "X Y Z"),
    ("MLP", "M L P"),
    ("URDF", "U R D F"),
    ("P3SAM", "P three S A M"),
    ("Figure 2", "Figure two"),
    ("Table 2", "Table two"),
)

VIETNAMESE_SPEECH_REPLACEMENTS: tuple[tuple[str, str], ...] = (
    ("PARTICULATE", "particulate"),
    ("Part là bộ phận", "Một bộ phận là thành phần"),
    ("base part", "bộ phận gốc"),
    ("3D mesh", "lưới ba chiều"),
    ("Cabinet", "chiếc tủ"),
    ("query-to-point cross-attention", "chú ý chéo từ truy vấn tới điểm"),
    ("query self-attention", "tự chú ý giữa các truy vấn"),
    ("maximum spanning arborescence", "cây bao trùm có hướng cực đại"),
    ("connected component", "thành phần liên thông"),
    ("physical plausibility", "tính hợp lý vật lý"),
    ("inter-part penetration", "hiện tượng các bộ phận xuyên vào nhau"),
    ("kinematic structure", "cấu trúc động học"),
    ("kinematic tree", "cây động học"),
    ("motion constraints", "ràng buộc chuyển động"),
    ("motion prediction", "dự đoán chuyển động"),
    ("motion range", "phạm vi chuyển động"),
    ("articulated structure", "cấu trúc khớp động"),
    ("articulated 3D object", "vật thể ba chiều có khớp động"),
    ("articulated object", "vật thể có khớp động"),
    ("articulated model", "mô hình có khớp động"),
    ("articulated asset", "tài nguyên có khớp động"),
    ("articulated parts", "các bộ phận khớp động"),
    ("part segmentation", "phân đoạn bộ phận"),
    ("part query", "truy vấn bộ phận"),
    ("point token", "mã điểm"),
    ("part token", "mã bộ phận"),
    ("point cloud", "đám mây điểm"),
    ("point prompt", "điểm gợi ý"),
    ("ground-truth", "nhãn chuẩn"),
    ("feed-forward", "truyền thẳng"),
    ("revolute joint", "khớp quay"),
    ("revolute axis", "trục quay"),
    ("revolute range", "phạm vi quay"),
    ("prismatic motion", "chuyển động tịnh tiến"),
    ("unit direction", "hướng đơn vị"),
    ("axis location", "vị trí trục"),
    ("surface normal", "pháp tuyến bề mặt"),
    ("semantic part feature", "đặc trưng ngữ nghĩa bộ phận"),
    ("physics simulator", "trình mô phỏng vật lý"),
    ("forward pass", "lượt truyền thẳng"),
    ("test time", "lúc kiểm thử"),
    ("training object", "vật thể huấn luyện"),
    ("articulation state", "trạng thái khớp động"),
    ("articulation prediction", "dự đoán khớp động"),
    ("full articulation", "toàn bộ cấu trúc khớp động"),
    ("axis estimation", "ước lượng trục"),
    ("generated assets", "tài nguyên được sinh"),
    ("generated meshes", "các lưới được sinh"),
    ("artist-created assets", "tài nguyên do họa sĩ tạo"),
    ("image-to-3D", "tạo mô hình ba chiều từ ảnh"),
    ("text-to-3D", "tạo mô hình ba chiều từ văn bản"),
    ("sim-to-real robotics", "rô bốt từ mô phỏng sang thực tế"),
    ("global shape", "hình dạng tổng thể"),
    ("semantic cues", "tín hiệu ngữ nghĩa"),
    ("decoder head", "đầu giải mã"),
    ("attention", "cơ chế chú ý"),
    ("mesh artifact", "lỗi hình học của lưới"),
    ("static 3D", "mô hình ba chiều tĩnh"),
    ("3D", "ba chiều"),
    ("parts", "các bộ phận"),
    ("part", "bộ phận"),
    ("joints", "các khớp"),
    ("joint", "khớp"),
    ("points", "các điểm"),
    ("point", "điểm"),
    ("queries", "các truy vấn"),
    ("query", "truy vấn"),
    ("inference", "suy luận"),
    ("training", "huấn luyện"),
    ("segmentation", "phân đoạn"),
    ("prediction", "dự đoán"),
    ("direction", "hướng"),
    ("axis", "trục"),
    ("range", "phạm vi"),
    ("motion", "chuyển động"),
    ("parent", "cha"),
    ("child", "con"),
    ("root", "gốc"),
    ("fixed", "cố định"),
    ("prismatic", "tịnh tiến"),
    ("revolute", "quay"),
    ("both", "kết hợp"),
    ("input", "đầu vào"),
    ("output", "đầu ra"),
    ("runtime", "thời gian chạy"),
    ("method", "phương pháp"),
    ("model", "mô hình"),
    ("network", "mạng"),
    ("object", "vật thể"),
    ("static", "tĩnh"),
    ("mesh", "lưới"),
    ("face", "mặt lưới"),
    ("type", "loại"),
    ("score", "điểm số"),
    ("dataset", "tập dữ liệu"),
    ("baseline", "phương pháp đối chứng"),
    ("limitation", "hạn chế"),
    ("paper", "bài báo"),
    ("tokens", "các mã"),
    ("token", "mã"),
    ("features", "các đặc trưng"),
    ("feature", "đặc trưng"),
    ("dimension", "số chiều"),
    ("topology", "cấu trúc liên kết"),
    ("learnable", "có thể học"),
    ("sampled", "được lấy mẫu"),
    ("sample", "lấy mẫu"),
    ("optimization", "tối ưu hóa"),
    ("prior", "thông tin tiên nghiệm"),
    ("prompt", "gợi ý"),
    ("reconstruct", "tái dựng"),
    ("category", "nhóm vật thể"),
    ("metric", "chỉ số"),
    ("comparison", "phép so sánh"),
    ("ablation", "thử nghiệm loại bỏ thành phần"),
)


@dataclass(frozen=True)
class Cue:
    start: float
    end: float
    text: str


SCENES: tuple[tuple[str, str], ...] = (
    ("s01_hook", "Scene01Hook"),
    ("s02_articulation", "Scene02Articulation"),
    ("s03_old_methods", "Scene03OldMethods"),
    ("s04_input_output", "Scene04InputOutput"),
    ("s05_pipeline", "Scene05Pipeline"),
    ("s06_segmentation", "Scene06Segmentation"),
    ("s07_joint_motion", "Scene07JointMotion"),
    ("s08_training_inference", "Scene08TrainingInference"),
    ("s09_results_applications", "Scene09ResultsApplications"),
    ("s10_conclusion", "Scene10Conclusion"),
)


def parse_timestamp(value: str) -> float:
    hours, minutes, seconds_millis = value.split(":")
    seconds, millis = seconds_millis.split(",")
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(millis) / 1000


def parse_srt(path: Path) -> list[Cue]:
    blocks = re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip())
    cues: list[Cue] = []
    for block in blocks:
        lines = block.splitlines()
        start_text, end_text = lines[1].split(" --> ")
        cues.append(
            Cue(
                start=parse_timestamp(start_text),
                end=parse_timestamp(end_text),
                text=" ".join(lines[2:]),
            )
        )
    return cues


def fit_audio(audio: np.ndarray, available_seconds: float) -> np.ndarray:
    audio = np.asarray(audio, dtype=np.float32).reshape(-1)
    max_samples = max(1, int(available_seconds * SAMPLE_RATE))
    if len(audio) <= max_samples:
        return audio
    rate = len(audio) / max_samples
    stretched = librosa.effects.time_stretch(audio, rate=rate)
    return np.asarray(stretched[:max_samples], dtype=np.float32)


def speech_text(text: str, terms: str) -> str:
    """Keep Vietnamese narration while making technical terms code-switch clearly."""

    spoken = text
    replacements = VIETNAMESE_SPEECH_REPLACEMENTS if terms == "vi" else SPEECH_REPLACEMENTS
    for source, replacement in replacements:
        spoken = re.sub(
            rf"(?<!\w){re.escape(source)}(?!\w)",
            replacement,
            spoken,
            flags=re.IGNORECASE,
        )
    return spoken


def synthesize_scene(
    tts: object,
    cues: list[Cue],
    duration: float,
    voice: str,
    pace: float,
    terms: str,
) -> np.ndarray:
    master = np.zeros(int(duration * SAMPLE_RATE), dtype=np.float32)
    for index, cue in enumerate(cues, start=1):
        spoken = speech_text(cue.text, terms)
        print(f"  cue {index:02d}/{len(cues):02d}: {spoken}", flush=True)
        generated = tts.infer(spoken, voice=voice, style="tu_nhien")
        cue_start = cue.start / pace
        cue_end = cue.end / pace
        available = cue_end - cue_start - LEAD_IN_SECONDS - TAIL_SECONDS
        generated = fit_audio(generated, available)
        start_sample = int((cue_start + LEAD_IN_SECONDS) * SAMPLE_RATE)
        end_sample = min(start_sample + len(generated), len(master))
        master[start_sample:end_sample] += generated[: end_sample - start_sample]
    peak = float(np.max(np.abs(master)))
    if peak > 0.94:
        master *= 0.94 / peak
    return master


def probe_duration(video: Path) -> float:
    import av

    with av.open(str(video)) as container:
        stream = container.streams.video[0]
        return float(stream.duration * stream.time_base)


def mux_voice(video: Path, audio: Path, output: Path, pace: float) -> None:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(video),
            "-i",
            str(audio),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-filter:v",
            f"setpts=PTS/{pace}",
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
            str(output),
        ],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--voice", default="Phạm Tuyên")
    parser.add_argument("--pace", type=float, default=1.0)
    parser.add_argument("--revision", default="v01")
    parser.add_argument("--terms", choices=("en", "vi"), default="en")
    parser.add_argument("--scene", choices=[scene for scene, _ in SCENES], action="append")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    selected = {scene for scene in args.scene} if args.scene else None
    tts = Vieneu(backend="onnx")

    for scene, _class_name in SCENES:
        if selected is not None and scene not in selected:
            continue
        subtitle = root / "subtitles" / f"{scene}.vi.srt"
        preview = root / "output" / "review" / f"{scene}_preview.mp4"
        master = root / "assets" / "audio" / f"{scene}_vo_{args.revision}.wav"
        voiced = root / "output" / "review" / f"{scene}_preview_with_voice_{args.revision}.mp4"
        source_duration = probe_duration(preview)
        duration = source_duration / args.pace
        print(
            f"{scene}: {duration:.2f}s, voice={args.voice}, pace={args.pace}",
            flush=True,
        )
        audio = synthesize_scene(
            tts,
            parse_srt(subtitle),
            duration,
            args.voice,
            args.pace,
            args.terms,
        )
        sf.write(master, audio, SAMPLE_RATE, subtype="PCM_24")
        mux_voice(preview, master, voiced, args.pace)
        print(f"  wrote {master.relative_to(root)}", flush=True)
        print(f"  wrote {voiced.relative_to(root)}", flush=True)


if __name__ == "__main__":
    main()
