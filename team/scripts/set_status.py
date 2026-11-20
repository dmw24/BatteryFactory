#!/usr/bin/env python3
"""Lead helper: python3 team/scripts/set_status.py <status> <TASK>... [--verdict v --by who --notes text]"""
import json, sys
args = sys.argv[1:]
opts = {}
for k in ("--verdict", "--by", "--notes"):
    if k in args:
        i = args.index(k); opts[k[2:]] = args[i + 1]; del args[i:i + 2]
status, ids = args[0], args[1:]
p = "team/tasks.json"; t = json.load(open(p))
for task in t["tasks"]:
    if task["id"] in ids:
        task["status"] = status
        task["owner"] = task["owner"] or "worker"
        if status == "in_progress":
            task["attempts"] += 1
        for k, v in opts.items():
            task["audit"][k] = v
json.dump(t, open(p, "w"), indent=2)
print(f"{status}: {' '.join(ids)}")
