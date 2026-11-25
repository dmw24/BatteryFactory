"""Per-plant capacity series, v4 rules (T102 + T111 audits, 2026-11-25). Used by build_timeseries.py.

Evidence precedence:
  1. installed anchor (installed_capacity_gwh @ installed_as_of) — tier from field evidence;
  2. v2 dated steps (capacity_by_year_json) — confirmed PER STEP: a step is confirmed only if a confirmed quote for
     the field contains its value; other steps are reported;
  3. v1 capacity_timeline firm points — reported only; points the timeline check found unsupported are dropped one by
     one; used when the row has no v2 steps, or for years after the last v2 step (to raise C, never A).
Hard rules: nothing before an evidenced start_year (or before the first evidence year when start is unknown); before an
installed anchor only dated steps / history count, never the full plan; reported never overrides confirmed; operational
plants with nothing dated are online-unquantified; paused/cancelled projects contribute nothing from 2025 on (D-018).
Series per year:
  firm (A)  = confirmed INSTALLED anchor only (from installed_as_of on) — the installed floor;
  best (C)  = A, else confirmed dated step, else reported step/history, else (no anchor, no dated data) nameplate fill;
  npl  (B)  = A, else (dated data exists) C, else nameplate fill — the upper fill, never below C;
  iea  (D)  = max(C, any v2 step) and the full nameplate once a DATED reference year (D-032) is reached — unless a
              confirmed installed anchor at or after that year is lower than the nameplate;
  iea_high  = max(D, nameplate once any reference year is reached);
  pipe      = planned target above C (0 for inactive projects).
"""
import json
import re

FIRST, HORIZON, LAST_ACTUAL = 2015, 2030, 2025


def _steps(js):
    try:
        return {int(k): float(v) for k, v in json.loads(js).items() if v is not None and float(v) > 0}
    except (ValueError, TypeError, AttributeError, json.JSONDecodeError):
        return {}


def _level(steps, y):
    ks = [k for k in steps if k <= y]
    return steps[max(ks)] if ks else 0.0


def _v1_points(tl, bad_points, rid):
    try:
        pts = [p for p in json.loads(tl) if isinstance(p, dict) and p.get("year")
               and p.get("basis") in ("operational", "commissioned")]
    except (TypeError, json.JSONDecodeError):
        return {}
    out, level = {}, None
    for p in sorted(pts, key=lambda p: int(p["year"])):
        if (rid, int(p["year"])) in bad_points:
            continue                                   # point-level rejection (T111)
        if p.get("cumulative_gwh") is not None:
            level = float(p["cumulative_gwh"])
        elif p.get("added_gwh") is not None:
            level = (level or 0.0) + float(p["added_gwh"])
        if level is not None:
            out[int(p["year"])] = level
    return out


def _num_forms(v):
    f = float(v)
    forms = {f"{f:g}", f"{f:.1f}", f"{f:.2f}"}
    if f == int(f):
        forms.add(str(int(f)))
    return forms


def step_confirmed(value, quotes):
    """A step is confirmed if any confirmed quote for capacity_by_year_json contains the number."""
    for q in quotes:
        txt = re.sub(r"[\s,]", "", q or "")
        if any(re.search(r"(?<![\d.])" + re.escape(form) + r"(?![\d])", txt) for form in _num_forms(value)):
            return True
    return False


