#!/usr/bin/env python3
"""Ember-house-style reconciliation PNG: battery cell manufacturing capacity by year.

Series A (stacked bars, by region) = capacity ONLINE / achieved (dated, sourced
operational figures, held flat between sourced points) — the floor.
Series B (dashed line) = installed nameplate on the IEA/BNEF basis (an operational
plant's full nameplate credited from its commissioning year) — the upper comparator.
IEA / BNEF (gold markers) = published external nameplate benchmarks, which land
between A and B — the reconciliation.

Run: python3 scripts/make_chart_png.py  ->  capacity_chart.png
"""
import csv
import sys

import duckdb
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

sys.path.insert(0, "/root/.claude/skills/ember-chart-design/assets")
from ember_style import (setup_style, new_figure, add_header, add_footer,
                         round_ticks, COLOR, UI, BOLD_FAMILY)

DB = "factories.db"
OUT = "capacity_chart.png"
YEARS = list(range(2018, 2031))

# Collapse 8 regions into <=5 coloured groups (2026 guide: five colours or fewer).
# China carries the finding, so it gets the bright green; the rest are muted.
GROUPS = [
    ("China", "China", COLOR["solar"]),
    ("Europe", "Europe", COLOR["nuclear"]),
    ("USA", "United States", COLOR["highlight_blue"]),
    ("Rest of world", None, "#B0B7C6"),   # everything else
]
REST = {"South Korea", "Japan", "India", "Southeast Asia", "Rest of World"}


def load():
    con = duckdb.connect(DB)
    n = con.execute("SELECT count(*) FROM factories").fetchone()[0]
    firm = con.execute("""SELECT year, region, sum(gwh_firm) FROM capacity_by_year
        WHERE year BETWEEN 2018 AND 2030 GROUP BY year, region""").fetchall()
    nameplate = dict(con.execute("""SELECT year, sum(gwh_nameplate) FROM capacity_by_year
        WHERE year BETWEEN 2018 AND 2030 GROUP BY year""").fetchall())
    con.close()
    # group firm by the 4 display buckets
    G = {g[0]: {y: 0.0 for y in YEARS} for g in GROUPS}
    for y, r, g in firm:
        g = g or 0.0
        if r == "China":
            G["China"][y] += g
        elif r == "Europe":
            G["Europe"][y] += g
        elif r == "USA":
            G["USA"][y] += g
        elif r in REST:
            G["Rest of world"][y] += g
    B = {y: (nameplate.get(y) or 0.0) for y in YEARS}
    return n, G, B


def benchmarks():
    out = {"IEA": {}, "BNEF": {}}
    try:
        for row in csv.DictReader(l for l in open("scripts/benchmarks.csv") if not l.startswith("#")):
            if row["source"] in out:
                out[row["source"]][int(row["year"])] = float(row["gwh"]) / 1000.0
    except OSError:
        pass
    return out


