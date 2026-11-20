#!/usr/bin/env python3
"""Lint team/tasks.json. Exits 1 if any problem is found.

Checks: required fields, valid statuses and risk levels, unique IDs,
dependencies exist, no dependency cycles, no overlapping file ownership between
active tasks, approved/merged tasks have a pass or permitted waiver (never a
waiver for high-risk tasks), acceptance criteria and boundaries present, and
tasks that need a contract (config "contracts.required_for": high_risk | all |
none) have an approved one before review.

Usage: python3 validate_tasks.py [team/tasks.json]
"""
import fnmatch
import json
import os
import sys

STATUSES = {"pending", "in_progress", "in_review", "changes_requested",
            "approved", "merged", "blocked", "escalated"}
ACTIVE = {"in_progress", "in_review", "changes_requested"}
REQUIRED = ("id", "title", "files", "depends_on", "acceptance", "status")


def overlaps(a, b):
    for x in a:
        for y in b:
            if x == y or fnmatch.fnmatch(x, y) or fnmatch.fnmatch(y, x):
                return True
            px, py = x.split("*")[0], y.split("*")[0]
            if px and py and (px.startswith(py) or py.startswith(px)):
                return True
    return False


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "team/tasks.json"
    data = json.load(open(path))
    tasks = data.get("tasks", [])
    cfg_path = os.path.join(os.path.dirname(os.path.abspath(path)), "config.json")
    cfg = json.load(open(cfg_path)) if os.path.exists(cfg_path) else {}
    need = (cfg.get("contracts") or {}).get("required_for", "high_risk")
    errors = []
    ids = [t.get("id") for t in tasks]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        errors.append(f"duplicate ids: {sorted(dupes)}")
    by_id = {t.get("id"): t for t in tasks}

    for t in tasks:
        tid = t.get("id", "?")
        for f in REQUIRED:
            if f not in t:
                errors.append(f"{tid}: missing field '{f}'")
        if t.get("status") not in STATUSES:
            errors.append(f"{tid}: invalid status '{t.get('status')}'")
        if not t.get("acceptance"):
            errors.append(f"{tid}: no acceptance criteria")
        if not t.get("files"):
            errors.append(f"{tid}: no file boundary")
        for d in t.get("depends_on", []):
            if d not in by_id:
                errors.append(f"{tid}: depends on unknown task {d}")
        if t.get("risk", "normal") not in ("normal", "high"):
            errors.append(f"{tid}: risk must be 'normal' or 'high'")
        verdict = (t.get("audit") or {}).get("verdict")
        if t.get("status") in ("approved", "merged"):
            if verdict not in ("pass", "waived"):
                errors.append(f"{tid}: {t['status']} without verdict pass or waived")
            elif verdict == "waived" and t.get("risk") == "high":
                errors.append(f"{tid}: high-risk task cannot be waived")
        needs_contract = need == "all" or (need == "high_risk" and t.get("risk") == "high")
        if needs_contract and t.get("status") in ("in_review", "changes_requested", "approved", "merged") \
                and not (t.get("contract") or {}).get("approved"):
            errors.append(f"{tid}: past contract stage without an approved contract")
        if t.get("status") in ACTIVE and not t.get("owner"):
            errors.append(f"{tid}: active task has no owner")

    # cycles
    state = {}

    def visit(n, stack):
        if state.get(n) == 1:
            errors.append(f"dependency cycle: {' -> '.join(stack + [n])}")
            return
        if state.get(n) == 2 or n not in by_id:
            return
        state[n] = 1
        for d in by_id[n].get("depends_on", []):
            visit(d, stack + [n])
        state[n] = 2

    for i in by_id:
        visit(i, [])

    # file ownership between active tasks
    active = [t for t in tasks if t.get("status") in ACTIVE]
    for i, a in enumerate(active):
        for b in active[i + 1:]:
            if overlaps(a.get("files", []), b.get("files", [])):
                errors.append(f"{a['id']} and {b['id']} are both active with overlapping files")

    if errors:
        print("tasks.json problems:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"tasks.json OK ({len(tasks)} tasks)")


if __name__ == "__main__":
    main()

