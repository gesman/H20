# H20 Contract

This file ships inside copied `./H20/` directories so the payload stays self-contained after users copy only that directory into a project. In the source H20 repository, the root `README.md` remains the authoritative edit target for this contract; keep this payload copy in sync when changing schemas, recovery semantics, or helper behavior.

## Directory layout

Inside a target project using H20:

```text
./H20/
├── 1-clarify-task.md
├── 2-generate-master-plan.md
├── 3-emit-steps.md
├── 4-execute-step.md
├── Extras/
│   ├── 1-clarify-task-assume-defaults.md
│   ├── 3a-env-checker
│   ├── 4-autoexec-claude
│   ├── 4-autoexec-codex
│   ├── 5-review.md
│   ├── README.md
│   └── helpers/
├── Reviews/
│   └── 01-<first-milestone>/
│       ├── REVIEW-01.md
│       └── raw-review-prompt-01.md
├── CONTRACT.md
├── 01-<first-milestone>/
│   ├── raw-prompt.txt
│   ├── TASK.md
│   ├── MASTER-PLAN.md
│   ├── ROADMAP.md
│   ├── BLOCKED.md
│   ├── STEP-01--<kebab>.md
│   ├── STEP-01--DONE.md
│   ├── STEP-02--<kebab>.md
│   └── STEP-02--DONE.md
└── 02-<second-milestone>/
    └── …
```

Milestones start at `01`, two-digit zero-padded, kebab-case title. Steps and their done-files live inline in the milestone directory. There is no `steps/`, `plans/`, or `summaries/` subdirectory.

## File-naming rules

- Meta-prompts: `1-clarify-task.md`, `2-generate-master-plan.md`, `3-emit-steps.md`, and `4-execute-step.md` at `./H20/`.
- Milestones: `NN-<kebab>/` where `NN` is `01`..`99`.
- Raw prompt: `raw-prompt.txt`.
- Task brief: `TASK.md`.
- Master plan: `MASTER-PLAN.md`.
- Roadmap: `ROADMAP.md`.
- Steps: `STEP-NN--<kebab>.md`.
- Done-files: `STEP-NN--DONE.md`.
- Blocked handoff: optional milestone-root `BLOCKED.md`.
- Review snapshots: optional `./H20/Reviews/NN-<kebab>/REVIEW-NN.md`, where the review directory name matches the reviewed milestone.
- Review follow-up prompts: optional `./H20/Reviews/NN-<kebab>/raw-review-prompt-NN.md`, paired with the review snapshot that produced it.

## Schemas

### TASK.md schema

- `# Task: <milestone title>`
- `## Goal` — one paragraph, imperative voice.
- `## Context` — tech stack, target runtime, relevant existing code, users. Research-phase decisions land here.
- `## Requirements` — numbered list. Each item is one testable requirement. Preserve execution-critical source literals such as exact commands, config blocks, env vars, ignore patterns, file/path lists, validation queries, rollback steps, and security exclusions, or state the accepted supersession explicitly.
- `## Non-goals` — explicit scope exclusions.
- `## Success criteria` — bulleted, verifiable.
- `## Research notes` — optional; include only when the clarify-task research phase ran.
- `## Open questions` — optional; include only when clarify-task could not close all gaps.

### MASTER-PLAN.md schema

- `# Master Plan: <milestone title>`
- `## Task source` — path to this milestone's `TASK.md`.
- `## Strategy` — the reviewed per-milestone implementation approach: architecture, data flow, major boundaries, sequencing rationale, exact source literals needed for execution, and key decisions.
- `## Step outline` — ordered list of expected execution steps at the outcome level.
- `## Requirement coverage` — table with columns: `Requirement | Covered by | Notes`.
- `## Success coverage` — table with columns: `Success criterion | Verification approach | Notes`.
- `## Risks and mitigations` — concrete implementation risks, assumptions, and how steps should reduce or verify them.
- `## Out of scope` — boundaries inherited from `TASK.md` plus any planning-specific exclusions.
- `## Planner notes` — optional; only for real gaps that do not invalidate the task but should be visible before step emission.

### ROADMAP.md schema

- `# Roadmap: <milestone title>`
- `## Steps` — table with columns: `# | File | Goal | Depends on`.
- `## Execution order` — linear list of step filenames in execution order.
- `## Emitter notes` — optional; only for real gaps that `TASK.md` or `MASTER-PLAN.md` did not address.

### STEP-NN--<kebab>.md schema

- `# Step NN: <title>`
- `## Prerequisite` — either `none` or exactly one immediately prior done-file path.
- `## Goal` — one paragraph describing the outcome.
- `## Actions` — numbered list; each action small, specific, and verifiable.
- `## Deliverables` — files created or modified, with relative paths.
- `## Verification` — concrete commands or checks the executor must run. Prefer agent-runnable checks: commands, automated flows, API calls, screenshots, DOM checks, logs, or equivalent objective checks. Do not use manual visual check or user walkthrough language for objective behavior unless no reasonable agent-side tool or fallback can judge it. Mark verification human-only only with that reason.
- `## Done signal` — literal instruction to write `STEP-NN--DONE.md` on full pass and commit if in a git repo.

### STEP-NN--DONE.md schema

