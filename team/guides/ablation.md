# Ablation: keeping the harness lean

Every element of this harness – a role, a check, a contract, a brief's instruction – encodes an assumption about what the model can't do on its own. Those assumptions go stale as models improve, and instructions written for older models can now make output worse. This protocol finds out which elements are still earning their keep.

## When to run it

- After the first substantial project with the harness
- When the team moves to a new model generation
- When spend is high relative to what audits are catching

## Method

Remove one element at a time. Removing several at once makes it impossible to tell which ones were load-bearing.

1. **Pick a benchmark task set.** Three to five representative tasks from a finished or current project, with known good outcomes. Include at least one at the edge of what the workers handle well – that is where harness elements matter most.
2. **Run the baseline** with the full harness. Record: audit verdicts, human judgement of quality, spend, and wall-clock time.
3. **Remove one element** and re-run the same tasks. Candidates, roughly in order of cost:
   - per-task audit (keep only the final integration audit)
   - contracts
   - the researcher phase
   - long or detailed sections of an agent brief (try the shortest version that states the goal and the constraints)
   - checkpoint sweeps
   - the gardener
4. **Compare** against the baseline on quality first, then spend. Have a human judge quality blind to which run produced it where possible.
5. **Decide.** Keep the element if quality drops; drop or lighten it if quality holds. Record the result and reasoning in `team/DECISIONS.md`, and update the skill's defaults if the finding generalises.

## Brief length specifically

Current models follow brief instructions well and can be degraded by over-prescription. When testing a brief, write the minimal version – purpose, boundaries, output format, the few rules that prevent real failures – and compare it to the full one. Keep instructions that fix an observed failure; drop those that only restate good practice. Prefer explaining why over emphasis: capitals and "must" tend to cause over-application.

## What not to remove without evidence

The independent auditor on high-risk work, the executable definition of done, file boundaries, and the escalation rule for missing access. These guard against the failures that are most expensive when they slip through.

