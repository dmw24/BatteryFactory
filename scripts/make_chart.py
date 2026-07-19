#!/usr/bin/env python3
"""Generate a self-contained Ember-style stacked-column chart (inline SVG)
of battery cell manufacturing capacity online by year and region."""
import duckdb

OUT = "capacity_chart.html"

con = duckdb.connect("factories.db")
YEARS = list(range(2018, 2031))
# stacking order (bottom -> top): China first (largest), then by size
REGIONS = ["China", "Europe", "USA", "South Korea", "Japan", "India",
           "Southeast Asia", "Rest of World"]
COLOURS = {
    "China":          "#13CE74",  # Ember green — the story/highlight
    "Europe":         "#203772",  # navy
    "USA":            "#1E609C",  # mid blue
    "South Korea":    "#37A6E6",  # light blue
    "Japan":          "#97CCED",  # pale blue
    "India":          "#553E39",  # brown (accessible with green/blue)
    "Southeast Asia": "#857572",  # mid brown
    "Rest of World":  "#B0B7C6",  # grey
}

rows = con.execute("""SELECT year, region, round(sum(gwh_online),0) g
    FROM capacity_by_year WHERE year BETWEEN 2018 AND 2030 GROUP BY year, region""").fetchall()
D = {(y, r): 0.0 for y in YEARS for r in REGIONS}
for y, r, g in rows:
    if r in COLOURS:
        D[(y, r)] = g or 0.0
totals = {y: sum(D[(y, r)] for r in REGIONS) for y in YEARS}
con.close()

# ---- geometry ----
W, H = 920, 560
ML, MR, MT, MB = 60, 20, 196, 96          # margins (big top for title/legend)
plot_w = W - ML - MR
plot_h = H - MT - MB
ymax = 6500
yticks = [0, 1500, 3000, 4500, 6000]
n = len(YEARS)
band = plot_w / n
bw = band * 0.62

def x_center(i): return ML + band * i + band / 2
def y_of(v): return MT + plot_h - (v / ymax) * plot_h

svg = []
svg.append(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" '
           f'aria-label="Stacked column chart of battery cell manufacturing capacity online by year and region, 2018 to 2030. '
           f'China dominates but its share falls from about 85 percent in 2023 to about 56 percent by 2030 as the US and Europe scale.">')

# gridlines + y tick labels
for t in yticks:
    y = y_of(t)
    svg.append(f'<line x1="{ML}" y1="{y:.1f}" x2="{W-MR}" y2="{y:.1f}" class="grid"/>')
    svg.append(f'<text x="{ML-10}" y="{y+4:.1f}" class="ytick" text-anchor="end">{t:,}</text>')

# stacked bars (data in front of gridlines)
for i, yr in enumerate(YEARS):
    base = 0.0
    cx = x_center(i)
    x0 = cx - bw / 2
    for r in REGIONS:
        v = D[(yr, r)]
        if v <= 0:
            continue
        y1 = y_of(base + v)
        y0 = y_of(base)
        pipeline = yr >= 2026
        op = ' opacity="0.62"' if pipeline else ''
        svg.append(f'<rect x="{x0:.1f}" y="{y1:.1f}" width="{bw:.1f}" height="{(y0-y1):.1f}" '
                   f'fill="{COLOURS[r]}"{op}><title>{r} — {yr}: {v:,.0f} GWh/yr</title></rect>')
        base += v
    # total label above each column
    svg.append(f'<text x="{cx:.1f}" y="{y_of(base)-6:.1f}" class="tot" text-anchor="middle">'
               f'{base/1000:.1f}</text>')
    # x tick label
    svg.append(f'<text x="{cx:.1f}" y="{MT+plot_h+20:.1f}" class="xtick" text-anchor="middle">{yr}</text>')

