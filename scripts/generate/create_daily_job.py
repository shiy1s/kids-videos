"""Create a deterministic, log-aware original HAPPY HIPPO pilot job (free tools only).

This legacy procedural worker can render previews, but it is NOT production-approved
for publishing until layered puppet animation, lip-sync, and review are verified.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
LOG_PATH = ROOT / "episode_log.json"
SIGN_OFF = "Big smiles, little steps — see you next time!"

# Original candidates. Topic + plot are both checked against the episode log.
STORIES = [
    {
        "topic": "colors",
        "title": "Bibi Finds the Blue Button",
        "plot": "A blue button rolls away during a color-sorting game; Bibi and Tiko search by color clues.",
        "structure": "mystery",
        "lesson": "Notice and name the color blue.",
        "location": "home",
        "scenes": [
            ("Bibi sees a blue button roll beneath a cushion; Tiko points in surprise.", "Oh! Where did blue go?"),
            ("Bibi and Tiko look beside yellow and red toys.", "Not red. Not yellow. Let's look!"),
            ("They search slowly and peek behind a cushion.", "Can you spot the blue button?"),
            ("Pause for the child to answer; Tiko lifts the cushion.", "There it is!"),
            ("Bibi places the blue button beside matching blue blocks.", "Blue with blue. We found it!"),
            ("Both friends wave while three blue objects gently bounce.", "Blue is our color. We looked together! " + SIGN_OFF),
        ],
        "chorus": [
            "Blue, blue, look around!",
            "Blue is what we found.",
            "Look up high, look down low,",
            "Find the blue and watch it glow.",
            "Blue, blue, point with me,",
            "Blue like sky above the tree.",
            "Blue, blue, now we know,",
            "Spot the blue before we go!",
        ],
    },
    {
        "topic": "feelings",
        "title": "Tiko's Wobbly Tower",
        "plot": "A block tower falls; Tiko feels disappointed, takes a breath, asks for help, and rebuilds calmly.",
        "structure": "mistake-and-repair",
        "lesson": "Name a feeling and take a calm breath.",
        "location": "playroom",
        "scenes": [
            ("Tiko proudly stacks blocks; the tower wobbles and falls softly.", "Oh! My tower fell down!"),
            ("Tiko's face looks sad; Bibi sits nearby kindly.", "I feel sad. Can you tell?"),
            ("Bibi models one slow gentle breath.", "Breathe in slowly. Breathe out."),
            ("Tiko tries again with a wider base and Bibi helps.", "Let's try again. Help me, please."),
            ("The tower stands; both friends smile and clap gently.", "I feel proud. We did it!"),
            ("They point to happy, sad, and calm face cards.", "Feelings have names. Breathe and try again! " + SIGN_OFF),
        ],
        "chorus": [
            "When I feel sad, I stop,",
            "Breathe in softly, then breathe out.",
            "When I need help, I can ask,",
            "Trying again is a brave task.",
            "Happy, sad, calm, and proud,",
            "Name my feelings, say them loud.",
            "Breathe in softly, breathe out slow,",
            "Little steps help feelings grow!",
        ],
    },
    {
        "topic": "counting",
        "title": "Momo's Three Little Seeds",
        "plot": "Momo drops three seeds; Bibi and Tiko help count and plant each seed in a little pot.",
        "structure": "helping-a-friend",
        "lesson": "Count from one to three.",
        "location": "garden",
        "scenes": [
            ("Momo's three seeds roll gently onto a garden mat.", "Oh, my seeds! How many?"),
            ("Bibi points to the first seed; it pops up gently.", "One little seed. Count with me!"),
            ("Tiko finds the second seed beside a pot.", "Two little seeds. One, two!"),
            ("Momo finds the third seed near a flower.", "Three little seeds. One, two, three!"),
            ("Friends plant three seeds in three small pots.", "One, two, three. We did it!"),
            ("Three sprouts sway gently while friends wave.", "We counted three seeds together! " + SIGN_OFF),
        ],
        "chorus": [
            "One little seed in the sun,",
            "Two little seeds, what fun!",
            "Three little seeds in a row,",
            "Watch our little garden grow.",
            "One, two, three, count with me,",
            "Seeds are growing happily.",
            "One, two, three, now we know,",
            "Spot three seeds before we go!",
        ],
    },
    {
        "topic": "manners",
        "title": "Bibi's Please-and-Thank-You Picnic",
        "plot": "At a picnic, Bibi forgets to ask before taking a cup, notices Tiko's feelings, then practises asking politely.",
        "structure": "mistake-and-repair",
        "lesson": "Ask politely and say thank you.",
        "location": "garden",
        "scenes": [
            ("Bibi reaches for Tiko's cup, then pauses as Tiko looks surprised.", "May I use your cup, please?"),
            ("Tiko smiles and offers the cup.", "Yes, you may. Here you go!"),
            ("Bibi takes the cup carefully with both hands.", "Thank you, Tiko!"),
            ("Tiko asks to share a napkin; Bibi offers it.", "May I share your napkin, please?"),
            ("Both friends enjoy their picnic and nod happily.", "Please is kind. Thank you is kind."),
            ("They wave beside the picnic blanket.", "Ask kindly. Say thank you! " + SIGN_OFF),
        ],
        "chorus": [
            "Please, please, may I try?",
            "Thank you, with a happy sigh.",
            "Kind words help our friends feel glad,",
            "Kind words help when days feel bad.",
            "Please when asking, thank you too,",
            "Friendly words from me to you.",
            "Please and thanks, now we know,",
            "Spot kind words before we go!",
        ],
    },
    {
        "topic": "healthy food",
        "title": "Momo's Rainbow Snack",
        "plot": "Momo wants only one color of fruit; friends make a colorful snack plate and gently explore new colors without pressure.",
        "structure": "rainy-day-game",
        "lesson": "Notice different fruit colors and try at your own pace.",
        "location": "home",
        "scenes": [
            ("Momo sees red, yellow, and green fruit on a plate.", "So many colors! Which shall I choose?"),
            ("Bibi points to a red apple slice.", "Red apple. Can you spot red?"),
            ("Tiko points to a yellow banana slice.", "Yellow banana. Here is yellow!"),
            ("Momo looks at green pear and chooses a tiny taste.", "I can try when I am ready."),
            ("Friends arrange the fruit into a rainbow.", "Different colors make a happy plate."),
            ("They smile beside the rainbow plate.", "Explore new foods at your own pace! " + SIGN_OFF),
        ],
        "chorus": [
            "Red and yellow, green and blue,",
            "Lots of colors just for you.",
            "Look and smell, then you may try,",
            "Rainbow snacks are piled up high.",
            "Choose a little, take your time,",
            "Colors make a rainbow line.",
            "Red and yellow, now we know,",
            "Spot a color before we go!",
        ],
    },
    {
        "topic": "kindness",
        "title": "The Quiet Little Wave",
        "plot": "A shy new garden friend stays quiet; Bibi and Tiko offer a gentle wave and space, and the friend joins when ready.",
        "structure": "surprise-visitor",
        "lesson": "Kindness can be gentle and give others time.",
        "location": "garden",
        "scenes": [
            ("A new little bird watches from beside a flower.", "Hello, new friend! Would you like to play?"),
            ("The bird looks shy; Bibi gives a gentle wave.", "It's okay. You can take your time."),
            ("Tiko leaves a little space beside the flower path.", "We can wait. You are safe here."),
            ("The bird gives a tiny wave back.", "A little wave is a lovely start."),
            ("The bird joins them to spot yellow flowers.", "We can be kind and go slowly."),
            ("All three wave gently to the viewer.", "Kindness gives friends room to grow! " + SIGN_OFF),
        ],
        "chorus": [
            "A little wave, a little smile,",
            "We can wait a little while.",
            "You can join when you feel ready,",
            "We can make our welcome steady.",
            "Kind words, soft steps, hearts that care,",
            "There's a little room to share.",
            "Wave hello, now we know,",
            "Spot kind hearts before we go!",
        ],
    },
]

def load_log() -> list[dict]:
    if not LOG_PATH.exists():
        raise SystemExit("EPISODE_LOG_MISSING: refusing to generate without duplicate history")
    data = json.loads(LOG_PATH.read_text(encoding="utf-8"))
    if not isinstance(data.get("episodes"), list):
        raise SystemExit("EPISODE_LOG_INVALID")
    return data["episodes"]

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--date", help="Optional YYYY-MM-DD date for deterministic tests")
    args = parser.parse_args()
    now = datetime.now(ZoneInfo("Asia/Kolkata"))
    if args.date:
        now = datetime.strptime(args.date, "%Y-%m-%d").replace(tzinfo=ZoneInfo("Asia/Kolkata"))
    date_id = now.strftime("%Y%m%d")
    log = load_log()
    used_topics = {str(e.get("topic", "")).strip().lower() for e in log}
    used_plots = {str(e.get("plot", "")).strip().lower() for e in log}
    used_titles = {str(e.get("title", "")).strip().lower() for e in log}
    candidates = [
        s for s in STORIES
        if s["topic"].lower() not in used_topics
        and s["plot"].lower() not in used_plots
        and s["title"].lower() not in used_titles
    ]
    if not candidates:
        raise SystemExit("NO_UNUSED_STORY_CANDIDATES: skip episode and alert owner")
    # Deterministic per date, but only among stories not reserved in the log.
    story = candidates[now.timetuple().tm_yday % len(candidates)]
    scenes = [{
        "sceneId": f"scene_{i:02d}",
        "order": i,
        "durationSeconds": 8,
        "visualPrompt": visual,
        "narration": narration,
        "location": story["location"],
        "motionRequired": True,
        "camera": ["wide", "close-up", "tracking", "over-shoulder", "slow-push-in", "wide"][i-1],
        "callResponsePauseSeconds": 3 if story["topic"] == "colors" and i == 3 else 0,
    } for i, (visual, narration) in enumerate(story["scenes"], start=1)]
    job = {
        "jobId": f"kids-{date_id}",
        "content": {
            "topic": story["topic"],
            "ageRange": "1-5",
            "language": "en",
            "title": story["title"],
            "story": story["plot"],
            "learningGoal": story["lesson"],
            "storyStructure": story["structure"],
            "songLyrics": "\n".join(story["chorus"]),
            "signatureSignOff": SIGN_OFF,
            "characterBible": "Bibi: mint-green bunny with teal overalls and yellow button. Tiko: peach turtle with green shell/backpack and orange cap. Momo: peach bird with lilac cap and yellow dot. See characters/character_bible.md.",
            "styleBible": "Original rounded 2D preschool puppet art, gentle saturated colors, soft shadows, layered scenery, expressive eyes. Reuse locked character assets; no copyrighted characters, logos, brands, scary imagery, violence, or dangerous instructions.",
            "scenes": scenes,
        },
        "video": {
            "width": 1080, "height": 1920, "fps": 30,
            "durationSeconds": sum(s["durationSeconds"] for s in scenes),
            "minDurationSeconds": 20, "maxDurationSeconds": 60,
        },
        "publishing": {"privacyStatus": "private", "madeForKids": True, "qualityApproved": False},
        "createdAt": now.isoformat(),
        "episodeMetadata": {
            "date": now.strftime("%Y-%m-%d"),
            "structure": story["structure"],
            "chorusLines": len(story["chorus"]),
            "historyChecked": True,
            "historyPath": "episode_log.json",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(job, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"jobId": job["jobId"], "title": story["title"], "topic": story["topic"], "historyChecked": True}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
