#!/usr/bin/env python3
"""Build a single self-contained HTML dashboard of battery gigafactory insights.

Fully offline / no CDN: all CSS + charts are inline SVG, the world map is drawn
from the bundled data/world.geo.json. Sections: headline stats, world map,
capacity online over time by region (with IEA/BNEF overlay), top owners, chemistry
and end-market splits, status x region, and the largest plants. Ember house style,
theme-aware (light/dark).

Run: python3 scripts/build_report.py  ->  report.html
"""
import csv
import json
import re
import duckdb

DB = "factories.db"
OUT = "report.html"
WORLD = "data/world.geo.json"
YEARS = list(range(2018, 2031))
REGIONS = ["China", "Europe", "USA", "South Korea", "Japan", "India",
           "Southeast Asia", "Rest of World"]
RCOL = {"China": "#13CE74", "Europe": "#203772", "USA": "#1E609C", "South Korea": "#37A6E6",
        "Japan": "#97CCED", "India": "#553E39", "Southeast Asia": "#857572", "Rest of World": "#B0B7C6"}
SCOL = {"operational": "#13CE74", "under_construction": "#37A6E6",
        "announced": "#203772", None: "#8792A6"}

con = duckdb.connect(DB)


def q(sql):
    return con.execute(sql).fetchall()


# ---------- owner normalisation (merge spelling variants of big groups) ----------
def owner(name):
    s = (name or "").lower()
    for key, label in [
        ("catl", "CATL"), ("contemporary amperex", "CATL"),
        ("byd", "BYD / FinDreams"), ("findreams", "BYD / FinDreams"), ("fudi", "BYD / FinDreams"),
        ("calb", "CALB"), ("eve", "EVE Energy"), ("gotion", "Gotion High-tech"),
        ("svolt", "SVOLT"), ("sunwoda", "Sunwoda"), ("envision", "Envision AESC"),
        ("lg energy", "LG Energy Solution"), ("samsung", "Samsung SDI"), ("sk on", "SK On"),
        ("panasonic", "Panasonic"), ("tesla", "Tesla"), ("northvolt", "Northvolt"),
        ("farasis", "Farasis"), ("rept", "REPT Battero"), ("great power", "Great Power"),
        ("lishen", "Lishen"), ("bak", "BAK"), ("acc", "ACC"), ("powerco", "PowerCo / VW"),
        ("volkswagen", "PowerCo / VW"), ("ford", "Ford"), ("hli", "HLI (Hyundai-LG)"),
        ("blueoval", "BlueOval SK"), ("verkor", "Verkor"), ("automotive cells", "ACC"),
    ]:
        if key in s:
            return label
    # else use the raw name trimmed of legal suffixes
    return re.sub(r"\s*(co\.?,?\s*(ltd|limited).*|inc\.?|group|corp.*|gmbh|se|s\.a\.).*$", "",
                  name or "", flags=re.I).strip() or (name or "?")


# ---------- SVG helpers ----------
def hbars(data, unit="GWh/yr", w=520, rowh=26, pad_left=170, colour="#13CE74", maxv=None):
    """Horizontal bar chart from [(label, value), ...]."""
    if not data:
        return ""
    maxv = maxv or max(v for _, v in data)
    h = rowh * len(data) + 10
    plotw = w - pad_left - 60
    out = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img">']
    for i, (lab, v) in enumerate(data):
        y = i * rowh + 6
        bw = (v / maxv) * plotw if maxv else 0
        out.append(f'<text x="{pad_left-8}" y="{y+rowh/2-2}" class="blab" text-anchor="end">{lab}</text>')
        out.append(f'<rect x="{pad_left}" y="{y}" width="{bw:.1f}" height="{rowh-9}" fill="{colour}" rx="2"><title>{lab}: {v:,.0f} {unit}</title></rect>')
        out.append(f'<text x="{pad_left+bw+5:.1f}" y="{y+rowh/2-2}" class="bval">{v:,.0f}</text>')
    out.append("</svg>")
    return "\n".join(out)


