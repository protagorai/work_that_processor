# System Report

System Report is a small cross platform tool to gather information about the
current machine. It collects CPU, GPU, RAM, storage and software information
and stores it in a timestamped JSON file in the user's Downloads directory.

## Running

Install the package in editable mode and run the CLI:

```bash
pip install -e .
system-report
```

This will create or update a `system_report.json` file in your `~/Downloads`
directory.

## Tests

Unit tests are located under `system_report/tests`. Install the package and run
`pytest`:

```bash
pip install -e .
pytest -q
```

A GitHub Actions workflow in `.github/workflows/python-tests.yml` automatically
executes these tests on pushes and pull requests.
