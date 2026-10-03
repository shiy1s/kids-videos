"""Build a deterministic scene manifest from JSON scene definitions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    scenes = data.get("scenes", [])
    if not scenes:
        raise SystemExit("No scenes supplied")

    normalized = []
    for index, scene in enumerate(scenes, start=1):
        if not scene.get("visualPrompt") or not scene.get("narration"):
            raise SystemExit(f"Scene {index} is missing visualPrompt or narration")
        normalized.append({
            "sceneId": str(scene.get("sceneId", f"scene_{index:02d}")),
            "order": index,
            "durationSeconds": float(scene.get("durationSeconds", 5)),
            "visualPrompt": scene["visualPrompt"].strip(),
            "narration": scene["narration"].strip(),
            "assetPath": scene.get("assetPath"),
            "audioPath": scene.get("audioPath")
        })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps({"scenes": normalized}, indent=2),
        encoding="utf-8",
    )
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
