# Audit log

One entry per audit. Used to tune the harness: which checks catch real problems,
which failure types recur, whether the model tiers are right.

| Date | Task | Verdict | Failure type (spec gap / capability / diligence / none) | What was caught |
|---|---|---|---|---|


## T002 (CATL pilot) – audit 1 – 2026-11-20 – auditor opus/high
VERDICT fail · diligence (primary), 2 capability, 2 spec gaps. Quotes 26/26 on page; values 24/26 supported (Xiamen-80 ref year from a structure-completion date; Thuringia start_year pointed at wrong source). Blocking: Yichun status the worker itself doubted; operator site list built from news, not CATL's disclosure (Times-FAW Xiapu, Ampace Xiamen missing); Luoyang nulled although People's Daily 2023-09-25 gives phase 1 = 60 GWh. G4: 4 large rows < 0.6 not escalated.
Caught by: auditor value-vs-quote probe and independent search (checks C0–C6 could not catch any of these).
Harness changes: brief steps 6–8 (dig/escalate, open snippets, mine cited pages), self-check additions (quote contains number, ref-year from 达产 statement, phase arithmetic), D-012 narrowed, installed basis note, lead-side filings extraction (scripts/fetch_filings.py) because workers cannot read PDFs.
