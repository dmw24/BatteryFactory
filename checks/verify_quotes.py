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


def norm(s, is_html=True):
    if is_html:  # PDF text can contain '<' in tables; only strip tags from HTML
        s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    # drop all whitespace: PDF layout text and Chinese pages insert spaces between characters and numbers
    s = s.translate(str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-", "\u00a0": " "}))
    return re.sub(r"[\s　]+", "", s).lower()


def local_filing(url):
    import glob
    for f in glob.glob(os.path.join(ROOT, "team/evidence/filings/*.txt")):
        with open(f, encoding="utf-8", errors="ignore") as fh:
            if fh.readline().strip() == f"SOURCE: {url}":
                return fh.read()
    return None


class ScannedPDF(Exception):
    """PDF without a text layer: cannot be string-matched; needs a visual check (tag SCANNED_PDF)."""


def fetch(url):
    if url.lower().endswith(".pdf"):
        txt = local_filing(url)
        if txt is not None:
            return txt
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (dataset verification)"})
    with urllib.request.urlopen(req, timeout=25) as r:
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip" or raw[:2] == b"\x1f\x8b":
            import gzip
            raw = gzip.decompress(raw)
    if raw[:5] == b"%PDF-":  # remote PDF: extract its text layer; a scanned PDF has (almost) none
        import subprocess
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tf:
            tf.write(raw); tf.flush()
            txt = subprocess.run(["pdftotext", "-layout", tf.name, "-"], capture_output=True).stdout.decode("utf-8", "ignore")
        if len(re.sub(r"\s+", "", txt)) < 200:
            raise ScannedPDF("no text layer")
        return "\x00PDF\x00" + txt
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
    cache, counts = {}, {"FOUND": 0, "MISSING": 0, "FETCH_FAIL": 0, "SCANNED_PDF": 0, "REPORTED_TIER": 0}
    for _, r in rows.iterrows():
        if str(r.get("tier", "")).strip() == "reported":
            counts["REPORTED_TIER"] += 1
            print(f"REPORTED_TIER {r.source_id} {r.id} [{r.field}] {r.url} (snippet evidence; not string-matched)")
            continue
        try:
            if r.url not in cache:
                raw = fetch(r.url)
                is_pdf_text = raw.startswith("\x00PDF\x00") or (r.url.lower().endswith(".pdf") and local_filing(r.url) is not None)
                cache[r.url] = norm(raw.replace("\x00PDF\x00", ""), is_html=not is_pdf_text)
            page = cache[r.url]
            q = norm(str(r.quote))
            # tolerate ellipses in quotes: every fragment must be present
            ok = all(frag.strip().rstrip(".。,，;；") in page for frag in re.split(r"\s*(?:\.\.\.|…)\s*", q) if frag.strip().rstrip(".。,，;；"))  # sentence-final punctuation the page may continue past
            tag = "FOUND" if ok else "MISSING"
        except ScannedPDF:
            tag = "SCANNED_PDF"
        except Exception as e:  # noqa: BLE001
            tag = f"FETCH_FAIL"
            q = f"{type(e).__name__}"
        counts[tag] += 1
        print(f"{tag} {r.source_id} {r.id} [{r.field}] {r.url}")
    print(f"SUMMARY task={a.task} sampled={len(rows)} " + " ".join(f"{k}={v}" for k, v in counts.items()))


if __name__ == "__main__":
    main()
