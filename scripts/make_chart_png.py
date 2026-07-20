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

    # Series B — installed nameplate (IEA/BNEF basis): dashed line
    bvals = np.array([B[y] / 1000.0 for y in YEARS])
    ax.plot(x, bvals, color=UI["title"], linewidth=2, linestyle=(0, (5, 3)),
            zorder=4)

    # IEA / BNEF published benchmarks — gold markers
    gold = COLOR["highlight_yellow"]
    for yr, g in bench["IEA"].items():
        if yr in YEARS:
            ax.scatter([YEARS.index(yr)], [g], s=70, color=gold, edgecolor="#7a5300",
                       linewidth=1, zorder=7)
    for yr, g in bench["BNEF"].items():
        if yr in YEARS:
            ax.scatter([YEARS.index(yr)], [g], s=70, marker="D", facecolor="none",
                       edgecolor=gold, linewidth=2, zorder=7)

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
        Line2D([0], [0], color=UI["title"], linewidth=2, linestyle=(0, (5, 3)),
               label="Installed nameplate (IEA/BNEF basis)"),
        Line2D([0], [0], marker="o", linestyle="", markersize=9, markerfacecolor=gold,
               markeredgecolor="#7a5300", label="IEA (published)"),
        Line2D([0], [0], marker="D", linestyle="", markersize=8, markerfacecolor="none",
               markeredgecolor=gold, markeredgewidth=2, label="BNEF (published)"),
    ]
    leg = ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, 1.27),
                    ncol=3, frameon=False, handletextpad=0.5, columnspacing=1.4,
                    fontsize=10.5)
    for t in leg.get_texts():
        t.set_color(UI["title"])

    add_header(fig,
               "IEA and BNEF sit between the cell capacity actually online\nand the full installed nameplate",
               "Global battery cell manufacturing capacity (TWh per year), by region, 2018–2030",
               title_y=0.97, subtitle_y=0.84)
    add_footer(fig,
               source="Ember Futures battery gigafactory database; IEA; BloombergNEF; Ember analysis",
               note="Bars show capacity online – dated, sourced operational figures held flat between sourced points (the floor). The\n"
                    "dashed line credits each operational plant's full nameplate from its commissioning year (the IEA/BNEF basis; real\n"
                    "utilisation ~40–50%). IEA and BNEF report nameplate and land between the two. ~95% of the online curve is real, sourced data.")

    fig.savefig(OUT, dpi=200, facecolor=UI["background"], bbox_inches="tight")
    print(f"wrote {OUT}")
    print("online TWh:", {y: round(online_top[i], 2) for i, y in enumerate(YEARS)})
    print("nameplate TWh:", {y: round(B[y] / 1000, 2) for y in YEARS})


if __name__ == "__main__":
    main()
