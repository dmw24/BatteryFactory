#!/usr/bin/env python3
"""Extract factory-researcher result objects from a workflow journal.jsonl.

Usage: python scripts/extract_journal.py <journal.jsonl> <out.json>
Writes a JSON array of the per-agent `result` objects (dropping the internal
_candidate helper key). These are then fed to orchestrator.py --load.
"""
import json
import sys


def main():
    journal, out = sys.argv[1], sys.argv[2]
    objs = []
    for line in open(journal):
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        if o.get("type") != "result":
            continue
        res = o.get("result")
        if isinstance(res, dict):
            res.pop("_candidate", None)
            objs.append(res)
    json.dump(objs, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"Extracted {len(objs)} objects -> {out}")


if __name__ == "__main__":
    main()
