"""Deterministic renderer entry point.

This is intentionally a small foundation. Production rendering will use
FFmpeg and real generated assets. Keep media transformation deterministic
and testable from the command line.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    raise SystemExit(
        "Renderer is not wired yet. Add the production FFmpeg pipeline before enabling publishing."
    )


if __name__ == "__main__":
    main()