def compute(r, tiers, step_quotes, bad_points, ref_basis_dated):
    st, state = r["status"], (r.get("project_state") or "active")
    active = state == "active"
    np_, ry = r["nameplate_capacity_gwh"], r["capacity_ref_year"]
    t = tiers.get(r["id"], {})
    reported = set(json.loads(r["reported_fields"])) if r.get("reported_fields") else set()

    def confirmed(field):
        return field not in reported and t.get(field) != "reported"

    out = {}
    if st != "operational":
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
    field_conf = bool(steps) and confirmed("capacity_by_year_json")
    qs = step_quotes.get(r["id"], [])
    conf_steps = {k: v for k, v in steps.items() if field_conf and step_confirmed(v, qs)}
    v1 = _v1_points(r["capacity_timeline"], bad_points, r["id"]) if r["capacity_timeline"] else {}
    last_step = max([k for k in steps if k <= LAST_ACTUAL], default=None)
    v1_late = {k: v for k, v in v1.items() if last_step is not None and k > last_step}
    use_v1 = v1 if not steps else {}
    sy = r["start_year"]
    sy_ev = sy is not None and confirmed("start_year")

    ev_years = ([k for k in steps if k <= LAST_ACTUAL] + ([ay] if ay else [])
                + [k for k in list(use_v1) + list(v1_late) if k <= LAST_ACTUAL])
    if sy_ev:
        first = int(sy)
    elif sy is not None:
        first = min([int(sy)] + ev_years)
    else:
        first = min(ev_years) if ev_years else None
    if first is None:
        return {}
    has_rejected = any(rid == r["id"] for rid, _ in bad_points)
    has_dated = bool(steps or use_v1 or v1_late or ay) or has_rejected   # rejected history: never plan-filled
    anchor_caps_d = inst_conf and np_ is not None and float(inst) < np_

    for y in range(max(first, FIRST), HORIZON + 1):
        a = float(inst) if (inst_conf and y >= ay) else 0.0
        if a > 0:
            best, basis = a, "confirmed"
        else:
            cs = _level(conf_steps, y)
            rs = _level(steps, y)                       # all v2 steps (cumulative sums of quoted phases are reported)
            if ay is not None and y < ay:
                cs, rs = min(cs, float(inst)), min(rs, float(inst))
            if np_ is not None:
                rs = min(rs, np_)
            if cs > 0 or rs > 0:
                best, basis = (cs, "dated_step") if cs >= rs else (rs, "reported_step")
            else:
                if ay is not None and y >= ay:
                    rep = float(inst)                          # reported anchor
                else:
                    rep = max(_level(steps, y), _level(use_v1, y))
                    if ay is not None:
                        rep = min(rep, float(inst))
                if np_ is not None:
                    rep = min(rep, np_)
                if rep > 0:
                    best, basis = rep, ("reported_v1_timeline" if (use_v1 and not steps) else "reported")
                elif not has_dated and np_ is not None:
                    best, basis = np_, "nameplate_fill"
                else:
                    best, basis = 0.0, "none"
        # a later reported v1 point may raise C (never A), but not above a confirmed anchor already in force
        late = _level(v1_late, y)
        if late > best and (np_ is None or late <= np_) and a == 0:
            best, basis = late, "reported_v1_later"
        npl = max(a, best) if has_dated else (np_ if np_ is not None else best)
        # D
        iea, ibasis = best, "as_best"
        stp = min(_level(steps, y), np_) if (steps and np_ is not None) else _level(steps, y)
        if stp > iea:
            iea, ibasis = stp, "dated_phase_step"
        full_ok = not (anchor_caps_d and y <= ay)
        if np_ is not None and ry is not None and int(ry) <= y and ref_basis_dated and np_ > iea and full_ok:
            iea, ibasis = np_, "full_nameplate_dated"
        ih = max(iea, np_) if (np_ is not None and ry is not None and int(ry) <= y) else iea
        target = np_ if (np_ is not None and ry is not None and y >= int(ry)) else max(best, _level(steps, y))
        pipe = max(0.0, (target or 0.0) - best) if active else 0.0
        if not active and y >= LAST_ACTUAL:
            a = best = npl = iea = ih = pipe = 0.0
        kind = "real" if (inst_conf or conf_steps) else ("reported" if has_dated else "modelled")
        out[y] = dict(firm=a, pipe=pipe, npl=npl, best=best, basis=basis, iea=iea, ibasis=ibasis, iea_high=ih, kind=kind)
    if all(v["best"] == 0 for y, v in out.items() if y <= LAST_ACTUAL):
        for v in out.values():
            v["kind"] = "online_unquantified"
    return out
