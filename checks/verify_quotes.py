#!/usr/bin/env python3
"""Re-fetch evidence URLs and confirm each quote appears verbatim (whitespace/case-insensitive).

    python3 checks/verify_quotes.py --task T003 [--sample 15] [--seed 1]

Used by the auditor (network-dependent, so not part of run_all.py). Prints one line per
source: FOUND / MISSING / FETCH_FAIL. FETCH_FAIL is not a failure of the worker, but the
auditor must then check that quote by hand (WebFetch) or mark it UNKNOWN.
"""
import argparse
import html
import os
import random
import re
import urllib.request

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def norm(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    # drop all whitespace: PDF layout text and Chinese pages insert spaces between characters and numbers
    return re.sub(r"[\s　]+", "", s).lower()


def local_filing(url):
    import glob
    for f in glob.glob(os.path.join(ROOT, "team/evidence/filings/*.txt")):
        with open(f, encoding="utf-8", errors="ignore") as fh:
            if fh.readline().strip() == f"SOURCE: {url}":
                return fh.read()
    return None


def fetch(url):
    if url.lower().endswith(".pdf"):
        txt = local_filing(url)
        if txt is not None:
            return txt
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (dataset verification)"})
    with urllib.request.urlopen(req, timeout=25) as r:
        raw = r.read()
    for enc in ("utf-8", "gb18030", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "ignore")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--sample", type=int, default=15)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    ev = pd.read_csv(os.path.join(ROOT, "data/field_evidence.csv"))
    ev = ev[ev.task == a.task].drop_duplicates("source_id")
    rows = ev.sample(min(a.sample, len(ev)), random_state=a.seed) if len(ev) else ev
    cache, counts = {}, {"FOUND": 0, "MISSING": 0, "FETCH_FAIL": 0}
    for _, r in rows.iterrows():
        try:
            page = cache.setdefault(r.url, norm(fetch(r.url)))
            q = norm(str(r.quote))
            # tolerate ellipses in quotes: every fragment must be present
            ok = all(frag.strip() in page for frag in re.split(r"\s*(?:\.\.\.|…)\s*", q) if frag.strip())
            tag = "FOUND" if ok else "MISSING"
        except Exception as e:  # noqa: BLE001
            tag = f"FETCH_FAIL"
            q = f"{type(e).__name__}"
        counts[tag] += 1
        print(f"{tag} {r.source_id} {r.id} [{r.field}] {r.url}")
    print(f"SUMMARY task={a.task} sampled={len(rows)} " + " ".join(f"{k}={v}" for k, v in counts.items()))


if __name__ == "__main__":
    main()
