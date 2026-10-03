"""Generate scene images/audio, render, and QC one Kids Video job."""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
from pathlib import Path

import requests


OPENAI_URL = "https://api.openai.com/v1"


def api_headers() -> dict[str, str]:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY_MISSING")
    return {"Authorization": f"Bearer {key}"}


def generate_image(prompt: str, output: Path) -> None:
    payload = {
        "model": os.environ.get("KIDS_IMAGE_MODEL", "gpt-image-1-mini"),
        "prompt": prompt,
        "size": "1024x1536",
        "quality": os.environ.get("KIDS_IMAGE_QUALITY", "medium"),
    }
    response = requests.post(
        f"{OPENAI_URL}/images/generations",
        headers={**api_headers(), "Content-Type": "application/json"},
        json=payload,
        timeout=300,
    )
    response.raise_for_status()
    data = response.json()["data"][0]
    encoded = data.get("b64_json")
    if not encoded:
        raise RuntimeError("IMAGE_RESPONSE_MISSING_B64")
    output.write_bytes(base64.b64decode(encoded))


def generate_audio(text: str, output: Path) -> None:
    payload = {
        "model": os.environ.get("KIDS_TTS_MODEL", "gpt-4o-mini-tts"),
        "input": text,
        "voice": os.environ.get("KIDS_TTS_VOICE", "alloy"),
        "response_format": "mp3",
    }
    response = requests.post(
        f"{OPENAI_URL}/audio/speech",
        headers={**api_headers(), "Content-Type": "application/json"},
        json=payload,
        timeout=180,
    )
    response.raise_for_status()
    output.write_bytes(response.content)


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

    character_bible = job["content"].get("characterBible", "")
    style_bible = job["content"].get(
        "styleBible",
        "original child-friendly 2D cartoon, clean shapes, bright but gentle colors, soft lighting",
    )

    manifest_scenes = []
    for scene in scenes:
        scene_id = scene["sceneId"]
        visual_prompt = (
            f"{style_bible}. "
            f"Character continuity: {character_bible}. "
            f"Scene: {scene['visualPrompt']}. "
            "Original characters only. No copyrighted characters, logos, brands, or frightening imagery. "
            "No readable text in the image. Vertical composition with clear foreground and background."
        )
        image_path = images / f"{scene_id}.png"
        audio_path = audio / f"{scene_id}.mp3"
        generate_image(visual_prompt, image_path)
        generate_audio(scene["narration"], audio_path)
        manifest_scenes.append({
            **scene,
            "assetPath": str(image_path),
            "audioPath": str(audio_path),
        })

    manifest = {"jobId": job["jobId"], "scenes": manifest_scenes}
    manifest_path = work / "scene_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    output = artifacts / "kids-video.mp4"
    subprocess.run([
        "python", "scripts/render/render_ffmpeg.py",
        "--manifest", str(manifest_path),
        "--output", str(output),
    ], check=True)

    subprocess.run([
        "python", "scripts/qc/validate_media.py", str(output),
    ], check=True)

    result = {
        "jobId": job["jobId"],
        "status": "success",
        "stage": "render_qc",
        "output": str(output),
        "sceneCount": len(manifest_scenes),
    }
    (work / "worker_result.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
