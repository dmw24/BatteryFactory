#!/usr/bin/env python3
"""Full v2 pipeline in the right order (checks/run_all.py rebuilds factories.db and drops derived tables):

    python3 scripts/build_all.py

rebuild -> time series (A-D) -> unallocated company capacity (E) -> QA report -> HTML report -> v2 charts.
"""
import subprocess
import sys

STEPS = ["scripts/rebuild.py", "scripts/build_timeseries.py", "scripts/build_unallocated.py", "scripts/build_history_model.py", "scripts/build_utilisation.py", "scripts/build_ownership.py", "scripts/qa.py",
         "scripts/build_report.py", "scripts/make_v2_charts.py"]
for s in STEPS:
    r = subprocess.run([sys.executable, s], capture_output=True, text=True)
    print(f"{'OK  ' if r.returncode == 0 else 'FAIL'} {s}")
    if r.returncode:
        print(r.stderr[-2000:]); sys.exit(1)
