"""
Integration tests that actually run the pipeline scripts end to end, the way
a real user would, rather than just unit-testing their internal functions.

Both scripts are run as subprocesses inside a clean temporary directory that
contains nothing but a copy of the source files and the sample CSV -- no
.env file, so both scripts must fall back to a fresh local SQLite database
on their own, exactly like a first-time clone would.
"""
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent
SOURCE_FILES = ["esg_parser.py", "esg_analytics.py", "esg_ingestion.py"]
DATA_FILE = "company_esg_financial_dataset_sample.csv"


@pytest.fixture
def clean_project_dir(tmp_path):
    for filename in SOURCE_FILES + [DATA_FILE]:
        shutil.copy(REPO_ROOT / filename, tmp_path / filename)
    return tmp_path


def _run_script(script_name, cwd):
    return subprocess.run(
        [sys.executable, script_name],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )


def test_esg_analytics_runs_clean_on_fresh_clone(clean_project_dir):
    result = _run_script("esg_analytics.py", clean_project_dir)
    assert result.returncode == 0, f"stdout:\n{result.stdout}\n\nstderr:\n{result.stderr}"
    assert "PIPELINE PROCESS COMPLETION: STATUS 0 [SUCCESS]" in result.stdout


def test_esg_ingestion_runs_clean_on_fresh_clone_with_no_env(clean_project_dir):
    result = _run_script("esg_ingestion.py", clean_project_dir)
    assert result.returncode == 0, f"stdout:\n{result.stdout}\n\nstderr:\n{result.stderr}"
    assert "LOCAL ENGINE" in result.stdout
    assert "PIPELINE RUN COMPLETION: STATUS 0 [SUCCESS]" in result.stdout

    db_path = clean_project_dir / "local_portfolio.db"
    assert db_path.exists(), "expected local_portfolio.db to be created by the SQLite fallback"

    conn = sqlite3.connect(db_path)
    try:
        total_rows = conn.execute("SELECT COUNT(*) FROM esg_financials_raw").fetchone()[0]
        # The source sample has 100 rows across 10 companies x 10-11 years
        # each. If CompanyID alone were used as the key, every later year
        # would overwrite the earlier one and this would collapse to ~10.
        assert total_rows == 100, f"expected all 100 source rows to survive, found {total_rows}"

        distinct_companies = conn.execute("SELECT COUNT(DISTINCT CompanyID) FROM esg_financials_raw").fetchone()[0]
        assert distinct_companies < total_rows, "expected multiple years per company, not one row per company"

        # The ESG/environmental columns must actually be loaded, not dropped.
        esg_value = conn.execute(
            "SELECT ESG_Overall, CarbonEmissions FROM esg_financials_raw WHERE CompanyID='1' AND Year=2015"
        ).fetchone()
        assert esg_value is not None
        assert esg_value[0] is not None, "ESG_Overall should be populated, not dropped during ingestion"
        assert esg_value[1] is not None, "CarbonEmissions should be populated, not dropped during ingestion"
    finally:
        conn.close()


def test_esg_ingestion_is_idempotent(clean_project_dir):
    first = _run_script("esg_ingestion.py", clean_project_dir)
    assert first.returncode == 0, first.stderr
    second = _run_script("esg_ingestion.py", clean_project_dir)
    assert second.returncode == 0, second.stderr

    db_path = clean_project_dir / "local_portfolio.db"
    conn = sqlite3.connect(db_path)
    try:
        total_rows = conn.execute("SELECT COUNT(*) FROM esg_financials_raw").fetchone()[0]
        assert total_rows == 100, "running the pipeline twice should not duplicate rows"
    finally:
        conn.close()
