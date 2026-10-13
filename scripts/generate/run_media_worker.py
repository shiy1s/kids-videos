"""Generate original 2D scene animation, narration, music, and a QC-checked preview."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

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
    frames_root = work / "frames"
    audio = work / "audio"
    artifacts = work / "artifacts"
    frames_root.mkdir(parents=True, exist_ok=True)
    audio.mkdir(parents=True, exist_ok=True)
    artifacts.mkdir(parents=True, exist_ok=True)

    for binary in ("ffmpeg", "espeak-ng"):
        if not shutil.which(binary):
            raise RuntimeError(f"{binary.upper().replace('-', '_')}_NOT_INSTALLED")

    manifest_scenes = []
    frame_rate = 6
    for scene in scenes:
        scene_id = scene["sceneId"]
        frame_dir = frames_root / scene_id
        frame_dir.mkdir(parents=True, exist_ok=True)
        duration = float(scene["durationSeconds"])
        frame_count = max(1, int(duration * frame_rate))
        for frame_no in range(frame_count):
            frame_path = frame_dir / f"frame_{frame_no:04d}.png"
            make_scene(scene, int(scene["order"]) - 1, frame_path, frame=frame_no, frame_rate=frame_rate)

        audio_path = audio / f"{scene_id}.wav"
        narration = scene["narration"].strip()
        # Keep this known free voice as a fallback, not a claim of premium TTS.
        run(["espeak-ng", "-v", "en-us+f3", "-s", "138", "-p", "70", "-a", "120",
             "-g", "3", "-w", str(audio_path), narration])

        manifest_scenes.append({
            **scene,
            "framePattern": str(frame_dir / "frame_%04d.png"),
            "frameRate": frame_rate,
            "audioPath": str(audio_path),
        })

    manifest = {"jobId": job["jobId"], "scenes": manifest_scenes}
    manifest_path = work / "scene_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    output = artifacts / "kids-video.mp4"
    music_path = audio / "gentle_background_music.wav"
    duration = sum(float(scene["durationSeconds"]) for scene in scenes)
    run(["python", "scripts/generate/soft_music.py", "--duration", str(duration),
         "--output", str(music_path)])
    run(["python", "scripts/render/render_ffmpeg.py", "--manifest", str(manifest_path),
         "--music", str(music_path), "--output", str(output)])

    run(["python", "scripts/qc/validate_media.py", str(output)])
    result = {
        "jobId": job["jobId"],
        "status": "preview_rendered",
        "stage": "technical_qc",
        "output": str(output),
        "sceneCount": len(manifest_scenes),
        "frameRate": frame_rate,
        "frameByFrameMotion": True,
        "publishingApproved": False,
        "note": "Human visual/audio review and lip-sync review are still required.",
    }
    (work / "worker_result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
