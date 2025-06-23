import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_cli_starts(tmp_path, monkeypatch):
    """
    Copies the scraper into a temp dir, injects a bogus NASA_KEY
    so requests fail fast with 401, and asserts non-zero exit.
    """
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data").mkdir()
    (tmp_path / "db").mkdir()
    monkeypatch.setenv("NASA_KEY", "BAD_KEY")

    scraper_src = ROOT / "src" / "firms_scraper.py"
    target = tmp_path / "firms_scraper.py"
    target.write_bytes(scraper_src.read_bytes())

    completed = subprocess.run(
        [sys.executable, target],
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    assert "NASA_KEY" not in completed.stdout  # secrecy check
