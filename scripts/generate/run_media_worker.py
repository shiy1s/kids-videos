"""Generate original cartoon assets locally, render, and QC a Kids Video job.

No paid AI API is used. Images are procedural Pillow artwork and narration uses
the open-source espeak-ng command installed on the GitHub runner.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

# When this file is executed directly, Python starts with scripts/generate on sys.path.
# Add the repository root so the worker can import its sibling package reliably.
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.generate.procedural_assets import make_scene


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    job = json.loads(args.job_json.read_text(encoding="utf-8"))
    scenes = job["content"]["scenes"]
    work = args.output_dir
    images = work / "images"
    audio = work / "audio"
    artifacts = work / "artifacts"
    images.mkdir(parents=True, exist_ok=True)
    audio.mkdir(parents=True, exist_ok=True)
    artifacts.mkdir(parents=True, exist_ok=True)

    if not shutil.which("ffmpeg"):
        raise RuntimeError("FFMPEG_NOT_INSTALLED")
    if not shutil.which("espeak-ng"):
        raise RuntimeError("ESPEAK_NG_NOT_INSTALLED")

    manifest_scenes = []
    for scene in scenes:
        scene_id = scene["sceneId"]
        image_path = images / f"{scene_id}.png"
        audio_path = audio / f"{scene_id}.wav"

        make_scene(scene, int(scene["order"]) - 1, image_path)

        narration = scene["narration"].strip()
        run([
            "espeak-ng", "-s", "145", "-p", "55", "-a", "145",
            "-w", str(audio_path), narration,
        ])

        manifest_scenes.append({
            **scene,
            "assetPath": str(image_path),
            "audioPath": str(audio_path),
        })

    manifest = {"jobId": job["jobId"], "scenes": manifest_scenes}
    manifest_path = work / "scene_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    output = artifacts / "kids-video.mp4"
    run([
        "python", "scripts/render/render_ffmpeg.py",
        "--manifest", str(manifest_path),
        "--output", str(output),
    ])

    run(["python", "scripts/qc/validate_media.py", str(output)])

    result = {
        "jobId": job["jobId"],
        "status": "success",
        "stage": "render_qc",
        "output": str(output),
        "sceneCount": len(manifest_scenes),
    }
    (work / "worker_result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