def stacked_time():
    """Stacked columns of online capacity by region 2018-2030, + nameplate line + IEA/BNEF."""
    firm = {(y, r): 0.0 for y in YEARS for r in REGIONS}
    for y, r, g in q("""SELECT year, region, sum(gwh_firm) FROM capacity_by_year
        WHERE year BETWEEN 2018 AND 2030 GROUP BY 1,2"""):
        if r in RCOL:
            firm[(y, r)] = g or 0.0
    npl = dict(q("""SELECT year, sum(gwh_nameplate) FROM capacity_by_year
        WHERE year BETWEEN 2018 AND 2030 GROUP BY 1"""))
    bench = {"IEA": {}, "BNEF": {}}
    try:
        for row in csv.DictReader(l for l in open("scripts/benchmarks.csv") if not l.startswith("#")):
            if row["source"] in bench:
                bench[row["source"]][int(row["year"])] = float(row["gwh"]) / 1000
    except OSError:
        pass
    W, H, ML, MR, MT, MB = 900, 430, 44, 16, 16, 40
    pw, ph = W - ML - MR, H - MT - MB
    ymax = 6.0
    band = pw / len(YEARS)
    bw = band * 0.66
    def xc(i): return ML + band * i + band / 2
    def yo(v): return MT + ph - (v / ymax) * ph
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img">']
    for t in [0, 1.5, 3, 4.5, 6]:
        s.append(f'<line x1="{ML}" y1="{yo(t):.1f}" x2="{W-MR}" y2="{yo(t):.1f}" class="grid"/>')
        s.append(f'<text x="{ML-6}" y="{yo(t)+4:.1f}" class="ytick" text-anchor="end">{t:g}</text>')
    for i, yr in enumerate(YEARS):
        base = 0.0
        x0 = xc(i) - bw / 2
        for r in REGIONS:
            v = firm[(yr, r)] / 1000
            if v <= 0:
                continue
            s.append(f'<rect x="{x0:.1f}" y="{yo(base+v):.1f}" width="{bw:.1f}" height="{yo(base)-yo(base+v):.1f}" fill="{RCOL[r]}"><title>{r} {yr}: {v*1000:,.0f} GWh/yr online</title></rect>')
            base += v
        s.append(f'<text x="{xc(i):.1f}" y="{yo(base)-4:.1f}" class="tot" text-anchor="middle">{base:.1f}</text>')
        s.append(f'<text x="{xc(i):.1f}" y="{H-MB+16:.1f}" class="xtick" text-anchor="middle">{yr}</text>')
    # nameplate faint line
    pts = " ".join(f"{xc(i):.1f},{yo(min(npl.get(yr,0)/1000,ymax)):.1f}" for i, yr in enumerate(YEARS))
    s.append(f'<polyline points="{pts}" fill="none" stroke="#B0B7C6" stroke-width="1.3" stroke-dasharray="2 2"/>')
    # benchmarks
    for src, mk in (("BNEF", "diamond"), ("IEA", "circle")):
        p = sorted((YEARS.index(y), g) for y, g in bench[src].items() if y in YEARS)
        if len(p) > 1:
            s.append(f'<polyline points="{" ".join(f"{xc(i):.1f},{yo(g):.1f}" for i,g in p)}" fill="none" stroke="#E9A21B" stroke-width="2"/>')
        for i, g in p:
            if mk == "circle":
                s.append(f'<circle cx="{xc(i):.1f}" cy="{yo(g):.1f}" r="4.5" fill="#E9A21B" stroke="#7a5300"><title>{src} {YEARS[i]}: {g:.2f} TWh</title></circle>')
            else:
                s.append(f'<rect x="{xc(i)-4:.1f}" y="{yo(g)-4:.1f}" width="8" height="8" fill="none" stroke="#E9A21B" stroke-width="2" transform="rotate(45 {xc(i):.1f} {yo(g):.1f})"><title>{src} {YEARS[i]}: {g:.2f} TWh</title></rect>')
        if p:
            s.append(f'<text x="{xc(p[-1][0])+8:.1f}" y="{yo(p[-1][1])+4:.1f}" class="blab" fill="#8a6300">{src}</text>')
    s.append("</svg>")
    return "\n".join(s)


