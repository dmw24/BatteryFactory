#!/usr/bin/env python3
"""Total spend recorded in headless run logs and compare with the budget.

Scans team/logs/*.jsonl for result messages (stream-json output of claude -p)
and sums "total_cost_usd" and token usage. Field names can change between
Claude Code versions: if totals are zero after a real run, inspect a log's last
line and adjust. Interactive and cloud runs aren't logged here; the lead records
their spend in PROGRESS.md (see runtime-notes.md §9).

Usage: python3 spend.py [--config team/config.json] [--logs team/logs]
Exit 1 if a configured budget is exceeded.
"""
import json
import sys
from pathlib import Path


def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


cfg = json.load(open(arg("--config", "team/config.json")))
limits = cfg.get("limits", {})
usd, tokens, runs = 0.0, 0, 0
for f in sorted(Path(arg("--logs", "team/logs")).glob("*.jsonl")):
    for line in f.read_text(errors="ignore").splitlines():
        try:
            m = json.loads(line)
        except json.JSONDecodeError:
            continue
        if m.get("type") != "result":
            continue
        runs += 1
        usd += float(m.get("total_cost_usd") or m.get("cost_usd") or 0)
        u = m.get("usage") or {}
        tokens += sum(int(u.get(k) or 0) for k in (
            "input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))

bu, bt = limits.get("budget_usd"), limits.get("budget_tokens")
print(f"Spend: ${usd:,.2f}" + (f" of ${bu:,.2f}" if bu else "") +
      f" · {tokens:,} tokens" + (f" of {bt:,}" if bt else "") + f" · {runs} runs")
over = (bu is not None and usd >= bu) or (bt is not None and tokens >= bt)
if over:
    print("BUDGET EXCEEDED – stop and report.")
sys.exit(1 if over else 0)

