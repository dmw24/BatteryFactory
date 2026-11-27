WebSearch has a budget of 200 calls per lead turn, SHARED by every sub-agent launched in that turn — 15 parallel researchers starve after ~8–40 searches each.
Launch at most 2–3 search-heavy researchers per lead turn; give everything else filing-only tasks (local text in
team/evidence/filings/, fetched by the lead with scripts/fetch_filings.py), which need no WebSearch. WebFetch cannot read
cninfo/SZSE PDFs (no text layer for the tool, >10 MB), so the lead must pre-fetch filings with pdftotext.