def world_map():
    """Equirectangular inline-SVG world map with capacity bubbles."""
    W, H = 900, 470
    LAT0, LAT1 = 83, -56
    def X(lon): return (lon + 180) / 360 * W
    def Y(lat): return (LAT0 - lat) / (LAT0 - LAT1) * H
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="World map of battery cell factories, bubble size by nameplate capacity, colour by status">']
    s.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="var(--ocean)"/>')
    feats = json.load(open(WORLD))["features"]
    for f in feats:
        g = f["geometry"]
        rings = ([g["coordinates"][0]] if g["type"] == "Polygon"
                 else [p[0] for p in g["coordinates"]] if g["type"] == "MultiPolygon" else [])
        for ring in rings:
            d = "M" + " L".join(f"{X(lon):.1f},{Y(lat):.1f}" for lon, lat in ring) + "Z"
            s.append(f'<path d="{d}" class="land"/>')
    rows = q("""SELECT plant_name, status, latitude, longitude, nameplate_capacity_gwh
        FROM factories WHERE latitude IS NOT NULL AND longitude IS NOT NULL
        ORDER BY nameplate_capacity_gwh DESC NULLS LAST""")
    maxc = max((r[4] or 0) for r in rows)
    import math
    for name, st, lat, lon, cap in rows:
        x, y = X(lon), Y(lat)
        if cap:
            r = max(2.0, math.sqrt(cap / maxc) * 22)
            c = SCOL.get(st, SCOL[None])
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{c}" fill-opacity="0.62" stroke="#fff" stroke-width="0.4"><title>{name} — {cap:,.0f} GWh/yr ({st or "?"})</title></circle>')
        else:
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="none" stroke="#8792A6" stroke-width="0.7"><title>{name} — capacity not published</title></circle>')
    s.append("</svg>")
    return "\n".join(s)


# ---------- gather stats ----------
tot_sites = q("SELECT count(*) FROM factories")[0][0]
by_status = dict(q("SELECT status, count(*) FROM factories GROUP BY 1"))
op_cap = q("SELECT round(sum(nameplate_capacity_gwh)) FROM factories WHERE status='operational'")[0][0] or 0
tot_cap = q("SELECT round(sum(nameplate_capacity_gwh)) FROM factories")[0][0] or 0
n_countries = q("SELECT count(DISTINCT country) FROM factories")[0][0]
china_share = q("""SELECT round(100.0*sum(CASE WHEN region='China' THEN nameplate_capacity_gwh ELSE 0 END)
    / nullif(sum(nameplate_capacity_gwh),0)) FROM factories""")[0][0] or 0
online25 = q("SELECT round(sum(gwh_firm)) FROM capacity_by_year WHERE year=2025")[0][0] or 0

# owners
own = {}
for pc, cap in q("""SELECT coalesce(parent_company, operator), nameplate_capacity_gwh FROM factories
        WHERE nameplate_capacity_gwh IS NOT NULL"""):
    own[owner(pc)] = own.get(owner(pc), 0) + cap
top_owners = sorted(own.items(), key=lambda kv: -kv[1])[:12]

