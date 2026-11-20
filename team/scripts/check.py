#!/usr/bin/env python3
"""Run the team's checks with agent-friendly output.

Runs check_command (or check_command_fast with --fast) from team/config.json,
writes the full output to team/logs/checks/<timestamp>.log, and prints only:
a one-line result, the ERROR/FAIL lines (grep-friendly), and the log path.
This keeps check output from flooding an agent's context.

TEAM_CHECK_SEED is exported to the command (defaults to the current branch
name), so a fast mode that samples can be deterministic per task and still
cover different items across tasks.

Usage: python3 team/scripts/check.py [--fast] [--max-lines N]
Exit code is the check command's exit code.
"""
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

fast = "--fast" in sys.argv
max_lines = int(sys.argv[sys.argv.index("--max-lines") + 1]) if "--max-lines" in sys.argv else 25
cfg = json.load(open("team/config.json"))
cmd = (cfg.get("check_command_fast") if fast else None) or cfg["check_command"]
mode = "fast" if fast and cfg.get("check_command_fast") else "full"

seed = os.environ.get("TEAM_CHECK_SEED")
if not seed:
    try:
        seed = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                              capture_output=True, text=True).stdout.strip() or "default"
    except Exception:
        seed = "default"
env = dict(os.environ, TEAM_CHECK_SEED=seed)

logdir = Path("team/logs/checks")
logdir.mkdir(parents=True, exist_ok=True)
stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
log = logdir / f"{stamp}-{mode}.log"

r = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)
out = (r.stdout or "") + (r.stderr or "")
log.write_text(f"$ {cmd}\n(seed={seed})\n\n{out}\nexit={r.returncode}\n")

flagged = [l for l in out.splitlines() if re.search(r"\b(ERROR|FAIL(ED|URE)?|Traceback)\b", l)]
status = "PASS" if r.returncode == 0 else "FAIL"
print(f"CHECKS {status} ({mode}, exit {r.returncode}) – full log: {log}")
if flagged:
    print(f"{len(flagged)} ERROR/FAIL lines" + (f" (first {max_lines})" if len(flagged) > max_lines else "") + ":")
    for l in flagged[:max_lines]:
        print("  " + l.strip()[:300])
elif r.returncode != 0:
    tail = [l for l in out.splitlines() if l.strip()][-10:]
    print("No ERROR/FAIL lines found; last lines of output:")
    for l in tail:
        print("  " + l.strip()[:300])
sys.exit(r.returncode)

