# Decisions waiting for the owner (digest, 2026-11-24)

Each line is a choice the team made and logged in `team/DECISIONS.md` as "pending owner". The data is built on the
recommended option; ticking it confirms. Changing one means a rebuild, not a re-research, unless marked *re-research*.

## Definitions that move the totals
- [ ] **D-014 Nameplate = full site plan** (built + under construction + every stated phase with a GWh figure). Alternative: built + under construction only. *Recommended: keep* — the built-nameplate series already separates built from planned.
- [ ] **D-015 Undated aspirations go to notes, not nameplate** ("can later be doubled"). *Recommended: keep.*
- [ ] **D-017 A later company description supersedes an earlier site total.** *Recommended: keep.*
- [ ] **D-021 Reference year = latest dated phase** when only some phases are dated. *Recommended: keep.*
- [ ] **D-022 "Up to X GWh" counts as design capacity** of a named plant. *Recommended: keep.*
- [ ] **D-026 Bundled figures (cells + packs/systems) → plant kept, capacity null.** *Recommended: keep* (conservative).
- [ ] **D-019 Long-duration non-lithium chemistries excluded from totals** (Form, ESS Inc, Eos, …). *Recommended: keep.*
- [ ] **D-023/D-024/D-027/D-028/D-030 The five series** (A confirmed, B upper fill, C best estimate, D/D-high built nameplate,
      E with unallocated company capacity; Ah-converted estimates reported separately). *Recommended: quote C as
      "producing" and E as the IEA-comparable figure, always with D-high as the range.*

## Evidence rules
- [ ] **D-013 User-posted aggregator pages (e.g. Xueqiu) allowed only at confidence ≤0.5.** *Recommended: keep.*
- [ ] **D-016 Status from a company's environmental-disclosure list → operational at confidence ≤0.4.** *Recommended: keep.*
- [ ] **D-020 "Under construction" needs physical site works**, not a ceremony. *Recommended: keep.*
- [ ] **D-018 Idle plants → paused, installed null.** *Recommended: keep.*
- [ ] **D-029 Benchmarks may come from paywalled publishers' own free pages** (overlay only). *Recommended: keep.*

## Process (informational)
- [ ] D-001 Standard tier, D-003 project_state field, D-005 staged budget, D-006 done-gate thresholds, D-007 patch build,
      D-008 installed vs nameplate, D-009–D-012 workflow choices. *Recommended: accept as recorded.*

## Open owner actions (not decisions above)
- [ ] **Done gates G2a (≥3.2 TWh installed) and G4 (no ≥10 GWh plant below 0.6 confidence)** still fail by design;
      accept as documented limits or fund more work (see FINAL_REPORT.md).
- [ ] **Licence** for publishing the dataset — see `docs/LICENSE_PROPOSAL.md`.
- [ ] **Network allowlist** for nrel.gov, iea.org, meti.go.jp, dart.fss.or.kr, jintan.gov.cn (`team/ESCALATIONS.md`, T088).