- `# STEP-NN DONE: <title>`
- `## Summary` — 3–6 bullets covering what was built, key decisions, capability-use outcome (`used`, `best-effort fallback`, `blocked`, or `not needed`), tests added or not applicable, and human-verification outcome when applicable.
- `## Files changed` — bullet list of paths.
- `## Verification results` — one line per check using `✅`, `❌`, or `⚠ skipped`.
- `## Gotchas for next step` — full-sentence notes the next step needs.
- `## Commit` — if in a git repo, record `same commit as this done-file — subject: step-NN: <title>`; otherwise `not a git repo — no commit`. The executor's final handoff should print the actual SHA separately because a tracked file cannot contain its own final commit ID without changing that ID.

### BLOCKED.md schema

- `# BLOCKED: STEP-NN <title>`
- `## What happened` — one paragraph explaining the blocker.
- `## Evidence` — bullet list of concrete observations.
- `## Earliest safe recovery point` — one of `resume current step`, `re-emit steps from current step`, `redo master plan`, `redo task`, or `start new milestone`, plus one-sentence reasoning.
- `## Workspace state` — what changed, what is safe to keep, what is safe to discard, and any verification already run.
- `## Suggested user actions` — 2 or 3 labeled options, with exactly one recommended.

### Optional review artifacts

These artifacts are produced only by non-core helpers such as `./H20/Extras/5-review.md`. They live under `./H20/Reviews/` and do not change milestone completion semantics, done-file recovery, or executor behavior.

Done-files may define review scope, but they are not correctness evidence. Review findings and clearances must be backed by inspected artifacts, concrete recorded verification, or fresh read-only checks when available.

### REVIEW-NN.md schema

- `# Review NN: <reviewed milestone title>`
- `## Reviewed scope` — the reviewed milestone path, whether the run covered the whole milestone or a specific completed step, and any explicit exclusions.
- `## Review basis` — review run date, reviewer / agent label if known, done-files used to derive scope, and files actually inspected.
- `## Seeded concerns` — optional. Each entry records the original concern, its source, the outcome (`confirmed`, `disproved`, `not applicable`, or `inconclusive`), and one-sentence reasoning.
- `## Independent findings` — numbered list ordered by severity. Each finding includes: severity, issue, evidence, affected files or interfaces, and recommended disposition (`carry forward`, `defer`, `cross-cutting`, or `acceptable tradeoff pending user confirmation`).
- `## Deferred or acceptable tradeoffs` — optional.
- `## Cross-cutting or unrelated observations` — optional.
- `## Recommended follow-up milestones` — 1 to 3 concrete next-milestone options, with exactly one recommended.

### raw-review-prompt-NN.md schema

- `# Raw review prompt NN: <proposed follow-up title>`
- `## Source review` — path to the paired `REVIEW-NN.md` and one sentence describing the review scope.
- `## Goal` — one paragraph describing the follow-up milestone to create.
- `## Findings included` — numbered list of review findings intentionally carried into the follow-up scope.
- `## Findings explicitly excluded` — numbered or bulleted list of findings intentionally left out, deferred, or treated as unrelated.
- `## Constraints` — explicit scope fences, assumptions, and boundaries for the next milestone.
- `## Success criteria` — bulleted, verifiable outcomes expected from the follow-up milestone.

## Recovery rule

Before executing `STEP-NN--<kebab>.md`, check whether the sibling `STEP-NN--DONE.md` exists in the same milestone directory. If it exists, stop and report `STEP-NN already executed`. If it does not, execute. To rerun a step, delete its done-file manually. That is the entire recovery mechanism.

`BLOCKED.md` never marks a step complete and does not alter the done-file recovery rule.

## Interrupted runs

H20 auto-recovers completed steps through done-files. It does not silently recover partial runs. If a coding agent crashed before writing `STEP-NN--DONE.md`, the next executor run must first check for workspace drift: already-created deliverables from the step, or unrelated dirty files in the worktree. If either is present, stop and ask the user whether to inspect, clean up, or intentionally continue.

## Blocked runs

If execution hits a durable blocker that makes the current step unsafe to complete, the executor should write milestone-root `BLOCKED.md` and stop without writing a done-file or making a commit. Durable blockers include invalidated step assumptions with no safe in-scope repair, missing external access or credentials, failed or unavailable capabilities or facilities with no safe fallback, or external constraints that change the implementation path.

Do not use `BLOCKED.md` for ordinary clarifying chat, dirty-worktree checks, suspected partial-run detection, or planned human-only verification pauses already covered elsewhere in the executor flow.

`BLOCKED.md` is consumed only when the user explicitly passes it into `3-emit-steps.md`, `2-generate-master-plan.md`, or `1-clarify-task.md`. Its presence on disk alone does not auto-replan anything.

After the user chooses a recovery path and materializes it, delete `BLOCKED.md`. If the milestone is abandoned entirely, keeping `BLOCKED.md` as a tombstone is fine.

## Optional executor overlays

Optional convenience wrappers may append literal control lines after the step path in executor input:

- `AUTOEXEC_MODE=1` — executor capability assessment must use any already-available capabilities without pausing; if a required capability is missing or failing and no safe fallback exists, the executor should write `BLOCKED.md` and stop.
- `AUTOEXEC_SKIP_HUMAN=1` — human-only verification may be recorded as `⚠ skipped` after the executor performs all automatable setup. Without this marker, human-only verification still pauses for user input even in autoexec mode.

These overlays do not change the done-file recovery rule, partial-run detection, blocker semantics, or milestone schemas.
