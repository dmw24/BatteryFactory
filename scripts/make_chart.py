#!/usr/bin/env python3
"""Self-contained Ember-style stacked-column chart (inline SVG) of battery cell
manufacturing capacity ONLINE by year and region, plus announced/UC pipeline."""
import duckdb

OUT = "capacity_chart.html"

con = duckdb.connect("factories.db")
N = con.execute("SELECT count(*) FROM factories").fetchone()[0]
YEARS = list(range(2018, 2031))
REGIONS = ["China", "Europe", "USA", "South Korea", "Japan", "India",
           "Southeast Asia", "Rest of World"]
COLOURS = {
    "China": "#13CE74", "Europe": "#203772", "USA": "#1E609C", "South Korea": "#37A6E6",
    "Japan": "#97CCED", "India": "#553E39", "Southeast Asia": "#857572", "Rest of World": "#B0B7C6",
}
firm = con.execute("""SELECT year, region, round(sum(gwh_firm),0) g FROM capacity_by_year
    WHERE year BETWEEN 2018 AND 2030 GROUP BY year, region""").fetchall()
pipe = con.execute("""SELECT year, round(sum(gwh_pipeline),0) g FROM capacity_by_year
    WHERE year BETWEEN 2018 AND 2030 GROUP BY year""").fetchall()
F = {(y, r): 0.0 for y in YEARS for r in REGIONS}
for y, r, g in firm:
    if r in COLOURS:
        F[(y, r)] = g or 0.0
P = {y: 0.0 for y in YEARS}
for y, g in pipe:
    P[y] = g or 0.0
online_tot = {y: sum(F[(y, r)] for r in REGIONS) for y in YEARS}
con.close()

W, H = 920, 580
ML, MR, MT, MB = 62, 20, 208, 96
plot_w, plot_h = W - ML - MR, H - MT - MB
ymax = 7500
yticks = [0, 1500, 3000, 4500, 6000, 7500]
band = plot_w / len(YEARS)
bw = band * 0.64
def xc(i): return ML + band * i + band / 2
def yo(v): return MT + plot_h - (v / ymax) * plot_h

svg = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" '
       f'aria-label="Battery cell manufacturing capacity online by year and region 2018-2030, with announced pipeline above. '
       f'China dominates the online capacity; a large pipeline sits above it.">']
for t in yticks:
    y = yo(t)
    svg.append(f'<line x1="{ML}" y1="{y:.1f}" x2="{W-MR}" y2="{y:.1f}" class="grid"/>')
    svg.append(f'<text x="{ML-10}" y="{y+4:.1f}" class="ytick" text-anchor="end">{t:,}</text>')
for i, yr in enumerate(YEARS):
    base = 0.0
    x0 = xc(i) - bw / 2
    for r in REGIONS:
        v = F[(yr, r)]
        if v <= 0:
            continue
        svg.append(f'<rect x="{x0:.1f}" y="{yo(base+v):.1f}" width="{bw:.1f}" height="{(yo(base)-yo(base+v)):.1f}" '
                   f'fill="{COLOURS[r]}"><title>{r} online — {yr}: {v:,.0f} GWh/yr</title></rect>')
        base += v
    online_top = base
    pv = P[yr]
    if pv > 0:
        svg.append(f'<rect x="{x0:.1f}" y="{yo(base+pv):.1f}" width="{bw:.1f}" height="{(yo(base)-yo(base+pv)):.1f}" '
                   f'fill="#C4D9E9" fill-opacity="0.55" stroke="#B0B7C6" stroke-width="0.5" stroke-dasharray="2 2">'
                   f'<title>Announced/UC pipeline — {yr}: {pv:,.0f} GWh/yr</title></rect>')
    svg.append(f'<text x="{xc(i):.1f}" y="{yo(online_top)-5:.1f}" class="tot" text-anchor="middle">{online_top/1000:.1f}</text>')
    svg.append(f'<text x="{xc(i):.1f}" y="{MT+plot_h+20:.1f}" class="xtick" text-anchor="middle">{yr}</text>')
