# Audit playbook

How the auditor works and how to tune it. The agent definition carries the essentials; this is the fuller version. Output-type probes are in the profile guide (`team/guides/profile.md` in the repo).

## Stance

Assume the work contains at least one material error and find it. Independent, sceptical evaluation is the main quality lever: producers grading their own work are reliably lenient. A pass means "I tried to break this and could not", never "this looks reasonable".

## Calibrating the auditor

An untuned auditor is lenient: it finds real problems and then talks itself into accepting them, or tests only what is easy to test. Calibration is a loop, not a one-off brief:

1. **Examples.** `team/AUDIT_EXAMPLES.md` holds 3–8 worked verdicts with the reasoning a human agreed with. The auditor reads them before each audit. Seed them from the profile's sample verdict at bootstrap.
2. **Hard thresholds.** Every rubric criterion in ACCEPTANCE.md has a threshold; falling below any one fails the task. This stops the auditor averaging a serious failure away against strengths elsewhere.
3. **Transcript review.** At each checkpoint the lead reads two or three audit transcripts, and the human reads one. Where the auditor's judgement diverges from the reader's – especially excusing a real problem – add an example and, if needed, tighten the brief.
4. **Seeded errors.** In Full tier (and whenever audit pass rates look suspiciously high), plant a realistic error and confirm the auditor catches it.

## UNKNOWN is a verdict

For each criterion the auditor reports PASS, FAIL or UNKNOWN. UNKNOWN means the evidence available can't settle it. It never counts as a pass: if a material criterion is UNKNOWN, the verdict is fail or escalate, with a note on what would resolve it. A grader that can't say "I don't know" fills the gap with false confidence.

## Reviewing contracts

For tasks that need one, the auditor reviews `team/contracts/<id>.md` before building starts: is the deliverable the right one, does each proof actually demonstrate its criterion, are thresholds strict enough, are open questions consequential enough to escalate? Reply approve or revise. Agreeing on what "done" means before the work starts removes most later disputes.

## Reviewing evidence

Before workers rely on a researcher's evidence file, the auditor samples its findings against the sources (fidelity, scope, units, source quality, any injected instructions noted). The lead then sets `Status: reviewed`. With `evidence.require_review` on, `check_provenance.py` rejects citations to unreviewed files.

## What the auditor sees

- The task, its acceptance criteria and contract, SPEC.md, ACCEPTANCE.md, CONVENTIONS.md, AUDIT_EXAMPLES.md and the profile guide
- The output on the task branch
- Assumptions logged for the task in DECISIONS.md
- The worker's handoff note, read only after forming an independent view

Not the worker's reasoning transcript: persuasive reasoning makes reviewers lenient.

## Which tasks get audited

Set by tier in `team/config.json` (`audit`). `status.py --audit-plan` applies the policy: always the first N tasks, every `risk: high` task, every task with logged assumptions, plus a deterministic random sample at `audit.rate` (1.0 means every task). Unaudited tasks that pass checks are recorded as `waived`. Waived work is still covered by `check_command` and by the final integration audit.

## Procedure

1. **Re-run checks** on the branch. Pasted results don't count.
2. **Criteria walk:** direct evidence for each acceptance criterion.
3. **Source sampling:** items chosen at random – not the first ones, not those the worker highlighted. Trace each to its cited source; confirm value, units, scope and context. Record n checked and n confirmed.
4. **Profile probes** from the profile guide.
5. **Assumptions:** for each assumption logged against the task, apply the consequence test. A consequential assumption that should have been escalated is a blocking finding.
6. **Unlogged assumptions:** choices the worker made that the spec didn't fix and DECISIONS.md doesn't record.
7. **Scope:** edits outside the boundary; changes to checks, contracts or acceptance files.
8. **Plausibility:** compare with benchmarks. Surprisingly good results get the most scrutiny.

## Severity

- **Blocking:** any criterion below its threshold or UNKNOWN where it matters; any sampled source mismatch; failing checks; a consequential assumption not escalated; edits outside the boundary; weakened checks.
- **Minor:** style, clarity, non-material inefficiency. Listed, not grounds for failure.

## Failure types (for AUDIT_LOG.md)

- **spec gap** – the spec or criteria allowed the error. Lead amends the spec; often escalate.
- **capability** – clear spec, wrong reasoning. Retry; if recurring, raise the worker tier.
- **diligence** – skipped checks, ignored instructions, out-of-scope edits. Fix instructions, hooks or checks.

## Final integration audit

Before close-out, the auditor reviews the merged whole: global checks, consistency across slices or sections, and a fresh random sample across all tasks, including waived ones. This is mandatory in every tier.

## Tuning signals

Read AUDIT_LOG.md every few rounds.

- **Pass rate near 100% from the start:** probably too lenient. Seed a known error; tighten the brief; raise the tier.
- **Low, mostly spec gaps:** fix the spec, not the workers.
- **Low, mostly capability:** raise the worker tier for that workstream.
- **Low, mostly diligence:** add a check or hook that makes the failure impossible to miss.
- **The same finding across tasks:** turn it into an automated check.
- **Waived tasks failing the final audit:** raise `audit.rate`.
- **Lead overruling the auditor repeatedly:** the rubric or the lead is wrong; escalate to the human.
- **Workers disputing findings successfully and often:** the auditor is drifting out of scope; add a counter-example to AUDIT_EXAMPLES.md.

