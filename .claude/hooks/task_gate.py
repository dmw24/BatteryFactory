#!/usr/bin/env python3
"""TaskCompleted hook for team-in-a-box (agent teams).

Blocks a build task from being marked complete unless check_command passes.
Exit code 2 sends stderr back to the agent as feedback and keeps it working.

Only tasks whose subject starts with a backlog id (e.g. "T012: ...") are gated.
Audit and housekeeping tasks pass through.

The hook input arrives as JSON on stdin. Field names can change between
Claude Code versions; this script searches defensively for the task subject.
Check the current schema in the hooks reference if gating never fires
(see references/runtime-notes.md §8 in the skill).
Checks run in the task's worktree (../wt-<id>, per the worker brief) if it
exists, otherwise in the project directory.
Set TEAM_GATE_DISABLE=1 to switch the gate off temporarily.
"""
import json
import os
import re
import subprocess
import sys

if os.environ.get("TEAM_GATE_DISABLE") == "1":
    sys.exit(0)

try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(0)  # never block on a malformed payload


def find_subject(obj):
    if isinstance(obj, dict):
        for key in ("task_subject", "subject", "title", "task_title", "content", "description"):
            v = obj.get(key)
            if isinstance(v, str) and v.strip():
                return v
        for v in obj.values():
            s = find_subject(v)
            if s:
                return s
    return None


subject = find_subject(payload) or ""
m = re.match(r"\s*(T\d{2,})\b", subject)
if not m or re.match(r"\s*(audit|review)\b", subject, re.I):
    sys.exit(0)
task_id = m.group(1)

root = payload.get("cwd") or os.getcwd()
try:
    cfg = json.load(open(os.path.join(root, "team", "config.json")))
except Exception:
    sys.exit(0)

cmd = os.environ.get("TEAM_GATE_CHECK") or cfg.get("check_command")
if not cmd:
    sys.exit(0)

wt = os.path.normpath(os.path.join(root, "..", f"wt-{task_id}"))
run_dir = wt if os.path.isdir(wt) else root

try:
    r = subprocess.run(cmd, shell=True, cwd=run_dir, capture_output=True, text=True, timeout=1800)
except subprocess.TimeoutExpired:
    print(f"{task_id}: check_command timed out; not marking complete.", file=sys.stderr)
    sys.exit(2)

if r.returncode != 0:
    tail = (r.stdout + r.stderr)[-2000:]
    print(f"{task_id} cannot be marked complete: `{cmd}` failed (exit {r.returncode}) in {run_dir}.\n"
          f"Fix the failures, or escalate in team/ESCALATIONS.md if they are outside your task.\n\n{tail}",
          file=sys.stderr)
    sys.exit(2)
sys.exit(0)