svg.append('</svg>')
svg = "\n".join(svg)

legend = "".join(f'<span class="chip"><i style="background:{COLOURS[r]}"></i>{r}</span>' for r in REGIONS)
legend += '<span class="chip"><i style="background:#C4D9E9;opacity:.55;border:1px dashed #B0B7C6"></i>Announced / under-construction pipeline</span>'

html = f"""<div class="wrap">
  <div class="topbar"></div>
  <h1>China dominates the battery cell capacity actually online &ndash; with far more still in the pipeline</h1>
  <p class="sub">Cell manufacturing capacity ONLINE by year (GWh per year), by region, with announced / under-construction pipeline shown above. TWh labels are the online total. 2018&ndash;2030.</p>
  <div class="legend">{legend}</div>
  {svg}
  <p class="foot">&ldquo;Online&rdquo; = capacity from operational/commissioned sources, placed in the year it came online. The 60 largest plants carry <b>real dated, individually-sourced capacity timelines</b>; the remaining plants use phased or single-nameplate figures. Pipeline = announced/under-construction capacity above what is online. No ramps are modelled &ndash; years between sourced points hold the last observed level.</p>
  <p class="src">Source: Ember Futures battery gigafactory database ({N} plants); Ember analysis.</p>
</div>
<style>
  :root {{ --bg:#F5F7FA; --title:#192238; --sub:#3E4860; --tick:#626E88; --grid:#B0B7C6; --card:#F5F7FA; }}
  @media (prefers-color-scheme: dark) {{ :root {{ --bg:#141a2e; --title:#eef2fa; --sub:#aab4cc; --tick:#8c96ac; --grid:#39415c; --card:#1b2237; }} }}
  :root[data-theme="light"] {{ --bg:#F5F7FA; --title:#192238; --sub:#3E4860; --tick:#626E88; --grid:#B0B7C6; --card:#F5F7FA; }}
  :root[data-theme="dark"]  {{ --bg:#141a2e; --title:#eef2fa; --sub:#aab4cc; --tick:#8c96ac; --grid:#39415c; --card:#1b2237; }}
  body {{ margin:0; background:var(--bg); }}
  .wrap {{ max-width:940px; margin:0 auto; padding:20px 22px 26px;
    font-family:'Poppins', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif; background:var(--card); }}
  .topbar {{ width:20%; height:6px; border-radius:3px; margin-bottom:16px; background:linear-gradient(90deg,#203772 0%,#13CE74 100%); }}
  h1 {{ color:var(--title); font-size:21px; font-weight:700; line-height:1.28; margin:0 0 6px; letter-spacing:-0.2px; }}
  .sub {{ color:var(--sub); font-size:13px; line-height:1.4; margin:0 0 14px; }}
  .legend {{ display:flex; flex-wrap:wrap; gap:6px 16px; margin:0 0 8px; }}
  .chip {{ display:inline-flex; align-items:center; gap:6px; color:var(--sub); font-size:12px; }}
  .chip i {{ width:11px; height:11px; border-radius:2px; display:inline-block; }}
  svg {{ display:block; }}
  .grid {{ stroke:var(--grid); stroke-width:1; opacity:.55; }}
  .ytick, .xtick {{ fill:var(--tick); font-size:11px; }}
  .tot {{ fill:var(--title); font-size:10.5px; font-weight:700; }}
  .foot, .src {{ color:var(--tick); font-size:10.5px; line-height:1.4; margin:10px 0 0; }}
  .src {{ margin-top:6px; }}
  text {{ font-family:'Poppins', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif; }}
</style>"""
open(OUT, "w").write(html)
print(f"wrote {OUT}; online totals TWh:", {y: round(online_tot[y]/1000, 2) for y in YEARS})
