"""Validate a rendered video with ffprobe.

The worker fails closed if ffprobe is unavailable or the media does not meet
the configured vertical-video requirements.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    args = parser.parse_args()

    if not shutil.which("ffprobe"):
        raise SystemExit("FFPROBE_NOT_INSTALLED")

    cmd = [
        "ffprobe", "-v", "error", "-show_streams", "-show_format",
        "-of", "json", str(args.video)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)

    video = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
    if not video:
        raise SystemExit("VIDEO_STREAM_MISSING")

    width = int(video.get("width", 0))
    height = int(video.get("height", 0))
    if width != 1080 or height != 1920:
        raise SystemExit(f"VIDEO_DIMENSIONS_INVALID:{width}x{height}")

    duration = float(data.get("format", {}).get("duration", 0))
    if duration < 20 or duration > 60:
        raise SystemExit(f"VIDEO_DURATION_INVALID:{duration}")

    print(f"MEDIA_VALID duration={duration:.2f} size={width}x{height}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
