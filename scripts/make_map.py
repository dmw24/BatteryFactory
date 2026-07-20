#!/usr/bin/env python3
"""Global bubble map of battery cell manufacturing sites (2025 snapshot), fully offline.

Bubble AREA = nameplate capacity (GWh/year); colour = status. Uses each site's stored
coordinates (mostly city-centroid approximations, flagged in the DB — fine at world
scale) and a bundled low-res world outline (data/world.geo.json) so no map tiles or
CDN geometry are fetched. Renders an Ember-styled PNG via matplotlib.

Run: python3 scripts/make_map.py  ->  capacity_map.png
"""
import json
import sys

import duckdb
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection
from matplotlib.lines import Line2D

sys.path.insert(0, "/root/.claude/skills/ember-chart-design/assets")
from ember_style import setup_style, add_header, add_footer, UI, BOLD_FAMILY, FONT_FAMILY

OUT = "capacity_map.png"
WORLD = "data/world.geo.json"

STATUS = [
    ("operational",        "Operational",        "#13CE74"),
    ("under_construction", "Under construction", "#37A6E6"),
    ("announced",          "Announced",          "#203772"),
]
UNKNOWN_COL = "#8792A6"
LAND, BORDER = "#E4E8EF", "#FFFFFF"


def polys(geom):
    """Yield lon/lat ring lists for Polygon / MultiPolygon."""
    t, c = geom["type"], geom["coordinates"]
    if t == "Polygon":
        yield c[0]
    elif t == "MultiPolygon":
        for p in c:
            yield p[0]


def main():
    setup_style()
    con = duckdb.connect("factories.db")
    rows = con.execute("""SELECT plant_name, region, status, latitude, longitude,
        nameplate_capacity_gwh FROM factories
        WHERE latitude IS NOT NULL AND longitude IS NOT NULL""").fetchall()
    n_total = con.execute("SELECT count(*) FROM factories").fetchone()[0]
    con.close()

    sized = [r for r in rows if r[5]]
    nocap = [r for r in rows if not r[5]]
    maxcap = max(r[5] for r in sized)
    SCALE = 900.0 / maxcap          # max bubble ~900 pt^2 area; area ∝ capacity

    fig = plt.figure(figsize=(13, 7.2))
    fig.subplots_adjust(top=0.80, bottom=0.11, left=0.02, right=0.98)
    ax = fig.add_axes([0.02, 0.11, 0.96, 0.66])

    # world land
    patches = []
    for feat in json.load(open(WORLD))["features"]:
        for ring in polys(feat["geometry"]):
            patches.append(MplPolygon(ring, closed=True))
    ax.add_collection(PatchCollection(patches, facecolor=LAND, edgecolor=BORDER,
                                      linewidths=0.5, zorder=1))

    # located-only sites (capacity unpublished): small hollow dots
    if nocap:
        ax.scatter([r[4] for r in nocap], [r[3] for r in nocap], s=8, facecolors="none",
                   edgecolors=UNKNOWN_COL, linewidths=0.6, alpha=0.7, zorder=2)

    # sized bubbles by status
    for key, label, colour in STATUS:
        grp = [r for r in sized if r[2] == key]
        if grp:
            ax.scatter([r[4] for r in grp], [r[3] for r in grp],
                       s=[r[5] * SCALE for r in grp], color=colour,
                       edgecolors="white", linewidths=0.4, alpha=0.72, zorder=3)
    unk = [r for r in sized if r[2] not in {s[0] for s in STATUS}]
    if unk:
        ax.scatter([r[4] for r in unk], [r[3] for r in unk],
                   s=[r[5] * SCALE for r in unk], color=UNKNOWN_COL,
                   edgecolors="white", linewidths=0.4, alpha=0.72, zorder=3)

    ax.set_xlim(-170, 185)
    ax.set_ylim(-58, 82)
    ax.set_aspect(1.35)              # gentle stretch so it reads as a world map
    ax.axis("off")

    # status legend (colour) + size legend (reference bubbles)
    status_h = [Line2D([0], [0], marker="o", linestyle="", markersize=9, markerfacecolor=c,
                       markeredgecolor="white", label=l) for _k, l, c in STATUS]
    status_h.append(Line2D([0], [0], marker="o", linestyle="", markersize=6,
                           markerfacecolor="none", markeredgecolor=UNKNOWN_COL,
                           label="Capacity not published"))
    leg1 = ax.legend(handles=status_h, loc="lower left", bbox_to_anchor=(0.0, -0.02),
                     frameon=False, fontsize=11, labelcolor=UI["title"], ncol=2,
                     handletextpad=0.4, columnspacing=1.2)
    ax.add_artist(leg1)
    size_h = [Line2D([0], [0], marker="o", linestyle="", markerfacecolor="#9aa4b8",
                     markeredgecolor="white",
                     markersize=(v * SCALE) ** 0.5, label=f"{v} GWh/yr")
              for v in (10, 50, 100)]
    ax.legend(handles=size_h, loc="lower right", bbox_to_anchor=(1.0, -0.02),
              frameon=False, fontsize=10.5, labelcolor=UI["title"], labelspacing=2.4,
              handletextpad=2.2, title="Bubble size", title_fontsize=10.5, borderpad=1.2)

    add_header(fig,
               "China anchors the global map of battery cell manufacturing",
               "Cell manufacturing sites, 2025 — bubble area = nameplate capacity (GWh per year), colour = status",
               title_y=0.955, subtitle_y=0.885)
    add_footer(fig,
               source="Ember Futures battery gigafactory database; Ember analysis",
               note=f"{len(sized)} sites sized by nameplate; {len(nocap)} located sites have no published "
                    f"capacity (open dots); {n_total - len(rows)} sites lack coordinates and are not shown. Most "
                    f"coordinates are city-centroid approximations (flagged in the database), not exact plant points.")

    fig.savefig(OUT, dpi=200, facecolor=UI["background"], bbox_inches="tight")
    print(f"wrote {OUT}  ({len(sized)} sized + {len(nocap)} located-only; max nameplate {maxcap:.0f} GWh)")


if __name__ == "__main__":
    main()