# chemistry buckets
def chem_bucket(c):
    s = (c or "").lower()
    has_lfp = "lfp" in s or "lithium iron" in s or "iron phosphate" in s
    has_nmc = "nmc" in s or "ncm" in s or "ternary" in s
    if "sodium" in s or "na-ion" in s or "sodium-ion" in s:
        return "Sodium-ion"
    if "solid" in s:
        return "Solid-state"
    if has_lfp and has_nmc:
        return "LFP + NMC"
    if has_lfp:
        return "LFP"
    if has_nmc or "nca" in s:
        return "NMC / NCA"
    return "Other / unspecified"
chem = {}
for c, cap in q("SELECT chemistry, nameplate_capacity_gwh FROM factories"):
    b = chem_bucket(c)
    chem[b] = chem.get(b, 0) + (cap or 0)
chem_rows = sorted(chem.items(), key=lambda kv: -kv[1])

# end market (free-text -> clean buckets)
def em_bucket(e):
    s = (e or "").lower()
    if not s:
        return "Unspecified"
    ev = "ev" in s or "vehicle" in s or "automotive" in s or "power batter" in s
    ess = "ess" in s or "energy storage" in s or "stationary" in s or "grid" in s or "bess" in s
    if s == "mixed" or (ev and ess):
        return "Mixed (EV+ESS)"
    if ev:
        return "EV"
    if ess:
        return "ESS"
    if "consumer" in s or "electronics" in s or "device" in s:
        return "Consumer"
    return "Other"
em = {}
for e, cap in q("SELECT end_market, nameplate_capacity_gwh FROM factories"):
    b = em_bucket(e)
    em[b] = em.get(b, 0) + (cap or 0)
em_rows = sorted(em.items(), key=lambda kv: -kv[1])

# region x status matrix (nameplate)
regmat = {}
for r, st, cap in q("""SELECT region, status, sum(nameplate_capacity_gwh) FROM factories GROUP BY 1,2"""):
    regmat.setdefault(r, {})[st] = cap or 0
reg_order = sorted(regmat, key=lambda r: -sum(regmat[r].values()))

# top plants
top_plants = q("""SELECT plant_name, operator, country, status, round(nameplate_capacity_gwh)
    FROM factories WHERE nameplate_capacity_gwh IS NOT NULL
    ORDER BY nameplate_capacity_gwh DESC LIMIT 15""")

# ---------- render sections ----------
def stat(v, lab):
    return f'<div class="stat"><div class="statv">{v}</div><div class="statl">{lab}</div></div>'

stats = "".join([
    stat(f"{tot_sites}", "cell manufacturing sites"),
    stat(f"{n_countries}", "countries"),
    stat(f"{op_cap:,.0f}", "GWh/yr operational nameplate"),
    stat(f"{online25/1000:.1f} TWh", "online in 2025 (sourced floor)"),
    stat(f"{china_share:.0f}%", "of nameplate is in China"),
])

reg_legend = "".join(f'<span class="chip"><i style="background:{RCOL[r]}"></i>{r}</span>' for r in REGIONS)
reg_legend += ('<span class="chip"><i class="dash"></i>Installed nameplate</span>'
               '<span class="chip"><i class="iea"></i>IEA</span><span class="chip"><i class="bnef"></i>BNEF</span>')
map_legend = "".join(f'<span class="chip"><i style="background:{SCOL[k]}"></i>{l}</span>'
                     for k, l in [("operational", "Operational"), ("under_construction", "Under construction"),
                                  ("announced", "Announced")])
map_legend += '<span class="chip"><i class="hollow"></i>Capacity not published</span>'

owners_svg = hbars([(k, v) for k, v in top_owners], colour="#13CE74")
chem_svg = hbars(chem_rows, colour="#1E609C", pad_left=150)
em_svg = hbars(em_rows, colour="#37A6E6", pad_left=128)

# region x status table
def cell(v):
    return f"{v:,.0f}" if v else "&ndash;"
