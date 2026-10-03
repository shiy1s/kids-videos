"""Render a vertical kids-video from prepared scene images and optional narration audio."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    for binary in ("ffmpeg", "ffprobe"):
        if not shutil.which(binary):
            raise SystemExit(f"{binary.upper()}_NOT_INSTALLED")

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    scenes = manifest.get("scenes", [])
    if not scenes:
        raise SystemExit("SCENES_EMPTY")

    args.output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        concat_lines = []

        for index, scene in enumerate(scenes, start=1):
            image = scene.get("assetPath")
            if not image or not Path(image).exists():
                raise SystemExit(f"SCENE_ASSET_MISSING:{scene.get('sceneId')}")

            duration = float(scene["durationSeconds"])
            audio = scene.get("audioPath")
            segment = tmpdir / f"scene_{index:03d}.mp4"

            video_cmd = [
                "ffmpeg", "-y", "-loop", "1", "-i", image,
                "-t", str(duration),
                "-vf",
                "scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920,"
                "zoompan=z='min(zoom+0.0008,1.08)':"
                "d=1:s=1080x1920:fps=30",
            ]

            if audio and Path(audio).exists():
                video_cmd += [
                    "-i", audio,
                    "-filter_complex", "[1:a]apad[a]",
                    "-map", "0:v:0", "-map", "[a]",
                    "-t", str(duration),
                    "-c:v", "libx264", "-c:a", "aac",
                    "-b:a", "128k", "-pix_fmt", "yuv420p",
                ]
            else:
                video_cmd += ["-an", "-c:v", "libx264", "-pix_fmt", "yuv420p"]

            video_cmd.append(str(segment))
            run(video_cmd)
            concat_lines.append(f"file '{segment.as_posix()}'")

        concat = tmpdir / "concat.txt"
        concat.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")

        run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat),
            "-c:v", "libx264", "-c:a", "aac",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(args.output)
        ])

    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
