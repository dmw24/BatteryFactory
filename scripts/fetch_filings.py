#!/usr/bin/env python3
"""Lead-side helper: fetch listed Chinese battery makers' annual reports from cninfo and
extract text so (shell-less) research workers can Grep them.

    python3 scripts/fetch_filings.py 300750 002594 ...   # stock codes
    python3 scripts/fetch_filings.py --all

Writes team/evidence/filings/<code>_<year>.txt (gitignored: large, rebuildable) and appends
to team/evidence/filings/MANIFEST.csv (committed: code, company, title, pdf url, fetched).
Quotes taken from these files must cite the PDF url in the manifest.
"""
import csv
import datetime
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "team/evidence/filings")
CODES = {  # stock code: company
    "300750": "CATL", "002594": "BYD", "002074": "Gotion High-tech", "300014": "EVE Energy",
    "300207": "Sunwoda", "300438": "Great Power", "688567": "Farasis", "002812": "Yunnan Energy (n/a)",
    "300073": "Dangsheng (materials, skip)", "002709": "Tinci (materials, skip)", "688819": "Tianneng",
    "300068": "Narada", "002245": "Envision?/Aoyang (check)", "002460": "Ganfeng Lithium",
    "300919": "Zhongwei (materials, skip)", "002733": "Xiongtao (check)", "688063": "Pylontech",
    "301327": "Hunan Huasheng (check)", "688005": "Ronbay (materials, skip)", "300035": "Zhongke Electric (check)",
}


def post(url, data):
    req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode(),
                                 headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/x-www-form-urlencoded"})
    return json.load(urllib.request.urlopen(req, timeout=40))


def fetch(code):
    org = post("https://www.cninfo.com.cn/new/information/topSearch/query", {"keyWord": code, "maxNum": 1})
    if not org:
        print(f"FAIL {code}: no org id"); return
    org_id, name = org[0]["orgId"], org[0]["zwjc"]
    column = "sse" if code.startswith("6") else "szse"
    res = post("https://www.cninfo.com.cn/new/hisAnnouncement/query",
               {"stock": f"{code},{org_id}", "tabName": "fulltext", "pageSize": 30, "pageNum": 1, "column": column,
                "category": "category_ndbg_szsh", "seDate": "2025-01-01~2026-11-20"})
    anns = [a for a in (res.get("announcements") or [])
            if "年度报告" in a["announcementTitle"] and "摘要" not in a["announcementTitle"]
            and "英文" not in a["announcementTitle"]]
    if not anns:
        print(f"FAIL {code} {name}: no annual report found"); return
    a = sorted(anns, key=lambda x: x["adjunctUrl"])[-1]
    url = "http://static.cninfo.com.cn/" + a["adjunctUrl"]
    year = "".join(ch for ch in a["announcementTitle"][:4] if ch.isdigit())
    pdf, txt = os.path.join(OUT, f"{code}.pdf"), os.path.join(OUT, f"{code}_{year}.txt")
    subprocess.run(["curl", "-s", "-m", "180", "-o", pdf, url], check=True)
    subprocess.run(["pdftotext", "-layout", pdf, txt], check=True)
    os.remove(pdf)
    with open(txt, "r+", encoding="utf-8", errors="ignore") as f:
        body = f.read(); f.seek(0)
        f.write(f"SOURCE: {url}\nTITLE: {name} {a['announcementTitle']}\nFETCHED: {datetime.date.today()}\n\n" + body)
    with open(os.path.join(OUT, "MANIFEST.csv"), "a", newline="") as f:
        csv.writer(f).writerow([code, name, a["announcementTitle"], url, datetime.date.today(), os.path.basename(txt)])
    print(f"OK {code} {name} {a['announcementTitle']} -> {txt} ({sum(1 for _ in open(txt))} lines)")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    codes = [c for c in CODES if "skip" not in CODES[c]] if "--all" in sys.argv else sys.argv[1:]
    for c in codes:
        try:
            fetch(c)
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {c}: {type(e).__name__} {e}")
