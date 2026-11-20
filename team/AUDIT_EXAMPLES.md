# Audit calibration examples

Few-shot examples that show the auditor how strict to be. The auditor reads these before every audit. Each example is a real (or realistic) piece of work with the verdict the human agreed was right and why.

Add an example whenever an audit diverges from human judgement – especially when the auditor found a real problem and then talked itself into passing the work anyway, or tested only the surface. Keep 3–8 examples; replace weaker ones rather than growing the file without limit.

---

## Example 1 – (title)

**Task:** (one line)
**What the work looked like:** (key facts, short)
**Correct verdict:** fail
**Criteria:** C1 pass · C2 pass · R1 FAIL (threshold: …; observed: …)
**Why:** (what a lenient auditor would have missed or excused, and why it matters)
**Lesson for the auditor:** (one sentence)


---

## Seed: profile example (replace with real examples from this project)

Illustrates the strictness expected: blocking findings with evidence, criteria with thresholds, UNKNOWN where it can't be settled.

```
VERDICT: fail
TASK: T005
FAILURE TYPE: diligence
CRITERIA: C1 PASS · C2 PASS · C3 FAIL (3 country-years > 0.5%) · C4 PASS · C5 PASS · R1 FAIL (series break unflagged)
CHECKS RE-RUN: checks/* → C3 fails for 3 country-years
FINDINGS:
  1. [blocking] Linear interpolation across a source switch in 2011 for 4 countries creates a false trend – data/build/europe/wind.csv rows 212–219 – break the series at the switch and flag
  2. [blocking] 2024 values carried forward from 2023 without an imputation flag – pipeline/gapfill.py:88
  3. [minor] Method note doesn't state the imputed share per country
SAMPLED FROM SOURCE: 15 checked, 13 confirmed, 2 mismatches (both carried-forward values above)
ASSUMPTIONS REVIEWED: A-012 (hydro includes pumped storage) – consequential for totals; should have been escalated
NOT CHECKED: source C values (raw data not in repo by licence)
```
