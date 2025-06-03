from system_report.cli import main


def test_cli_runs(tmp_path, monkeypatch):
    monkeypatch.setattr('system_report.save.default_path', lambda: tmp_path / 'out.json')
    main()
    assert (tmp_path / 'out.json').exists()