# divider marking pipeline (between 2025 and 2026)
xdiv = ML + band * (YEARS.index(2026))
svg.append(f'<line x1="{xdiv:.1f}" y1="{MT}" x2="{xdiv:.1f}" y2="{MT+plot_h}" class="divider"/>')
svg.append(f'<text x="{xdiv+6:.1f}" y="{MT+14:.1f}" class="note">← online &nbsp;·&nbsp; pipeline →</text>')
svg.append('</svg>')
svg = "\n".join(svg)

# legend chips
legend = "".join(
    f'<span class="chip"><i style="background:{COLOURS[r]}"></i>{r}</span>' for r in REGIONS
)

html = f"""<div class="wrap">
  <div class="topbar"></div>
  <h1>China still makes most of the world's battery cells &ndash; but its share slips from ~85% to ~56% as the US and Europe scale</h1>
  <p class="sub">Battery cell manufacturing capacity online by year (GWh per year), by region, 2018&ndash;2030. Numbers above bars are the global total in TWh per year.</p>
  <div class="legend">{legend}</div>
  {svg}
  <p class="foot">2026 onward (paler bars, right of the divider) reflects announced and under-construction plants placed in their expected first-production year &ndash; a coverage floor, not a forecast. Capacity is placed in the year each plant comes online, so a given year only includes plants online by then; this is not a cross-status nameplate sum.</p>
  <p class="src">Source: Ember Futures battery gigafactory database (340 plants); Ember analysis.</p>
</div>
<style>
  :root {{
    --bg:#F5F7FA; --title:#192238; --sub:#3E4860; --tick:#626E88; --grid:#B0B7C6; --card:#F5F7FA;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg:#141a2e; --title:#eef2fa; --sub:#aab4cc; --tick:#8c96ac; --grid:#39415c; --card:#1b2237; }}
  }}
  :root[data-theme="light"] {{ --bg:#F5F7FA; --title:#192238; --sub:#3E4860; --tick:#626E88; --grid:#B0B7C6; --card:#F5F7FA; }}
  :root[data-theme="dark"]  {{ --bg:#141a2e; --title:#eef2fa; --sub:#aab4cc; --tick:#8c96ac; --grid:#39415c; --card:#1b2237; }}
  body {{ margin:0; background:var(--bg); }}
  .wrap {{ max-width:940px; margin:0 auto; padding:20px 22px 26px;
    font-family:'Poppins', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif; background:var(--card); }}
  .topbar {{ width:20%; height:6px; border-radius:3px; margin-bottom:16px;
    background:linear-gradient(90deg,#203772 0%,#13CE74 100%); }}
  h1 {{ color:var(--title); font-size:21px; font-weight:700; line-height:1.28; margin:0 0 6px; letter-spacing:-0.2px; }}
  .sub {{ color:var(--sub); font-size:13px; line-height:1.4; margin:0 0 14px; }}
  .legend {{ display:flex; flex-wrap:wrap; gap:6px 16px; margin:0 0 8px; }}
  .chip {{ display:inline-flex; align-items:center; gap:6px; color:var(--sub); font-size:12px; }}
  .chip i {{ width:11px; height:11px; border-radius:2px; display:inline-block; }}
  svg {{ display:block; }}
  .grid {{ stroke:var(--grid); stroke-width:1; opacity:.55; }}
  .divider {{ stroke:var(--tick); stroke-width:1; stroke-dasharray:3 3; opacity:.6; }}
  .ytick, .xtick {{ fill:var(--tick); font-size:11px; }}
  .note {{ fill:var(--tick); font-size:10.5px; }}
  .tot {{ fill:var(--title); font-size:11px; font-weight:700; }}
  .foot, .src {{ color:var(--tick); font-size:10.5px; line-height:1.4; margin:10px 0 0; }}
  .src {{ margin-top:6px; }}
  text {{ font-family:'Poppins', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif; }}
</style>"""

open(OUT, "w").write(html)
print(f"wrote {OUT}")
print("year totals (TWh):", {y: round(totals[y]/1000, 2) for y in YEARS})
