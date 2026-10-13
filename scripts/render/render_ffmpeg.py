"""Render a vertical kids video from stills or a numbered frame sequence."""
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
    parser.add_argument("--music", type=Path, default=None)
    args = parser.parse_args()
    for binary in ("ffmpeg", "ffprobe"):
        if not shutil.which(binary):
            raise SystemExit(f"{binary.upper()}_NOT_INSTALLED")

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    scenes = manifest.get("scenes", [])
    if not scenes:
        raise SystemExit("SCENES_EMPTY")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    total_duration = sum(float(s["durationSeconds"]) for s in scenes)

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        concat_lines = []
        for index, scene in enumerate(scenes, start=1):
            duration = float(scene["durationSeconds"])
            audio = scene.get("audioPath")
            frame_pattern = scene.get("framePattern")
            segment = tmpdir / f"scene_{index:03d}.mp4"

            if frame_pattern:
                first = Path(frame_pattern.replace("%04d", "0000"))
                if not first.exists():
                    raise SystemExit(f"ANIMATION_FRAME_MISSING:{first}")
                video_cmd = ["ffmpeg", "-y", "-framerate", str(scene.get("frameRate", 6)),
                             "-i", frame_pattern]
            else:
                image = scene.get("assetPath")
                if not image or not Path(image).exists():
                    raise SystemExit(f"SCENE_ASSET_MISSING:{scene.get('sceneId')}")
                video_cmd = ["ffmpeg", "-y", "-loop", "1", "-i", image]

            if audio and Path(audio).exists():
                video_cmd += ["-i", audio, "-t", str(duration),
                              "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
                              "-filter_complex", "[1:a]apad,atrim=duration=" + str(duration) + ",volume=1.0[a]",
                              "-map", "0:v:0", "-map", "[a]",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                              "-c:a", "aac", "-b:a", "128k", "-pix_fmt", "yuv420p"]
            else:
                video_cmd += ["-t", str(duration),
                              "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
                              "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                              "-pix_fmt", "yuv420p"]
            video_cmd.append(str(segment))
            run(video_cmd)
            concat_lines.append(f"file '{segment.as_posix()}'")

        concat = tmpdir / "concat.txt"
        concat.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")
        joined = tmpdir / "joined.mp4"
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
             "-c:a", "aac", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(joined)])

        if args.music:
            if not args.music.exists():
                raise SystemExit(f"MUSIC_FILE_MISSING:{args.music}")
            run(["ffmpeg", "-y", "-i", str(joined), "-i", str(args.music),
                 "-t", f"{total_duration:.3f}",
                 "-filter_complex", "[0:a:0]volume=1.0[voice];[1:a:0]volume=0.12[music];"
                                   "[voice][music]amix=inputs=2:duration=first:dropout_transition=2,"
                                   "alimiter=limit=0.96,loudnorm=I=-16:TP=-1.5:LRA=11[aout]",
                 "-map", "0:v:0", "-map", "[aout]", "-c:v", "copy",
                 "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(args.output)])
        else:
            shutil.copy2(joined, args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
