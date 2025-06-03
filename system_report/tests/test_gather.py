import json
from system_report import gather_all, save_report


def test_gather_all_returns_dict(monkeypatch):
    data = gather_all()
    assert isinstance(data, dict)
    assert 'cpu' in data
    assert 'storage' in data


def test_save_report(tmp_path):
    data = gather_all()
    path = tmp_path / "report.json"
    save_report(data, path)
    assert path.exists()
    with path.open() as fh:
        stored = json.load(fh)
    assert list(stored.keys())[0] == data['timestamp']
