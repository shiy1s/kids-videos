"""Basic configuration sanity checks."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    for rel in ("config/video_defaults.json", "config/content_policy.json"):
        path = ROOT / rel
        with path.open("r", encoding="utf-8") as fh:
            json.load(fh)
    print("Configuration JSON OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
