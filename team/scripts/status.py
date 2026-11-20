#!/usr/bin/env python3
"""Summarise team/tasks.json and apply the audit policy from team/config.json.

Usage:
  python3 status.py                 counts, ready tasks, items needing a human
  python3 status.py --ready         claimable tasks (pending, all dependencies merged)
  python3 status.py --audit-plan    for tasks in review: must the auditor review it, and why
  python3 status.py --contracts     active or ready tasks that need a contract, and its state
  python3 status.py --done          exit 0 only if every task is merged
Options: --tasks PATH  --config PATH  (defaults: team/tasks.json, team/config.json)
"""
import hashlib
import json
import sys
from collections import Counter


def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


tasks_path = arg("--tasks", "team/tasks.json")
cfg_path = arg("--config", "team/config.json")
data = json.load(open(tasks_path))
try:
    cfg = json.load(open(cfg_path))
except FileNotFoundError:
    cfg = {}
tasks = data.get("tasks", [])
by_id = {t["id"]: t for t in tasks}
limits = cfg.get("limits", {})
audit = {"rate": 0.5, "first_n": 3, "always_high_risk": True, "always_with_assumptions": True}
audit.update(cfg.get("audit", {}))


def ready(t):
    return t["status"] == "pending" and all(
        by_id.get(d, {}).get("status") == "merged" for d in t.get("depends_on", []))


def sampled(tid, rate):
    h = int(hashlib.sha1(tid.encode()).hexdigest(), 16) % 10000
    return h < rate * 10000


def audit_reason(t):
    audited = sum(1 for x in tasks if (x.get("audit") or {}).get("verdict") in ("pass", "fail", "escalate"))
    if audit["rate"] >= 1:
        return "required: tier audits every task"
    if audit.get("always_high_risk") and t.get("risk") == "high":
        return "required: high risk"
    if audit.get("always_with_assumptions") and t.get("assumptions"):
        return f"required: logged assumptions {', '.join(t['assumptions'])}"
    if audited < audit.get("first_n", 0):
        return f"required: within first {audit['first_n']} audits (calibration)"
    if (t.get("audit") or {}).get("verdict") == "fail":
        return "required: previously failed audit"
    if sampled(t["id"], audit["rate"]):
        return f"required: sampled at rate {audit['rate']}"
    return None


if "--done" in sys.argv:
    remaining = [t["id"] for t in tasks if t["status"] != "merged"]
    if not tasks:
        print("No tasks defined.")
        sys.exit(1)
    if remaining:
        print(f"Not done: {len(remaining)} tasks not merged: {', '.join(remaining[:20])}")
        sys.exit(1)
    print(f"Done: all {len(tasks)} tasks merged.")
    sys.exit(0)

if "--ready" in sys.argv:
    for t in tasks:
        if ready(t):
            print(f"{t['id']}\t{t.get('risk', 'normal')}\t{t.get('workstream', '')}\t{t['title']}")
    sys.exit(0)

if "--contracts" in sys.argv:
    need = (cfg.get("contracts") or {}).get("required_for", "high_risk")
    rows = []
    for t in tasks:
        needs = need == "all" or (need == "high_risk" and t.get("risk") == "high")
        if needs and (t["status"] == "in_progress" or ready(t)):
            c = t.get("contract") or {}
            state = "approved" if c.get("approved") else ("drafted: " + c["path"] if c.get("path") else "not drafted")
            rows.append(f"{t['id']}\t{state}\t{t['title']}")
    print("\n".join(rows) if rows else "No tasks currently need a contract.")
    sys.exit(0)

if "--audit-plan" in sys.argv:
    review = [t for t in tasks if t["status"] == "in_review"]
    if not review:
        print("No tasks in review.")
    for t in review:
        r = audit_reason(t)
        print(f"{t['id']}\t{'AUDIT' if r else 'waive if check_command passes'}\t{r or 'sampled out'}")
    sys.exit(0)

c = Counter(t["status"] for t in tasks)
print(f"Objective: {data.get('objective') or cfg.get('objective') or '(unset)'}")
print(f"Tier: {cfg.get('tier', '?')}  Profile: {cfg.get('profile', '?')}  Integration: {cfg.get('integration', '?')}")
print(f"Tasks: {len(tasks)}  " + "  ".join(f"{k}={v}" for k, v in sorted(c.items())))
r = [t for t in tasks if ready(t)]
print(f"Ready to claim: {len(r)}")
for t in r[:10]:
    print(f"  {t['id']}  {t['title']}")
attn = [t for t in tasks if t["status"] in ("blocked", "escalated")]
if attn:
    print("Needs a human:")
    for t in attn:
        print(f"  {t['id']} [{t['status']}]  {t['title']}")
maxa = limits.get("max_attempts_per_task", data.get("max_attempts_per_task", 3))
for t in tasks:
    if t.get("attempts", 0) >= maxa and t["status"] not in ("merged", "escalated"):
        print(f"  {t['id']} has reached {t['attempts']} attempts – escalate it")

