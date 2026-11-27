#!/usr/bin/env python3
"""Lead integration: demote sources whose quote was not found on re-fetch to tier 'reported', then cap confidence
at 0.5 for rows whose status/capacity/installed/production now rest only on reported evidence; also fix S8 by
setting capacity_ref_year from the evidence's publication year (noted).
    python3 team/scripts/sc_demote.py SC001 S6l S13 ...   (no sources: only cap/fix)
"""
import json, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
task, sids = sys.argv[1], set(sys.argv[2:])
path = os.path.join(ROOT, f"data/supply_chain/patches/{task}.json")
p = json.load(open(path))
for sid in sids:
    s = p["sources"][sid]
    s["tier"] = "reported"
    s.setdefault("snippet", s.get("quote"))
    s["lead_note"] = "quote not found on re-fetch by checks/verify_quotes.py (2026-11-27); demoted to reported"
rep = {k for k, s in p["sources"].items() if s.get("tier") == "reported"}
KEY = ("status", "capacity", "installed_capacity", "production")
for r in p["rows"]:
    ev = r.get("evidence") or {}
    f = r.get("fields") or {}
    if any(k in ev and ev[k] and all(x in rep for x in ev[k]) for k in KEY) and r.get("confidence", 0) > 0.5:
        r["confidence"] = 0.5
        r["notes"] = (r.get("notes") or "") + " [lead] confidence capped at 0.5: key field rests on reported evidence."
    if f.get("capacity") is not None and f.get("capacity_ref_year") is None:
        pubs = [p["sources"][x].get("published") for x in ev.get("capacity", []) if p["sources"].get(x, {}).get("published")]
        fb = "publication-year"
        if not pubs and f.get("source_published_date"):
            pubs = [f["source_published_date"]]
        if not pubs:
            pubs = [p["sources"][x].get("accessed") for x in ev.get("capacity", []) if p["sources"].get(x, {}).get("accessed")]
            fb = "access-year (source undated)"
        if pubs:
            f["capacity_ref_year"] = int(max(pubs)[:4])
            r["notes"] = (r.get("notes") or "") + f" [lead] capacity_ref_year = {fb} fallback."
    if f.get("production") is not None and f.get("production_year") is None:
        f["production"] = None
        r["notes"] = (r.get("notes") or "") + " [lead] production dropped: no production year given."
    if f.get("installed_capacity") is not None and not f.get("installed_as_of"):
        pubs = [p["sources"][x].get("published") for x in ev.get("installed_capacity", []) if p["sources"].get(x, {}).get("published")]
        if pubs:
            f["installed_as_of"] = max(pubs)
json.dump(p, open(path, "w"), ensure_ascii=False, indent=1)
print("ok", task, len(sids), "demoted")
