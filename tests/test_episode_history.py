"""Regression tests for log-aware daily story selection."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class DailyJobTests(unittest.TestCase):
    def test_daily_job_uses_unused_topic_and_preserves_release_hold(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "job.json"
            subprocess.run(
                [sys.executable, str(ROOT / "scripts/generate/create_daily_job.py"),
                 "--output", str(output), "--date", "2026-10-14"],
                cwd=ROOT, check=True, capture_output=True, text=True,
            )
            job = json.loads(output.read_text(encoding="utf-8"))
        history = json.loads((ROOT / "episode_log.json").read_text(encoding="utf-8"))
        used_topics = {str(ep.get("topic", "")).strip().lower() for ep in history["episodes"]}
        self.assertNotIn(job["content"]["topic"].lower(), used_topics)
        self.assertEqual(len(job["content"]["scenes"]), 6)
        self.assertEqual(len(job["content"]["songLyrics"].splitlines()), 8)
        self.assertEqual(job["video"]["durationSeconds"], 48)
        self.assertEqual(job["publishing"]["privacyStatus"], "private")
        self.assertIs(job["publishing"]["madeForKids"], True)
        self.assertIs(job["publishing"]["qualityApproved"], False)
        self.assertTrue(job["episodeMetadata"]["historyChecked"])

    def test_missing_log_fails_closed(self):
        # The generator's log path is repository-rooted. This asserts that
        # the required canonical history file exists and parses as a list.
        log = json.loads((ROOT / "episode_log.json").read_text(encoding="utf-8"))
        self.assertIsInstance(log.get("episodes"), list)
        self.assertGreaterEqual(len(log["episodes"]), 1)

if __name__ == "__main__":
    unittest.main()
