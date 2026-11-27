#!/usr/bin/env python3
"""Supply-chain analytical charts (Ember analytical style; internal working charts).
charts/sc_asset_map.png — assets with coordinates, colour = step, operational vs pipeline marker.
charts/sc_coverage.png — our sourced production/capacity as a share of open benchmarks (latest year), by step.
Numbers are read from sc_assets.csv and sc_benchmark.csv only."""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.collections import PatchCollection  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT); os.makedirs("charts", exist_ok=True)
INK, SUB, GRID, CTX2 = "#192238", "#626E88", "#B0B7C6", "#D8DBE6"
WATERMARK = "Internal working chart – not for publication"
STEP_COL = {"mining": "#E04B00", "refining": "#37A6E6", "precursor": "#8E6CC8", "cathode": "#192238",
            "anode": "#3E9E6E", "electrolyte": "#D9A400", "separator": "#9AA5B8", "foil": "#B86E3C", "recycling": "#5CC3B5"}
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.edgecolor": GRID, "axes.labelcolor": SUB,
                     "xtick.color": SUB, "ytick.color": SUB})
a = pd.read_csv("sc_assets.csv")
a = a[a.project_state.fillna("active") == "active"]

fig = plt.figure(figsize=(11, 6.2), dpi=200)
ax = fig.add_axes([0.03, 0.12, 0.94, 0.72])
polys = []
for f in json.load(open("data/world.geo.json"))["features"]:
    g = f["geometry"]
    for p in (g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]):
        polys.append(Polygon(p[0], closed=True))
ax.add_collection(PatchCollection(polys, facecolor="#F0F1F5", edgecolor=CTX2, linewidth=0.3))
g = a[a.latitude.notna()]
for st, c in STEP_COL.items():
    s = g[g.step == st]
    op = s[s.status == "operational"]; pl = s[s.status != "operational"]
    ax.scatter(op.longitude, op.latitude, s=10, color=c, alpha=0.75, edgecolors="white", linewidths=0.2, label=f"{st} ({len(s)})")
    ax.scatter(pl.longitude, pl.latitude, s=10, facecolors="none", edgecolors=c, linewidths=0.6, alpha=0.8)
ax.set_xlim(-170, 180); ax.set_ylim(-58, 80); ax.axis("off")
fig.text(0.03, 0.93, "Battery supply-chain assets with coordinates, by step", fontsize=14, weight="bold", color=INK)
fig.text(0.03, 0.885, f"{len(g)} of {len(a)} active assets mapped (filled = operational, ring = under construction/announced); "
         "most points are city-level approximations", fontsize=10, color=SUB)
ax.legend(loc="lower left", frameon=False, fontsize=7.5, ncol=3, labelcolor=INK, markerscale=1.2)
fig.text(0.03, 0.04, "Source: Battery supply-chain asset database (open sources; CGS Nickel Smelter Dataset CC BY 4.0)", fontsize=7.5, color=SUB)
fig.text(0.97, 0.04, WATERMARK, fontsize=7.5, color=SUB, ha="right")
fig.savefig("charts/sc_asset_map.png"); plt.close(fig)

b = pd.read_csv("sc_benchmark.csv")
pick = [("mining", "lithium", "production", "World"), ("mining", "cobalt", "production", "World"),
        ("mining", "nickel", "production", "Canada"), ("mining", "graphite", "production", "World"),
        ("refining", "lithium", "production", "China"), ("cathode", "cathode", "production", "China"),
        ("anode", "anode", "shipments", "China"), ("electrolyte", "electrolyte", "shipments", "China"),
        ("separator", "separator", "shipments", "China")]
rows = []
for st, com, met, ctry in pick:
    s = b[(b.step == st) & (b.commodity == com) & (b.metric == met) & (b.country == ctry)]
    if st == "mining":
        s = s[s.source.str.startswith("USGS")]
    if not len(s):
        continue
    r = s.sort_values("year").iloc[-1]
    site = r.ours_production if st == "mining" else r.ours_capacity
    comp = r.unallocated_production if st == "mining" else r.company_disclosed_output
    lab = {"refining": f"{com} chemicals", "cathode": "cathode material", "anode": "anode material"}.get(st, com)
    rows.append((f"{lab} – {ctry} {r.year} (capacity vs output)" if st != "mining" else f"{com} mine output – {ctry} {r.year}",
                 site / r.benchmark, comp / r.benchmark, "capacity at sites" if st != "mining" else "site output"))
fig = plt.figure(figsize=(10, 5.6), dpi=200)
ax = fig.add_axes([0.36, 0.14, 0.58, 0.68])
ys = range(len(rows))[::-1]
ax.barh(list(ys), [min(r[1], 1.5) for r in rows], color="#E04B00", height=0.55, label="sourced at asset level (mining: output; processing: built capacity)")
ax.scatter([min(r[2], 1.5) for r in rows], list(ys), color=INK, zorder=5, s=18, label="company-disclosed output, China-only companies (processing) / company-level output (mining)")
ax.axvline(1, color=SUB, lw=0.8, ls=(0, (3, 3)))
ax.set_yticks(list(ys)); ax.set_yticklabels([r[0] for r in rows], fontsize=8, color=INK)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}")); ax.set_xlim(0, 1.5)
ax.xaxis.grid(True, color=GRID, lw=0.5); ax.set_axisbelow(True)
for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
fig.text(0.03, 0.93, "How much of the open benchmarks the asset database explains", fontsize=14, weight="bold", color=INK)
fig.text(0.03, 0.885, "Share of benchmark (USGS mine output; MIIT/industry China output) — 100% = benchmark", fontsize=10, color=SUB)
ax.legend(loc="lower right", frameon=False, fontsize=7, labelcolor=INK)
fig.text(0.03, 0.04, "Source: Battery supply-chain asset database; USGS MCS 2026; MIIT; EVTank/GGII/ICC via open press", fontsize=7.5, color=SUB)
fig.text(0.97, 0.04, WATERMARK, fontsize=7.5, color=SUB, ha="right")
fig.savefig("charts/sc_coverage.png"); plt.close(fig)
print("charts written")
