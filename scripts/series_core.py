"""Per-plant capacity series, v3 rules (T102 audit, 2026-11-24). Used by build_timeseries.py.

Evidence precedence (never let older or weaker data outrank newer research):
  1. installed anchor (installed_capacity_gwh @ installed_as_of), tier from field evidence;
  2. v2 dated steps (capacity_by_year_json), tier from field evidence;
  3. v1 capacity_timeline firm points — REPORTED only, used only when the row has no v2 steps at all and the points
     are not on the unsupported list (timeline_check), capped at the anchor before the anchor year.
Hard rules:
  - no capacity before an evidenced start_year (start_year non-null and not reported) — nor before the first evidence
    year when start_year is unknown;
  - before an installed anchor, only dated steps / history count, never the full plan; after it, the anchor;
  - reported never overrides confirmed;
  - paused/cancelled projects contribute nothing from 2025 on (D-018).
Series per year:
  firm (A)  = confirmed only (anchor, confirmed v2 steps);
  best (C)  = A, else reported steps/history, else (no anchor, operational) nameplate fill;
  npl  (B)  = A, else nameplate fill for operational plants without an anchor;
  iea  (D)  = max(C, any v2 step) and the full nameplate once a DATED reference year (D-032) is reached;
  iea_high  = max(D, nameplate once any reference year is reached).
"""
import json

FIRST, HORIZON, LAST_ACTUAL = 2015, 2030, 2025


def _steps(js):
    try:
        return {int(k): float(v) for k, v in json.loads(js).items() if v is not None and float(v) > 0}
    except (ValueError, TypeError, AttributeError, json.JSONDecodeError):
        return {}


def _level(steps, y):
    ks = [k for k in steps if k <= y]
    return steps[max(ks)] if ks else 0.0


def _v1_points(tl):
    try:
        pts = [p for p in json.loads(tl) if isinstance(p, dict) and p.get("year")
               and p.get("basis") in ("operational", "commissioned")]
    except (TypeError, json.JSONDecodeError):
        return {}
    out, level = {}, None
    for p in sorted(pts, key=lambda p: int(p["year"])):
        if p.get("cumulative_gwh") is not None:
            level = float(p["cumulative_gwh"])
        elif p.get("added_gwh") is not None:
            level = (level or 0.0) + float(p["added_gwh"])
        if level is not None:
            out[int(p["year"])] = level
    return out


def compute(r, tiers, bad_hist, ref_basis_dated):
    """Return {year: dict(firm, pipe, npl, best, basis, iea, ibasis, iea_high, kind)} or {}."""
    st, state = r["status"], (r.get("project_state") or "active")
    active = state == "active"
    np_, ry = r["nameplate_capacity_gwh"], r["capacity_ref_year"]
    t = tiers.get(r["id"], {})
    reported = set(json.loads(r["reported_fields"])) if r.get("reported_fields") else set()

    def confirmed(field):
        return field not in reported and t.get(field) != "reported"

    out = {}
    if st != "operational":
        # pipeline only
        oy = next((int(r[k]) for k in ("start_year", "capacity_ref_year", "announced_year") if r[k] is not None), None)
        if np_ is None or oy is None:
            return {}
        for y in range(max(oy, FIRST), HORIZON + 1):
            pipe = np_ if (active or y < LAST_ACTUAL) else 0.0
            out[y] = dict(firm=0.0, pipe=pipe, npl=0.0, best=0.0, basis="none", iea=0.0, ibasis="as_best",
                          iea_high=0.0, kind="pipeline")
        return out

    inst, asof = r["installed_capacity_gwh"], r["installed_as_of"]
    ay = int(str(asof)[:4]) if (inst is not None and asof) else None
    inst_conf = ay is not None and confirmed("installed_capacity_gwh")
    steps = _steps(r["capacity_by_year_json"]) if r["capacity_by_year_json"] else {}
    steps_conf = bool(steps) and confirmed("capacity_by_year_json")
    v1 = {} if (steps or r["id"] in bad_hist or not r["capacity_timeline"]) else _v1_points(r["capacity_timeline"])
    sy = r["start_year"]
    sy_ev = sy is not None and confirmed("start_year")

    # earliest year any capacity may be credited
    ev_years = [k for k in steps if k <= LAST_ACTUAL] + ([ay] if ay else []) + [k for k in v1 if k <= LAST_ACTUAL]
    if sy_ev:
        first = int(sy)                                   # never credit before an evidenced start year
    elif sy is not None:
        first = min([int(sy)] + ev_years)                 # reported start year: earliest of it and the evidence
    else:
        first = min(ev_years) if ev_years else None       # unknown start: from the first evidence year
    if first is None:
        return {}   # operational but nothing dated: counted as online-unquantified (not filled from the plan year)

    dated = ref_basis_dated
    for y in range(max(first, FIRST), HORIZON + 1):
        if y < first:
            continue
        # A: confirmed only
        a = 0.0
        if inst_conf and y >= ay:
            a = float(inst)
        elif steps_conf:
            a = _level(steps, y)
            if inst_conf and y < ay:
                a = min(a, float(inst))
        # C: best
        if a > 0:
            best, basis = a, "confirmed"
        else:
            rep = 0.0
            if ay is not None and y >= ay:                 # reported anchor
                rep = float(inst)
            elif steps:                                    # reported v2 steps
                rep = _level(steps, y)
            elif v1:                                       # v1 history, reported
                rep = _level(v1, y)
            if ay is not None and y < ay:
                rep = min(rep, float(inst))
            if np_ is not None:
                rep = min(rep, np_)
            if rep > 0:
                best, basis = rep, ("reported_v1_timeline" if (v1 and not steps) else "reported")
            elif r["id"] in bad_hist and not steps and ay is None:
                best, basis = 0.0, "unsupported_v1_timeline"      # rejected v1 history: no fill either
            elif ay is None and not steps and not v1 and np_ is not None:
                best, basis = np_, "nameplate_fill"
            else:
                best, basis = 0.0, "none"
        npl = a if a > 0 else (np_ if (ay is None and np_ is not None and basis != "unsupported_v1_timeline") else best)
        # D
        iea, ibasis = best, "as_best"
        stp = min(_level(steps, y), np_) if (steps and np_ is not None) else _level(steps, y)
        if stp > iea:
            iea, ibasis = stp, "dated_phase_step"
        if np_ is not None and ry is not None and int(ry) <= y and dated and np_ > iea:
            iea, ibasis = np_, "full_nameplate_dated"
        ih = max(iea, np_) if (np_ is not None and ry is not None and int(ry) <= y) else iea
        target = np_ if (np_ is not None and ry is not None and y >= int(ry)) else max(best, _level(steps, y))
        pipe = max(0.0, (target or 0.0) - a)
        if not active and y >= LAST_ACTUAL:
            a = best = npl = iea = ih = pipe = 0.0
        kind = "real" if (inst_conf or steps_conf) else ("reported" if (ay or steps or v1) else "modelled")
        out[y] = dict(firm=a, pipe=pipe, npl=npl, best=best, basis=basis, iea=iea, ibasis=ibasis, iea_high=ih, kind=kind)
    if all(v["best"] == 0 for y, v in out.items() if y <= LAST_ACTUAL):
        for v in out.values():
            v["kind"] = "online_unquantified"
    return out
