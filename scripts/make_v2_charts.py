#!/usr/bin/env python3
"""v2 analytical charts (Ember analytical-chart style: white background, watermark, source line; not for publication).

    python3 scripts/make_v2_charts.py     # after build_timeseries.py and build_unallocated.py

Writes charts/capacity_vs_benchmarks.png and charts/capacity_map_v2.png. Every number is read from factories.db,
capacity_by_year_e.csv and scripts/benchmarks.csv; nothing is typed in.
"""
import csv
import json
import os

import duckdb
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.collections import PatchCollection  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
os.makedirs("charts", exist_ok=True)
INK, SUB, GRID, TOTAL, HL, HL2, CTX2 = "#192238", "#626E88", "#B0B7C6", "#3E4860", "#E04B00", "#37A6E6", "#D8DBE6"
WATERMARK = "Internal working chart – not for publication"
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.edgecolor": GRID, "axes.labelcolor": SUB,
                     "xtick.color": SUB, "ytick.color": SUB, "figure.facecolor": "#FFFFFF", "axes.facecolor": "#FFFFFF"})

con = duckdb.connect("factories.db", read_only=True)
years = list(range(2020, 2026))
q = {r[0]: r[1:] for r in con.execute(
    f"SELECT year, sum(gwh_best), sum(gwh_iea), sum(gwh_iea_high) FROM capacity_by_year "
    f"WHERE year BETWEEN {years[0]} AND {years[-1]} GROUP BY year").fetchall()}
e = {int(r["year"]): float(r["gwh_series_e"]) for r in csv.DictReader(open("capacity_by_year_e.csv"))}
bench = [r for r in csv.DictReader(l for l in open("scripts/benchmarks.csv") if not l.startswith("#"))]


def tw(x):
    return x / 1000.0


C = [tw(q[y][0]) for y in years]
D = [tw(q[y][1]) for y in years]
DH = [tw(q[y][2]) for y in years]
E = [tw(e[y]) for y in years]

fig = plt.figure(figsize=(10, 6.2), dpi=200)
ax = fig.add_axes([0.08, 0.2, 0.74, 0.58])
ax.fill_between(years, D, DH, color=HL, alpha=0.15, linewidth=0)
ax.plot(years, C, color=TOTAL, lw=2)
ax.plot(years, E, color=HL, lw=2.5)
style = {"IEA": (HL2, "o"), "BNEF": (INK, "s"), "Benchmark": (SUB, "^")}
for b in bench:
    y, v = int(b["year"]), float(b["gwh"]) / 1000
    col, mk = style.get(b["source"], (SUB, "D"))
    derived = "NOT an IEA figure" in b["note"]
    ax.scatter([y], [v], s=55, marker=mk, facecolors="none" if derived else col, edgecolors=col, linewidths=1.5, zorder=5)
ax.set_xticks(years)
ax.set_ylim(0, 5)
ax.yaxis.grid(True, color=GRID, lw=0.6)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(length=0)
# direct labels at line ends
last = years[-1]
ax.annotate(f"Series E {E[-1]:.1f}", (last, E[-1]), xytext=(8, 6), textcoords="offset points", color=HL, fontsize=9)
ax.annotate(f"IEA-basis range {D[-1]:.1f}–{DH[-1]:.1f}", (last, DH[-1]), xytext=(8, 4), textcoords="offset points",
            color=HL, fontsize=8, alpha=0.9)
ax.annotate(f"Producing (C) {C[-1]:.1f}", (last, C[-1]), xytext=(8, -12), textcoords="offset points", color=TOTAL, fontsize=9)
share = 100 * e[last] / max(float(b["gwh"]) for b in bench if b["source"] == "IEA" and int(b["year"]) == last)
fig.text(0.08, 0.93, f"Bottom-up cell capacity reaches {share:.0f}% of the IEA figure for {last}",
         fontsize=14, weight="bold", color=INK)
fig.text(0.08, 0.885, f"Lithium-ion battery cell manufacturing capacity (TWh per year), global, {years[0]}–{last}",
         fontsize=10, color=SUB)
