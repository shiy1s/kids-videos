"""Validate scene ordering and basic production constraints."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    scenes = data.get("scenes", [])
    if not scenes:
        raise SystemExit("SCENES_EMPTY")

    orders = [s.get("order") for s in scenes]
    if orders != list(range(1, len(scenes) + 1)):
        raise SystemExit("SCENE_ORDER_INVALID")

    total = 0.0
    for scene in scenes:
        duration = float(scene.get("durationSeconds", 0))
        if duration < 1 or duration > 30:
            raise SystemExit(f"SCENE_DURATION_INVALID:{scene.get('sceneId')}")
        total += duration
        if not scene.get("visualPrompt") or not scene.get("narration"):
            raise SystemExit(f"SCENE_FIELDS_INVALID:{scene.get('sceneId')}")

    if total < 20 or total > 60:
        raise SystemExit(f"TOTAL_DURATION_OUT_OF_RANGE:{total}")

    print(f"SCENE_MANIFEST_VALID totalDuration={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
