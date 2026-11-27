#!/usr/bin/env python3
"""Rebuild every supply-chain output in order (audit: committed derived files must never be stale)."""
import subprocess, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for s in ("scripts/sc_build.py", "scripts/sc_unallocated.py", "scripts/sc_benchmark.py", "scripts/sc_report.py", "scripts/sc_timeseries.py", "scripts/sc_charts.py"):
    r = subprocess.run([sys.executable, os.path.join(ROOT, s)], capture_output=True, text=True)
    print(("OK   " if r.returncode == 0 else "FAIL ") + s)
    if r.returncode:
        print(r.stderr[-2000:]); sys.exit(1)
