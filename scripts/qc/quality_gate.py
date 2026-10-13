"""Validate a documented human release review. Missing evidence always fails closed."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

TECHNICAL_KEYS = (
    "dimensions1080x1920", "fps30", "duration45to60Seconds", "audioPresent",
    "noClipping", "noSilenceOver1_5s", "motionBeyondZoom", "lipSyncChecked",
)
SCORE_KEYS = (
    "characterConsistency", "motionQuality", "storyOriginalityAndLearning",
    "voiceClarityAndEmotion", "childSafety", "parentSuitability",
)
REQUIRED_REVIEW_FLAGS = (
    "voiceComparedAgainstPreviousEpisode", "visualFramesReviewed",
    "audioListenedToInFull",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("review", type=Path)
    args = parser.parse_args()
    if not args.review.is_file():
        raise SystemExit("QUALITY_REVIEW_MISSING")
    review = json.loads(args.review.read_text(encoding="utf-8"))
    errors = []
    for key in TECHNICAL_KEYS:
        if review.get("technicalChecks", {}).get(key) is not True:
            errors.append(f"TECHNICAL_CHECK_FAILED:{key}")
    for key in SCORE_KEYS:
        value = review.get("scores", {}).get(key)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 8 <= value <= 10:
            errors.append(f"SCORE_BELOW_THRESHOLD_OR_MISSING:{key}")
    for key in REQUIRED_REVIEW_FLAGS:
        if review.get(key) is not True:
            errors.append(f"REVIEW_EVIDENCE_MISSING:{key}")
    if review.get("parentWouldApprove") is not True:
        errors.append("PARENT_SUITABILITY_NOT_APPROVED")
    if review.get("approvedForPublicPublishing") is not True:
        errors.append("OWNER_RELEASE_APPROVAL_MISSING")
    if not review.get("reviewer") or not review.get("reviewedAt") or not review.get("jobId"):
        errors.append("REVIEW_AUDIT_FIELDS_MISSING")
    if errors:
        print(json.dumps({"status": "blocked", "errors": errors}, indent=2))
        raise SystemExit(1)
    print(json.dumps({"status": "approved", "jobId": review["jobId"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
