# Decomposition and integration

How to cut an objective into tasks a team can work on in parallel, and how to put the pieces back together. This is the step that most determines whether the team converges.

## Contents
1. What a good task looks like
2. Choosing the cut
3. Contracts first
4. Sequencing
5. Cross-cutting work
6. Integration
7. Anti-patterns

## 1. What a good task looks like

- **One deliverable** a reviewer can judge on its own: a module, a dataset slice, a section, an evidence file.
- **One session.** A worker should finish it, including verification, before its context fills. If you can't describe the deliverable in two sentences, split it.
- **An explicit boundary** (`files` in `tasks.json`) that no other active task touches.
- **Acceptance criteria written first**, specific to the task, on top of the global `check_command`.
- **A risk rating.** Mark `risk: high` for tasks whose errors would propagate (shared contracts, core methods, headline results). High-risk tasks are always audited.

## 2. Choosing the cut

Pick the axis along which the work is most independent. Common cuts:

| Cut | Use when | Example |
|---|---|---|
| **By component** | Parts interact only through defined interfaces | API, storage layer, CLI |
| **By pipeline stage** | Work flows through ingest → transform → validate → publish | Each stage owned by one workstream, stages joined by file formats |
| **By slice of the domain** | The same method applies to many independent units | Countries, regions, products, modules, chapters |
| **By method** | Different units need different expertise | Industry, transport and buildings modelled differently |
| **By question** | Research with separable questions | One evidence file per question |

Often you combine two: workstreams by method, tasks by slice within each. Prefer cuts where the boundary is a file or a folder; boundaries inside a file cause collisions.

Size: 2–4 workstreams; enough ready tasks that no worker idles (about 5 per worker is a good default); tasks small enough that a failed audit wastes little.

## 3. Contracts first

Parallel work needs fixed interfaces. Before fanning out, create one or two **contract tasks**, owned by the lead or one worker and always rated high risk:

- software: interfaces, types, API schemas, test fixtures
- data: schemas, units, keys and classifications, file layout, the format of intermediate outputs
- research: the question list, evidence file format, source ID scheme, inclusion criteria
- documents: outline, section briefs, terminology list, style rules

Every other task depends on these. Changing a contract later is a lead decision logged in DECISIONS.md, followed by re-planning of affected tasks.

The contract tasks also fill `team/CONVENTIONS.md`: the shared choices – naming, units, precision, edge cases, style – that parallel workers would otherwise each make differently. Parallel writers conflict mostly through these implicit choices, not through the explicit spec. Settle them before fan-out, and add new ones as workers report them.

**Task contracts** are different from contract tasks: for each task that needs one (by tier: none, high-risk only, or all), the worker writes `team/contracts/<id>.md` saying what it will deliver and how each criterion will be proven, the auditor reviews it, and the lead approves before building starts.

## 4. Sequencing

- A task is ready only when everything in `depends_on` is merged (`status.py --ready`). Workers never build on unmerged branches; it creates invisible coupling.
- Order: contracts → a thin end-to-end slice (one unit through every stage) → breadth. The thin slice surfaces integration problems while they're cheap.
- Put the riskiest, least certain tasks early, not last.
- Keep the critical path short: if many tasks wait on one, split that one.

## Discoveries

Workers don't share what they learn unless asked. The handoff has a **Discoveries** field for anything that affects other tasks or CONVENTIONS.md – a quirk in a source, an edge case, a better approach. The lead passes discoveries to affected tasks and updates conventions. Lessons that will matter in future sessions go in `team/lessons/`.

## Monolithic work

When the remaining work is one big indivisible task, every worker tends to hit the same problem and overwrite each other's fixes. Split it with an oracle: run most of the job through a trusted reference (an established tool, a published dataset, a previous verified version) and only a different subset through the team's output per worker. When the result breaks, the problem lies in that worker's subset. Keep narrowing until each worker owns a distinct failure.

## 5. Cross-cutting work

Some work touches everything: renaming, shared utilities, global configuration, cross-section consistency, final reconciliation. Don't spread it across workers.

- Small cross-cutting fixes: the lead does them during integration.
- Larger ones: a dedicated task that runs alone, with no other active tasks touching its files.
- Drift (duplicated logic, convention breaches, stale docs): the gardener in Full tier, running between rounds when no worker is active.
- Global checks (totals across slices, consistency across sections): an integration task near the end, plus checks in `check_command` that run on the merged base branch.

## 6. Integration

- Workers work in their own worktree on `task/<id>`, rebase on the base branch before handing off, and re-run checks after rebasing.
- The lead integrates one approved task at a time and re-runs `check_command` on the merged result. If it breaks, revert and reopen the task with the failure attached.
- Conflicts on merge mean a boundary was wrong: resolve, then fix the boundaries in `tasks.json` so it doesn't recur.
- With `integration: pr`, approved work merges via its PR. With `integration: merge`, the lead merges the branch locally and pushes.
- After every few merges, the lead re-reads the spec and checks the whole still answers it – parts can each pass while the whole drifts.

## 7. Anti-patterns

- **"Do the analysis"** – a task with no clear deliverable. Split by output.
- **Tasks defined by effort, not result** – "spend time on X". Define what exists when done.
- **Shared scratch files** that several tasks write to. Give each task its own output and merge in an integration task.
- **Contracts changed mid-stream by a worker.** Only the lead changes contracts.
- **A backlog planned in full at the start** for long jobs. Plan the next two rounds in detail and the rest as headings; re-plan as audits teach you things.

