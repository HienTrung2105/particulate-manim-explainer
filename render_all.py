"""Discover and render implemented Manim scenes in filename/class order."""

from __future__ import annotations

import argparse
import ast
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from config import FINAL_FRAME_RATE, FINAL_PIXEL_HEIGHT, FINAL_PIXEL_WIDTH

PROJECT_ROOT = Path(__file__).resolve().parent
SCENES_DIR = PROJECT_ROOT / "scenes"
MEDIA_DIR = PROJECT_ROOT / "output" / "manim"
SCENE_BASES = {"Scene", "MovingCameraScene", "ThreeDScene", "ZoomedScene"}


@dataclass(frozen=True)
class SceneSpec:
    path: Path
    class_name: str


def _base_name(node: ast.expr) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def discover_scenes(*, exclude_smoke: bool = False) -> list[SceneSpec]:
    """Find concrete scene classes without importing or executing scene files."""

    discovered: list[SceneSpec] = []
    for path in sorted(SCENES_DIR.glob("*.py")):
        if path.name == "__init__.py" or (exclude_smoke and "smoke" in path.stem):
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            if any(_base_name(base) in SCENE_BASES for base in node.bases):
                discovered.append(SceneSpec(path=path, class_name=node.name))
    return discovered


def quality_args(quality: str) -> list[str]:
    if quality == "final":
        return [
            "-qh",
            "-r",
            f"{FINAL_PIXEL_WIDTH},{FINAL_PIXEL_HEIGHT}",
            "--fps",
            str(FINAL_FRAME_RATE),
        ]
    return {"low": ["-ql"], "medium": ["-qm"], "high": ["-qh"]}[quality]


def _newest_video_for(scene: SceneSpec) -> Path:
    candidates = list(MEDIA_DIR.rglob(f"{scene.class_name}.mp4"))
    if not candidates:
        raise FileNotFoundError(f"No rendered video found for {scene.class_name}")
    return max(candidates, key=lambda path: path.stat().st_mtime_ns)


def render_scenes(scenes: list[SceneSpec], quality: str) -> list[Path]:
    rendered: list[Path] = []
    for index, scene in enumerate(scenes, start=1):
        print(f"[{index}/{len(scenes)}] Rendering {scene.class_name} ({scene.path.name})")
        command = [
            sys.executable,
            "-m",
            "manim",
            *quality_args(quality),
            "--renderer=cairo",
            "--media_dir",
            str(MEDIA_DIR),
            str(scene.path),
            scene.class_name,
        ]
        subprocess.run(command, cwd=PROJECT_ROOT, check=True)
        rendered.append(_newest_video_for(scene))
    return rendered


def _ffmpeg_path(path: Path) -> str:
    normalized = path.resolve().as_posix()
    return normalized.replace("'", "'\\''")


def concatenate_videos(videos: list[Path], output_file: Path) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError(
            "FFmpeg CLI is not installed or not on PATH. "
            "Install it before using --concat."
        )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    concat_list = output_file.parent / "concat.txt"
    concat_list.write_text(
        "\n".join(f"file '{_ffmpeg_path(video)}'" for video in videos) + "\n",
        encoding="utf-8",
    )
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
            "-c",
            "copy",
            str(output_file),
        ],
        cwd=PROJECT_ROOT,
        check=True,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--quality",
        choices=("low", "medium", "high", "final"),
        default="low",
    )
    parser.add_argument(
        "--exclude-smoke",
        action="store_true",
        help="Skip files whose name contains 'smoke'.",
    )
    parser.add_argument(
        "--concat",
        action="store_true",
        help="Concatenate rendered scenes with the external FFmpeg CLI.",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=PROJECT_ROOT / "output" / "particulate_final.mp4",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    scenes = discover_scenes(exclude_smoke=args.exclude_smoke)
    if not scenes:
        print("No implemented Manim Scene classes were found.", file=sys.stderr)
        return 1

    videos = render_scenes(scenes, args.quality)
    if args.concat:
        concatenate_videos(videos, args.output_file)
        print(f"Combined video: {args.output_file.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