def main():
    setup_style()
    n, G, B = load()
    bench = benchmarks()

    fig, ax = new_figure(figsize=(11, 7.4))
    # push the plot down to leave room for a 2-line title, subtitle and legend
    fig.subplots_adjust(top=0.58, bottom=0.20, left=0.07, right=0.97)
    x = np.arange(len(YEARS))

    # Series A — stacked bars (TWh)
    base = np.zeros(len(YEARS))
    for name, _lab, colour in GROUPS:
        vals = np.array([G[name][y] / 1000.0 for y in YEARS])
        ax.bar(x, vals, bottom=base, width=0.62, color=colour, zorder=3,
               edgecolor=UI["background"], linewidth=0.4)
        base += vals
    online_top = base.copy()

    # online total labels above each bar (TWh, one decimal)
    for i, v in enumerate(online_top):
        ax.text(x[i], v + 0.06, f"{v:.1f}", ha="center", va="bottom",
                fontsize=9, family=BOLD_FAMILY, color=UI["title"], zorder=6)

    # Series B — installed nameplate (IEA/BNEF basis): DEMOTED to a faint
    # background reference. The 2018 comparison shows BNEF's real reported
    # nameplate tracks the achieved bars, not this back-dated full-nameplate line.
    bvals = np.array([B[y] / 1000.0 for y in YEARS])
    ax.plot(x, bvals, color=UI["gridline"], linewidth=1.2, linestyle=(0, (2, 2)),
            zorder=2)
    ax.text(x[-1], bvals[-1] + 0.05, "Installed nameplate\n(full-nameplate basis)",
            ha="right", va="bottom", fontsize=8.5, color=UI["axis_label"], zorder=6)

    # IEA / BNEF published benchmarks — the lead comparison. Both amber, drawn as
    # connected lines across their sourced years and distinguished by marker +
    # direct label (never colour alone).
    gold = COLOR["highlight_yellow"]

    def bench_line(series, marker, filled, label):
        pts = sorted((YEARS.index(y), g) for y, g in series.items() if y in YEARS)
        if not pts:
            return
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        if len(pts) > 1:
            ax.plot(xs, ys, color=gold, linewidth=2, zorder=7)
        ax.scatter(xs, ys, s=64, marker=marker, zorder=8,
                   facecolor=(gold if filled else "none"),
                   edgecolor=("#7a5300" if filled else gold),
                   linewidth=(1 if filled else 2))
        ax.text(xs[-1] + 0.15, ys[-1], label, ha="left", va="center",
                fontsize=10.5, color="#8a6300", family=BOLD_FAMILY, zorder=8)

    bench_line(bench["BNEF"], "D", False, "BNEF")
    bench_line(bench["IEA"], "o", True, "IEA")

    ax.set_xticks(x)
    ax.set_xticklabels([str(y) for y in YEARS], rotation=0, fontsize=10)
    ax.grid(axis="x", visible=False)
    round_ticks(ax, axis="y")
    ax.set_ylim(0, 6.2)
    ax.set_xlim(-0.7, len(YEARS) - 0.3)

    # legend — bar groups + the two comparators (bar chart => legend is the fallback)
    handles = [Line2D([0], [0], marker="s", linestyle="", markersize=11,
                      markerfacecolor=c, markeredgewidth=0, label=lab)
               for lab, (_n, _l, c) in zip(
                   ["China", "Europe", "United States", "Rest of world"], GROUPS)]
    handles += [
        Line2D([0], [0], marker="D", linestyle="-", color=gold, markersize=8,
               markerfacecolor="none", markeredgecolor=gold, markeredgewidth=2,
               label="BNEF reported nameplate"),
        Line2D([0], [0], marker="o", linestyle="-", color=gold, markersize=9,
               markerfacecolor=gold, markeredgecolor="#7a5300", label="IEA reported nameplate"),
        Line2D([0], [0], color=UI["gridline"], linewidth=1.2, linestyle=(0, (2, 2)),
               label="Installed nameplate (full-nameplate basis)"),
    ]
    leg = ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, 1.27),
                    ncol=3, frameon=False, handletextpad=0.5, columnspacing=1.4,
                    fontsize=10.5)
    for t in leg.get_texts():
        t.set_color(UI["title"])

    add_header(fig,
               "The cell capacity we can source as online is a floor below\nIEA and BNEF's nameplate – and far below full nameplate",
               "Global battery cell manufacturing capacity (TWh per year), by region, 2018–2030",
               title_y=0.97, subtitle_y=0.84)
    add_footer(fig,
               source="Ember Futures battery gigafactory database; IEA; BloombergNEF; Ember analysis",
               note="Bars: capacity online – dated, sourced operational figures held flat between sourced points (the floor). IEA/BNEF lines are\n"
                    "their reported nameplate (IEA from 2021; 2021–22 derived from IEA's stated additions). No credible primary 2018–20 benchmark\n"
                    "could be sourced. The faint dotted line back-dates each plant's full nameplate to commissioning – an upper bound. ~95% of bars are sourced.")

    fig.savefig(OUT, dpi=200, facecolor=UI["background"], bbox_inches="tight")
    print(f"wrote {OUT}")
    print("online TWh:", {y: round(online_top[i], 2) for i, y in enumerate(YEARS)})
    print("nameplate TWh:", {y: round(B[y] / 1000, 2) for y in YEARS})


if __name__ == "__main__":
    main()
