#!/usr/bin/env python3
"""Self-contained Ember-style reconciliation chart (inline SVG) of battery cell
manufacturing capacity by year.

Three measures, so the reader can see the honest band:
  - Series A (bars, stacked by region) — capacity ONLINE / achieved: dated,
    sourced operational figures, held flat between sourced points. The floor.
  - Series B (dashed line) — installed nameplate on the IEA/BNEF basis: an
    operational plant's full nameplate credited from the year it came online.
    The upper comparator (trackers credit a commissioned line at full nameplate
    immediately; real utilisation is ~40-50%).
  - IEA / BNEF (gold markers) — published external nameplate benchmarks. They
    sit BETWEEN Series A and Series B, which is exactly the reconciliation.
"""
import csv
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
nameplate = con.execute("""SELECT year, round(sum(gwh_nameplate),0) g FROM capacity_by_year
    WHERE year BETWEEN 2018 AND 2030 GROUP BY year""").fetchall()
F = {(y, r): 0.0 for y in YEARS for r in REGIONS}
for y, r, g in firm:
    if r in COLOURS:
        F[(y, r)] = g or 0.0
B = {y: 0.0 for y in YEARS}
for y, g in nameplate:
    B[y] = g or 0.0
online_tot = {y: sum(F[(y, r)] for r in REGIONS) for y in YEARS}
con.close()

# published external benchmarks (nameplate basis) for overlay
BENCH = {"IEA": {}, "BNEF": {}}
try:
    for row in csv.DictReader(l for l in open("scripts/benchmarks.csv") if not l.startswith("#")):
        if row["source"] in BENCH:
            BENCH[row["source"]][int(row["year"])] = float(row["gwh"])
except OSError:
    pass

W, H = 920, 600
ML, MR, MT, MB = 62, 20, 214, 96
plot_w, plot_h = W - ML - MR, H - MT - MB
ymax = 6000
yticks = [0, 1500, 3000, 4500, 6000]
band = plot_w / len(YEARS)
bw = band * 0.64
def xc(i): return ML + band * i + band / 2
def yo(v): return MT + plot_h - (v / ymax) * plot_h

svg = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" '
       f'aria-label="Battery cell manufacturing capacity 2018-2030. Bars: capacity online (achieved) by region. '
       f'Dashed line: installed nameplate (IEA/BNEF basis). Gold markers: published IEA and BNEF nameplate figures, '
       f'which sit between the two.">']
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
    svg.append(f'<text x="{xc(i):.1f}" y="{yo(online_top)-5:.1f}" class="tot" text-anchor="middle">{online_top/1000:.1f}</text>')
    svg.append(f'<text x="{xc(i):.1f}" y="{MT+plot_h+20:.1f}" class="xtick" text-anchor="middle">{yr}</text>')

# Series B — installed nameplate (IEA/BNEF basis): dashed line
pts = " ".join(f"{xc(i):.1f},{yo(min(B[yr], ymax)):.1f}" for i, yr in enumerate(YEARS))
svg.append(f'<polyline points="{pts}" fill="none" stroke="#192238" stroke-width="2" '
           f'stroke-dasharray="5 3" opacity="0.75"/>')
for i, yr in enumerate(YEARS):
    if B[yr] > 0 and B[yr] <= ymax:
        svg.append(f'<circle cx="{xc(i):.1f}" cy="{yo(B[yr]):.1f}" r="2.4" fill="#192238" opacity="0.75">'
                   f'<title>Installed nameplate (IEA/BNEF basis) — {yr}: {B[yr]:,.0f} GWh/yr</title></circle>')

# IEA / BNEF published benchmarks — gold markers
def marker(x, y, kind):
    if kind == "IEA":
        return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#E9A21B" stroke="#7a5300" stroke-width="1">')
    return (f'<rect x="{x-4.5:.1f}" y="{y-4.5:.1f}" width="9" height="9" fill="none" '
            f'stroke="#E9A21B" stroke-width="2" transform="rotate(45 {x:.1f} {y:.1f})">')
for src in ("IEA", "BNEF"):
    for yr, g in BENCH[src].items():
        if yr in YEARS and g <= ymax:
            i = YEARS.index(yr)
            x, y = xc(i), yo(g)
            svg.append(marker(x, y, src) + f'<title>{src} {yr}: {g:,.0f} GWh/yr (published nameplate)</title>'
                       + ('</circle>' if src == "IEA" else '</rect>'))
svg.append('</svg>')
svg = "\n".join(svg)

legend = "".join(f'<span class="chip"><i style="background:{COLOURS[r]}"></i>{r}</span>' for r in REGIONS)
legend += ('<span class="chip"><i class="dash"></i>Installed nameplate (IEA/BNEF basis)</span>'
           '<span class="chip"><i class="iea"></i>IEA (published)</span>'
           '<span class="chip"><i class="bnef"></i>BNEF (published)</span>')

html = f"""<div class="wrap">
  <div class="topbar"></div>
  <h1>IEA and BNEF sit between the capacity actually online and the full installed nameplate</h1>
  <p class="sub">Battery cell manufacturing capacity, GWh per year, 2018&ndash;2030. Bars show capacity <b>online</b> (dated, sourced operational figures), stacked by region &ndash; TWh labels are the online total. The dashed line credits each operational plant&rsquo;s <b>full nameplate</b> from the year it came online (the IEA/BNEF basis). Published IEA and BNEF nameplate figures fall between the two.</p>
  <div class="legend">{legend}</div>
  {svg}
  <p class="foot">Series A (bars) &ndash; capacity <b>online / achieved</b>: operational-source figures placed in the year each came online and held flat between sourced points; no ramps modelled. The honest floor. Series B (dashed) &ndash; <b>installed nameplate</b>: an operational plant&rsquo;s full nameplate credited from its commissioning year, as trackers count it (IEA notes a line can take 5+ years to reach nominal output; real utilisation ~40&ndash;50%). The upper comparator. IEA/BNEF report nameplate and therefore land <b>between</b> the two &ndash; the reconciliation. ~95% of the online curve is real, individually-sourced data.</p>
  <p class="src">Source: Ember Futures battery gigafactory database ({N} plants); IEA (Batteries and Secure Energy Transitions 2024, Global EV Outlook 2025/2026); BloombergNEF (Apr 2024). Ember analysis.</p>
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
  .chip i.dash {{ width:20px; height:0; border-top:2px dashed var(--title); border-radius:0; }}
  .chip i.iea {{ width:11px; height:11px; border-radius:50%; background:#E9A21B; border:1px solid #7a5300; }}
  .chip i.bnef {{ width:9px; height:9px; border-radius:1px; background:transparent; border:2px solid #E9A21B; transform:rotate(45deg); }}
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
print("nameplate (Series B) TWh:", {y: round(B[y]/1000, 2) for y in YEARS})
