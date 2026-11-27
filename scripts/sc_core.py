"""Shared capacity rules for supply-chain outputs (after SC audit 2): one definition of BUILT for every script.

built(y)  = CONFIRMED-DATE FLOOR, not a growth series: max(installed_norm from installed_as_of; sourced dated steps (capacity_by_year_json) with year <= min(y, LAST));
            a plan's reference year never makes capacity built (fallback or target years are not completions);
upper(y)  = built + the rest of an OPERATIONAL row's plan once its capacity_ref_year <= y (D-high analogue, upper bound);
planned   = under_construction / announced capacity from the reference year (pipeline, separate).
Nickel intermediates (MHP, matte) are labelled separately so they are never added to the products made from them.
"""
import json

import pandas as pd

LAST = 2025
INTERMEDIATE = {"t Ni in MHP", "t Ni in matte"}


def steps(js):
    try:
        return {int(k): float(v) for k, v in json.loads(js).items() if v is not None}
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}


def built_upper(r, y):
    cap = r.capacity_norm if pd.notna(r.capacity_norm) else r.installed_norm
    if pd.isna(cap) and pd.isna(r.installed_norm):
        return 0.0, 0.0
    b = 0.0
    if pd.notna(r.installed_norm) and pd.notna(r.installed_as_of) and int(str(r.installed_as_of)[:4]) <= y:
        b = float(r.installed_norm)
    st = steps(r.capacity_by_year_json)
    if st:
        scale = (r.capacity_norm / r.capacity) if pd.notna(r.capacity_norm) and pd.notna(r.capacity) and r.capacity else 1.0
        ks = [k for k in st if k <= min(y, LAST)]
        if ks:
            b = max(b, st[max(ks)] * scale)
    up = b
    if pd.notna(cap) and pd.notna(r.capacity_ref_year) and int(r.capacity_ref_year) <= y:
        up = max(b, float(cap))
    return b, up


def is_intermediate(r):
    """Nickel MHP/matte rows: by capacity unit OR production unit (audit 3)."""
    return r.capacity_unit in INTERMEDIATE or getattr(r, "production_unit", None) in INTERMEDIATE


def commodity_label(r):
    return f"{r.commodity} (intermediate)" if is_intermediate(r) else r.commodity
