import json
from datetime import datetime
from pathlib import Path
import platform


def default_path() -> Path:
    home = Path.home()
    if platform.system() == "Windows":
        return home / "Downloads" / "system_report.json"
    else:
        return home / "Downloads" / "system_report.json"


def save_report(data: dict, path: Path = None) -> Path:
    if path is None:
        path = default_path()
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