regtbl = ['<table class="tbl"><thead><tr><th>Region</th><th>Operational</th><th>Under constr.</th><th>Announced</th><th>Total</th></tr></thead><tbody>']
for r in reg_order:
    m = regmat[r]
    tot = sum(m.values())
    regtbl.append(f'<tr><td>{r}</td><td>{cell(m.get("operational",0))}</td><td>{cell(m.get("under_construction",0))}</td><td>{cell(m.get("announced",0))}</td><td class="b">{tot:,.0f}</td></tr>')
regtbl.append("</tbody></table>")
regtbl = "".join(regtbl)

plantstbl = ['<table class="tbl"><thead><tr><th>Plant</th><th>Operator</th><th>Country</th><th>Status</th><th>GWh/yr</th></tr></thead><tbody>']
for name, op, country, st, cap in top_plants:
    plantstbl.append(f'<tr><td>{name}</td><td>{op}</td><td>{country}</td><td>{(st or "?").replace("_"," ")}</td><td class="b">{cap:,.0f}</td></tr>')
plantstbl.append("</tbody></table>")
plantstbl = "".join(plantstbl)

html = f"""<!-- generated by scripts/build_report.py -->
<div class="wrap">
  <div class="topbar"></div>
  <h1>The global battery cell manufacturing landscape</h1>
  <p class="sub">Ember Futures gigafactory database &ndash; {tot_sites} cell manufacturing sites worldwide. Capacity in GWh per year (nameplate unless stated); 2018&ndash;2030.</p>
  <div class="stats">{stats}</div>

  <section><h2>Where the factories are</h2>
    <p class="cap">Every located site; bubble area = nameplate capacity, colour = status. Most coordinates are city-centroid approximations.</p>
    <div class="legend">{map_legend}</div>
    {world_map()}
  </section>

  <section><h2>Capacity online over time, by region</h2>
    <p class="cap">Bars = capacity <b>online</b> (dated, sourced operational figures), stacked by region; labels are the TWh total. Amber = IEA/BNEF reported nameplate; faint dotted = full installed nameplate (upper bound).</p>
    <div class="legend">{reg_legend}</div>
    {stacked_time()}
  </section>

  <div class="grid2">
    <section><h2>Biggest owners</h2>
      <p class="cap">Total nameplate GWh/yr by parent group (variants merged).</p>
      {owners_svg}</section>
    <section><h2>By chemistry</h2>
      <p class="cap">Nameplate GWh/yr by cell chemistry.</p>
      {chem_svg}
      <h2 style="margin-top:18px">By end market</h2>
      {em_svg}</section>
  </div>

  <div class="grid2">
    <section><h2>Capacity by region &amp; status</h2>
      <p class="cap">Nameplate GWh/yr &ndash; never summed across status.</p>
      {regtbl}</section>
    <section><h2>Largest plants</h2>
      <p class="cap">Top 15 by nameplate capacity.</p>
      {plantstbl}</section>
  </div>

  <p class="src">Source: Ember Futures battery gigafactory database ({tot_sites} plants); IEA; BloombergNEF. Ember analysis. Capacity is annual GWh/year at nameplate; online series counts only dated, sourced operational capacity. Figures never summed across status.</p>
</div>
<style>
  :root {{ --bg:#F5F7FA; --card:#FFFFFF; --title:#192238; --sub:#3E4860; --tick:#626E88; --grid:#D9DEE8; --line:#E4E8EF; --ocean:#EEF2F7; --land:#E4E8EF; }}
  @media (prefers-color-scheme: dark) {{ :root {{ --bg:#10162a; --card:#171e33; --title:#eef2fa; --sub:#aab4cc; --tick:#8c96ac; --grid:#2a3350; --line:#2a3350; --ocean:#141b30; --land:#28314c; }} }}
  :root[data-theme="light"] {{ --bg:#F5F7FA; --card:#FFFFFF; --title:#192238; --sub:#3E4860; --tick:#626E88; --grid:#D9DEE8; --line:#E4E8EF; --ocean:#EEF2F7; --land:#E4E8EF; }}
  :root[data-theme="dark"] {{ --bg:#10162a; --card:#171e33; --title:#eef2fa; --sub:#aab4cc; --tick:#8c96ac; --grid:#2a3350; --line:#2a3350; --ocean:#141b30; --land:#28314c; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); }}
  .wrap {{ max-width:960px; margin:0 auto; padding:22px 22px 40px; font-family:'Poppins',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif; }}
  .topbar {{ width:20%; height:6px; border-radius:3px; margin-bottom:16px; background:linear-gradient(90deg,#203772,#13CE74); }}
  h1 {{ color:var(--title); font-size:25px; font-weight:700; margin:0 0 6px; letter-spacing:-0.3px; }}
  h2 {{ color:var(--title); font-size:16px; font-weight:700; margin:0 0 4px; }}
  .sub {{ color:var(--sub); font-size:13.5px; margin:0 0 18px; line-height:1.45; }}
  .cap {{ color:var(--tick); font-size:11.5px; margin:0 0 10px; line-height:1.4; }}
  .stats {{ display:flex; flex-wrap:wrap; gap:10px; margin:0 0 26px; }}
  .stat {{ flex:1 1 150px; background:var(--card); border:1px solid var(--line); border-radius:10px; padding:14px 16px; }}
  .statv {{ color:var(--title); font-size:23px; font-weight:700; letter-spacing:-0.5px; }}
  .statl {{ color:var(--tick); font-size:11.5px; margin-top:3px; }}
  section {{ background:var(--card); border:1px solid var(--line); border-radius:12px; padding:18px 18px 14px; margin:0 0 18px; }}
  .grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; }}
  @media (max-width:720px) {{ .grid2 {{ grid-template-columns:1fr; }} }}
  .legend {{ display:flex; flex-wrap:wrap; gap:5px 14px; margin:0 0 8px; }}
  .chip {{ display:inline-flex; align-items:center; gap:6px; color:var(--sub); font-size:11.5px; }}
  .chip i {{ width:11px; height:11px; border-radius:2px; display:inline-block; }}
  .chip i.dash {{ width:18px; height:0; border-top:2px dashed #B0B7C6; }}
  .chip i.iea {{ border-radius:50%; background:#E9A21B; }}
  .chip i.bnef {{ background:transparent; border:2px solid #E9A21B; transform:rotate(45deg); width:9px; height:9px; }}
  .chip i.hollow {{ background:transparent; border:1.5px solid #8792A6; border-radius:50%; }}
  svg {{ display:block; width:100%; height:auto; }}
  .land {{ fill:var(--land); stroke:var(--card); stroke-width:0.4; }}
  .grid {{ stroke:var(--grid); stroke-width:1; }}
  .ytick,.xtick {{ fill:var(--tick); font-size:11px; }}
  .tot {{ fill:var(--title); font-size:10px; font-weight:700; }}
  .blab {{ fill:var(--sub); font-size:11.5px; }}
  .bval {{ fill:var(--tick); font-size:11px; }}
  .tbl {{ width:100%; border-collapse:collapse; font-size:12px; }}
  .tbl th {{ text-align:right; color:var(--tick); font-weight:600; padding:5px 6px; border-bottom:1px solid var(--line); font-size:11px; }}
  .tbl th:first-child {{ text-align:left; }}
  .tbl td {{ text-align:right; color:var(--sub); padding:5px 6px; border-bottom:1px solid var(--line); }}
  .tbl td:first-child {{ text-align:left; color:var(--title); max-width:220px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
  .tbl td.b {{ color:var(--title); font-weight:700; }}
  .src {{ color:var(--tick); font-size:10.5px; line-height:1.45; margin:14px 0 0; }}
</style>"""

con.close()
open(OUT, "w").write(html)
print(f"wrote {OUT} ({len(html)//1024} KB); sites={tot_sites}, owners={len(top_owners)}, chem={len(chem_rows)}")
