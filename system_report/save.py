import json
from datetime import datetime
from pathlib import Path
import platform
import os

PACKAGE_ROOT = Path(__file__).resolve().parent.parent


def default_path() -> Path:
    """Return the default path to write the system report JSON."""
    examples = PACKAGE_ROOT / "examples"
    # fall back to user Downloads directory if examples folder is not
    # writeable (e.g. when installed system-wide)
    if examples.exists() and os.access(examples, os.W_OK):
        return examples / "system_report.json"

    home = Path.home()
    return home / "Downloads" / "system_report.json"


def save_report(data: dict, path: Path = None) -> Path:
    if path is None:
        path = default_path()
    # ensure the directory exists in case the examples folder or Downloads
    # directory is missing
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        with path.open("r", encoding="utf-8") as fh:
            existing = json.load(fh)
    else:
        existing = {}
    timestamp = data.get("timestamp", datetime.utcnow().isoformat())
    existing[timestamp] = data
    with path.open("w", encoding="utf-8") as fh:
        json.dump(existing, fh, indent=2)
    return path
