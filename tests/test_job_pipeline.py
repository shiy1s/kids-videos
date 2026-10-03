import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_create_and_validate_job(tmp_path):
    job = tmp_path / "job.json"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/generate/create_job.py"),
            "--topic", "A friendly little cloud",
            "--story", "A cloud learns to help flowers grow.",
            "--output", str(job),
        ],
        check=True,
    )
    data = json.loads(job.read_text())
    assert data["video"]["width"] == 1080

    subprocess.run(
        [sys.executable, str(ROOT / "scripts/qc/validate_job.py"), str(job)],
        check=True,
    )
