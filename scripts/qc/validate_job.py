"""Validate the job manifest without external dependencies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("job", type=Path)
    args = parser.parse_args()

    data = json.loads(args.job.read_text(encoding="utf-8"))
    for key in ("jobId", "content", "video"):
        if key not in data:
            raise SystemExit(f"Missing required field: {key}")

    for key in ("topic", "ageRange", "language", "story"):
        if not data["content"].get(key):
            raise SystemExit(f"Missing content field: {key}")

    for key in ("width", "height", "fps"):
        if int(data["video"].get(key, 0)) <= 0:
            raise SystemExit(f"Invalid video field: {key}")

    print("JOB_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
