"""Create a validated job manifest from explicit content inputs."""

from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--age-range", default="4-8")
    parser.add_argument("--language", default="English")
    parser.add_argument("--story", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    job = {
        "jobId": str(uuid.uuid4()),
        "content": {
            "topic": args.topic,
            "ageRange": args.age_range,
            "language": args.language,
            "story": args.story,
            "scenes": []
        },
        "video": {
            "width": 1080,
            "height": 1920,
            "fps": 30
        }
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(job, indent=2), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
