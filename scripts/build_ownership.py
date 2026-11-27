#!/usr/bin/env python3
"""Capacity by the battery maker's headquarters (owner upgrade list item 6, 2026-11-27).

Classifies each plant by the HQ of the cell maker that runs it (operator, else parent), by keyword. JVs between a
battery maker and an automaker are assigned to the battery maker (IEA instead splits JVs by ownership share — a known
difference). Writes capacity_by_hq.csv: year × HQ × plant region, built nameplate (D) and producing (C).
"""
import csv
import os
import re
from collections import defaultdict

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
RULES = [  # (regex on operator + parent, HQ) — first match wins; battery makers before automakers
    (r"\blg\b|lg energy|lg chem|ultium|l-h battery|hl-ga|nextstar", "South Korea"),
    (r"samsung|starplus", "South Korea"),
    (r"\bsk\b|sk on|sk innovation|blueoval|skoj|skoy|besk|hyundai-sk", "South Korea"),
    (r"panasonic|prime planet|ppes|toyota|gs yuasa|blue energy|murata|maxell|toshiba|aesc japan|vehicle energy|"
     r"honda|nissan|lithium energy japan|eliiy|fdk|softbank|kyocera|tdk", "Japan"),
    (r"envision|aesc", "China"),
    (r"catl|contemporary amperex|byd|findreams|gotion|guoxuan|eve energy|eve power|sunwoda|calb|svolt|rept|lanjun|"
     r"hithium|chuneng|cornex|farasis|zenergy|ganfeng|narada|great power|lishen|bak|cbak|tianneng|chilwee|phylion|"
     r"jeve|geely|energee|yaoning|inpower|wanxiang|a123|trina|hina|zoolnasm|desay|cosmx|ampace|atl\b|dmegc|"
     r"highstar|weilan|welion|qingtao|tailan|pylontech|shuangdeng|far east|kexiang|haisida|dfd|do-fluoride|"
     r"chinese|china|\(.*[一-鿿]", "China"),
    (r"tesla|ford|general motors|\bgm\b|our next energy|\bone\b|freyr|t1 energy|kore|lyten|amprius|enovix|"
     r"form energy|eos|american battery|microvast|sila|quantumscape|statevolt|ipower|mitra chem|ascend", "North America"),
    (r"volkswagen|powerco|acc\b|automotive cells|northvolt|verkor|inobat|morrow|elinor|freyr|customcells|"
     r"varta|leclanch|blue solutions|bollor|saft|totalenergies|mercedes|bmw|stellantis|italvolt|basquevolt|"
     r"cellforce|porsche|tiamat|rosatom|renera|liotech", "Europe"),
    (r"tata|agratas|ola|reliance|amara raja|exide|jsw|lucas|waaree|log9|ibc|international battery", "India"),
]


def hq(text):
    t = (text or "").lower()
    for pat, h in RULES:
        if re.search(pat, t):
            return h
    return "Other/unknown"


con = duckdb.connect("factories.db", read_only=True)
rows = con.execute("""SELECT b.year, f.operator, f.parent_company, f.region, b.gwh_built_nameplate, b.gwh_best
                      FROM capacity_by_year b JOIN factories f ON f.id = b.id WHERE b.year BETWEEN 2020 AND 2025""").fetchall()
agg = defaultdict(lambda: [0.0, 0.0])
for y, op, pc, reg, d, c in rows:
    k = (y, hq(f"{op} {pc}"), reg)
    agg[k][0] += d or 0
    agg[k][1] += c or 0
with open("capacity_by_hq.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["year", "hq", "plant_region", "gwh_built_nameplate", "gwh_producing"])
    for (y, h, reg), (d, c) in sorted(agg.items()):
        w.writerow([y, h, reg, round(d, 1), round(c, 1)])
tot = defaultdict(float)
for (y, h, reg), (d, c) in agg.items():
    if y == 2025:
        tot[h] += d
print({k: round(v) for k, v in sorted(tot.items(), key=lambda x: -x[1])})