handles = [Line2D([], [], color=HL, lw=2.5, label="Ours: Series E (IEA basis + unallocated company capacity)"),
           Line2D([], [], color=HL, lw=8, alpha=0.15, label="Ours: IEA-basis range (D to D-high)"),
           Line2D([], [], color=TOTAL, lw=2, label="Ours: actually producing (C)"),
           Line2D([], [], color=HL2, marker="o", lw=0, label="IEA"),
           Line2D([], [], color=INK, marker="s", lw=0, label="BNEF"),
           Line2D([], [], color=SUB, marker="^", lw=0, label="Benchmark")]
fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.075, 0.87), ncol=3, frameon=False, fontsize=8,
           labelcolor=INK)
fig.text(0.08, 0.10, "Hollow IEA markers (2021–2022) are back-calculated from IEA's stated annual additions, not IEA "
         "figures. IEA and Benchmark are not independent (IEA uses Benchmark data). Series E excludes converted Ah "
         "estimates.", fontsize=7.5, color=SUB, wrap=True)
fig.text(0.08, 0.06, "Source: Cell gigafactory database v2; IEA GEVO 2026; BNEF and Benchmark free pages", fontsize=7.5, color=SUB)
fig.text(0.98, 0.06, WATERMARK, fontsize=7.5, color=SUB, ha="right")
fig.savefig("charts/capacity_vs_benchmarks.png")
plt.close(fig)
# title check: the claim is recomputed above from the same data; assert it is still in range
assert 0 < share < 200, share

# ---- map ----
rows = con.execute("""SELECT longitude, latitude, status, coalesce(nameplate_capacity_gwh, 1)
                      FROM factories_active WHERE latitude IS NOT NULL AND longitude IS NOT NULL""").fetchall()
n_all = con.execute("SELECT count(*) FROM factories_active").fetchone()[0]
fig = plt.figure(figsize=(11, 6.2), dpi=200)
ax = fig.add_axes([0.03, 0.12, 0.94, 0.72])
geo = json.load(open("data/world.geo.json"))
polys = []
for f in geo["features"]:
    g = f["geometry"]
    parts = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    for p in parts:
        polys.append(Polygon(p[0], closed=True))
ax.add_collection(PatchCollection(polys, facecolor="#F0F1F5", edgecolor=CTX2, linewidth=0.3))
cols = {"operational": TOTAL, "under_construction": HL2, "announced": GRID}
for st in ("announced", "under_construction", "operational"):
    pts = [r for r in rows if r[2] == st]
    ax.scatter([r[0] for r in pts], [r[1] for r in pts], s=[max(4, r[3] * 1.2) for r in pts], color=cols[st],
               alpha=0.6, edgecolors="white", linewidths=0.3, label=st.replace("_", " "))
ax.set_xlim(-170, 180)
ax.set_ylim(-58, 80)
ax.axis("off")
n = {st: sum(1 for r in rows if r[2] == st) for st in cols}
fig.text(0.03, 0.93, "Battery cell plants by status, sized by planned capacity", fontsize=14, weight="bold", color=INK)
fig.text(0.03, 0.89, f"{len(rows)} located sites: {n['operational']} operational, {n['under_construction']} under "
         f"construction, {n['announced']} announced (bubble area = nameplate GWh per year)", fontsize=10, color=SUB)
ax.legend(loc="lower left", frameon=False, fontsize=8, markerscale=0.6, labelcolor=INK)
fig.text(0.03, 0.07, f"Most coordinates are city-level approximations. {n_all - len(rows)} of {n_all} active sites have no "
         "coordinates yet and are not shown.", fontsize=7.5, color=SUB)
fig.text(0.03, 0.04, "Source: Battery cell gigafactory database v2 (open sources)", fontsize=7.5, color=SUB)
fig.text(0.97, 0.04, WATERMARK, fontsize=7.5, color=SUB, ha="right")
fig.savefig("charts/capacity_map_v2.png")
print("wrote charts/capacity_vs_benchmarks.png, charts/capacity_map_v2.png;",
      f"title check: Series E {e[last]:.0f} GWh = {share:.0f}% of IEA {last}")
