"""Conservative child-content gate for generated text.

This is a deterministic pre-filter, not a substitute for a provider's safety
system or human review. It intentionally fails closed on obvious categories.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


BLOCKED = (
    "porn",
    "sexual",
    "gore",
    "suicide",
    "self-harm",
    "terrorist",
    "hate speech",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("text", type=Path)
    args = parser.parse_args()

    text = args.text.read_text(encoding="utf-8").lower()
    hits = [term for term in BLOCKED if re.search(rf"\b{re.escape(term)}\b", text)]
    if hits:
        raise SystemExit("CONTENT_REJECTED:" + ",".join(hits))

    print("CONTENT_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
