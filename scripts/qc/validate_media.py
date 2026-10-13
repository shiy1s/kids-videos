"""Fail-closed technical QC for a HAPPY HIPPO vertical Shorts render.

This verifies media mechanics only. It does not certify character animation,
lip-sync, narration quality, story quality, or child safety; those need review.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    args = parser.parse_args()

    for binary in ("ffprobe", "ffmpeg"):
        if not shutil.which(binary):
            raise SystemExit(f"{binary.upper()}_NOT_INSTALLED")
    if not args.video.is_file() or args.video.stat().st_size == 0:
        raise SystemExit("VIDEO_MISSING_OR_EMPTY")

    result = run([
        "ffprobe", "-v", "error", "-show_streams", "-show_format",
        "-of", "json", str(args.video)
    ])
    data = json.loads(result.stdout)
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    if not video:
        raise SystemExit("VIDEO_STREAM_MISSING")
    if not audio:
        raise SystemExit("AUDIO_STREAM_MISSING")

    width, height = int(video.get("width", 0)), int(video.get("height", 0))
    if (width, height) != (1080, 1920):
        raise SystemExit(f"VIDEO_DIMENSIONS_INVALID:{width}x{height}")

    fps_text = video.get("avg_frame_rate", "0/1")
    try:
        numerator, denominator = fps_text.split("/", 1)
        fps = float(numerator) / float(denominator)
    except (ValueError, ZeroDivisionError):
        fps = 0.0
    if abs(fps - 30.0) > 0.05:
        raise SystemExit(f"VIDEO_FPS_INVALID:{fps_text}")

    duration = float(data.get("format", {}).get("duration", 0))
    if not 45 <= duration <= 60:
        raise SystemExit(f"VIDEO_DURATION_INVALID:{duration:.2f}:expected_45_to_60_seconds")

    silence = run([
        "ffmpeg", "-hide_banner", "-i", str(args.video),
        "-af", "silencedetect=noise=-50dB:d=1.6",
        "-f", "null", "-"
    ], check=False)
    if re.search(r"silence_duration:\s*(?:1\.[6-9]|[2-9]\d*(?:\.\d+)?)", silence.stderr):
        raise SystemExit("AUDIO_LONG_SILENCE_DETECTED")

    peak = run([
        "ffmpeg", "-hide_banner", "-i", str(args.video),
        "-vn", "-af", "volumedetect", "-f", "null", "-"
    ], check=False)
    match = re.search(r"max_volume:\s*(-?\d+(?:\.\d+)?) dB", peak.stderr)
    if match and float(match.group(1)) >= 0.0:
        raise SystemExit(f"AUDIO_CLIPPING_DETECTED:{match.group(1)}dB")

    print(
        f"TECHNICAL_MEDIA_VALID duration={duration:.2f} "
        f"size={width}x{height} fps={fps:.2f} audio=present "
        "note=visual_animation_and_voice_quality_require_separate_review"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
