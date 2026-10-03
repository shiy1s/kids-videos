"""Create one deterministic, original child-directed job for the daily Kids Video pipeline."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

STORIES = [
    {
        "topic": "Kindness",
        "title": "Milo and Pip Learn to Share",
        "story": "Milo and Pip discover that sharing makes playtime happier for everyone.",
        "scenes": [
            ("A sunny garden with two original cartoon friends.", "Milo and Pip begin a happy adventure."),
            ("Two original cartoon friends notice a colorful ball.", "They find a ball and decide to play together."),
            ("Two original cartoon friends take turns with a ball.", "They take turns and learn that sharing is fun."),
            ("Two original cartoon friends help each other after a ball rolls away.", "They help each other when the ball rolls away."),
            ("Two original cartoon friends celebrate teamwork.", "They smile because teamwork made the problem easy."),
            ("Two original cartoon friends wave goodbye under soft stars.", "They wave goodbye and remember to be kind and share."),
        ],
    },
    {
        "topic": "Helping",
        "title": "Milo and Pip Help a Little Bird",
        "story": "Milo and Pip work together to help a little bird find its way back to a safe tree.",
        "scenes": [
            ("A bright garden where two original cartoon friends hear a gentle chirp.", "Milo and Pip hear a little bird nearby."),
            ("Two original cartoon friends look around a sunny garden.", "They look carefully and find the bird on the ground."),
            ("Two original cartoon friends point toward a safe low tree branch.", "They guide the bird toward a safe branch."),
            ("Two original cartoon friends work together beside a tree.", "They stay calm and help each other."),
            ("A little bird rests safely on a tree branch while two friends smile.", "The bird reaches the branch and feels safe."),
            ("Two original cartoon friends wave beside the tree at sunset.", "Milo and Pip learn that helping others feels good."),
        ],
    },
    {
        "topic": "Patience",
        "title": "Milo and Pip Practice Patience",
        "story": "Milo and Pip learn that waiting calmly can make a tricky activity easier.",
        "scenes": [
            ("Two original cartoon friends sit in a sunny garden beside a small puzzle.", "Milo and Pip find a little puzzle to solve."),
            ("Two original cartoon friends try to fit a puzzle piece.", "They try a piece, but it does not fit."),
            ("Two original cartoon friends pause and look carefully at the puzzle.", "Instead of rushing, they stop and look again."),
            ("Two original cartoon friends take turns trying puzzle pieces.", "They take turns and stay patient."),
            ("Two original cartoon friends complete a simple puzzle together.", "At last, the pieces fit together."),
            ("Two original cartoon friends celebrate under a soft evening sky.", "They learn that patience can help us solve problems."),
        ],
    },
    {
        "topic": "Honesty",
        "title": "Milo and Pip Tell the Truth",
        "story": "Milo and Pip learn that telling the truth helps friends solve small mistakes together.",
        "scenes": [
            ("Two original cartoon friends play near a cozy home.", "Milo and Pip are happily playing together."),
            ("A small toy sits beside two original cartoon friends.", "A toy falls down while they are playing."),
            ("Two original cartoon friends look at the fallen toy.", "Milo admits that he bumped the toy by accident."),
            ("Two original cartoon friends carefully pick up the toy together.", "Pip thanks Milo for telling the truth and helps fix it."),
            ("Two original cartoon friends smile beside the repaired toy.", "They discover that honesty makes it easier to solve mistakes."),
            ("Two original cartoon friends wave goodbye beside their home.", "They remember to tell the truth and help each other."),
        ],
    },
    {
        "topic": "Teamwork",
        "title": "Milo and Pip Build Together",
        "story": "Milo and Pip discover that teamwork helps them build something neither could make alone.",
        "scenes": [
            ("Two original cartoon friends stand beside colorful building blocks.", "Milo and Pip decide to build something together."),
            ("Two original cartoon friends sort colorful blocks.", "They sort the blocks and make a simple plan."),
            ("Two original cartoon friends build a small tower.", "They take turns adding blocks to the tower."),
            ("Two original cartoon friends steady a wobbly tower together.", "When the tower wobbles, they help each other."),
            ("Two original cartoon friends admire their finished block tower.", "Their teamwork creates a cheerful little tower."),
            ("Two original cartoon friends wave beside the finished tower.", "They learn that working together can make big ideas possible."),
        ],
    },
    {
        "topic": "Caring",
        "title": "Milo and Pip Care for a Garden",
        "story": "Milo and Pip care for a small garden and learn that gentle attention helps things grow.",
        "scenes": [
            ("Two original cartoon friends discover a small sunny garden.", "Milo and Pip find a garden that needs some care."),
            ("Two original cartoon friends gently water small flowers.", "They gently water the flowers."),
            ("Two original cartoon friends remove a few leaves from a garden path.", "They carefully tidy the garden path."),
            ("Two original cartoon friends place a small sign beside the flowers.", "They make a friendly reminder to care for the plants."),
            ("Two original cartoon friends admire fresh flowers in the garden.", "The garden looks bright and cheerful."),
            ("Two original cartoon friends wave beside the garden at sunset.", "They learn that caring for small things can make a big difference."),
        ],
    },
]

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    now = datetime.now(ZoneInfo("Asia/Kolkata"))
    date_id = now.strftime("%Y%m%d")
    story = STORIES[now.timetuple().tm_yday % len(STORIES)]
    scenes = [
        {
            "sceneId": f"scene_{i:02d}",
            "order": i,
            "durationSeconds": 6,
            "visualPrompt": visual,
            "narration": narration,
        }
        for i, (visual, narration) in enumerate(story["scenes"], start=1)
    ]

    job = {
        "jobId": f"kids-{date_id}",
        "content": {
            "topic": story["topic"],
            "ageRange": "3-7",
            "language": "en",
            "title": story["title"],
            "story": story["story"],
            "characterBible": "Milo is an original green round-eared friend. Pip is an original blue round-eared friend.",
            "styleBible": "Original simple 2D geometric children cartoon, gentle colors, friendly expressions, no copyrighted characters, logos, brands, scary imagery, violence, sexual content, hate, or dangerous instructions.",
            "scenes": scenes,
        },
        "video": {
            "width": 1080,
            "height": 1920,
            "fps": 30,
            "durationSeconds": 36,
            "minDurationSeconds": 20,
            "maxDurationSeconds": 60,
        },
        "publishing": {
            "privacyStatus": "private",
            "madeForKids": True,
        },
        "createdAt": now.isoformat(),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(job, indent=2), encoding="utf-8")
    print(json.dumps({"jobId": job["jobId"], "title": story["title"], "topic": story["topic"]}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
