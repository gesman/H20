# H20 Contract

This file ships inside copied `./H20/` directories so the payload stays self-contained after users copy only that directory into a project. In the source H20 repository, the root `README.md` remains the authoritative edit target for this contract; keep this payload copy in sync when changing schemas, recovery semantics, or helper behavior.

## Directory layout

Inside a target project using H20:

```text
./H20/
├── 1-create-prompt.md
├── 2-planner.md
├── 3-executor.md
├── Extras/
│   ├── 2a-env-checker
│   ├── 3-autoexec-claude
│   ├── 3-autoexec-codex
│   ├── README.md
│   └── helpers/
├── CONTRACT.md
├── 01-<first-milestone>/
│   ├── raw-prompt.txt
│   ├── good-prompt.md
│   ├── ROADMAP.md
│   ├── BLOCKED.md
│   ├── PLAN-01--<kebab>.md
│   ├── PLAN-01--DONE.md
│   ├── PLAN-02--<kebab>.md
│   └── PLAN-02--DONE.md
└── 02-<second-milestone>/
    └── …
```

Milestones start at `01`, two-digit zero-padded, kebab-case title. Plans and their done-files live inline in the milestone directory. There is no `plans/` or `summaries/` subdirectory.

## File-naming rules

- Meta-prompts: `1-create-prompt.md`, `2-planner.md`, `3-executor.md` at `./H20/`.
- Milestones: `NN-<kebab>/` where `NN` is `01`..`99`.
- Plans: `PLAN-NN--<kebab>.md`.
- Done-files: `PLAN-NN--DONE.md`.
- Raw prompt: `raw-prompt.txt`.
- Good prompt: `good-prompt.md`.
- Roadmap: `ROADMAP.md`.
- Blocked handoff: optional milestone-root `BLOCKED.md`.

## Schemas

### good-prompt.md schema

- `# Goal` — one paragraph, imperative voice.
- `## Context` — tech stack, target runtime, relevant existing code, users. Research-phase decisions land here.
- `## Requirements` — numbered list. Each item is one testable requirement.
- `## Non-goals` — explicit scope exclusions.
- `## Success criteria` — bulleted, verifiable.
- `## Research notes` — optional; include only when the create-prompt research phase ran.
- `## Open questions` — optional; include only when create-prompt could not close all gaps.

### ROADMAP.md schema

- `# Roadmap: <milestone title>`
- `## Plans` — table with columns: `# | File | Goal | Depends on`.
- `## Execution order` — linear list of plan filenames in execution order.
- `## Planner notes` — optional; only for real gaps that the good prompt did not resolve.

### PLAN-NN--<kebab>.md schema

- `# Plan NN: <title>`
- `## Prerequisite` — either `none` or exactly one immediately prior done-file path.
- `## Goal` — one paragraph describing the outcome.
- `## Steps` — numbered list; each step small, specific, verifiable.
- `## Deliverables` — files created or modified, with relative paths.
- `## Verification` — concrete commands or checks the executor must run.
- `## Done signal` — literal instruction to write `PLAN-NN--DONE.md` on full pass and commit if in a git repo.

### PLAN-NN--DONE.md schema

- `# PLAN-NN DONE: <title>`
- `## Summary` — 3–6 bullets covering what was built, key decisions, capability-use outcome (`used`, `best-effort fallback`, `blocked`, or `not needed`), tests added or not applicable, and human-verification outcome when applicable.
- `## Files changed` — bullet list of paths.
- `## Verification results` — one line per check using `✅`, `❌`, or `⚠ skipped`.
- `## Gotchas for next plan` — full-sentence notes the next plan needs.
- `## Commit` — if in a git repo, record `same commit as this done-file — subject: plan-NN: <title>`; otherwise `not a git repo — no commit`. The executor's final handoff should print the actual SHA separately because a tracked file cannot contain its own final commit ID without changing that ID.

### BLOCKED.md schema

- `# BLOCKED: PLAN-NN <title>`
- `## What happened` — one paragraph explaining the blocker.
- `## Evidence` — bullet list of concrete observations.
- `## Earliest safe recovery point` — one of `resume current plan`, `replan from current plan`, `redo good-prompt`, or `start new milestone`, plus one-sentence reasoning.
- `## Workspace state` — what changed, what is safe to keep, what is safe to discard, and any verification already run.
- `## Suggested user actions` — 2 or 3 labeled options, with exactly one recommended.

## Recovery rule

Before executing `PLAN-NN--<kebab>.md`, check whether the sibling `PLAN-NN--DONE.md` exists in the same milestone directory. If it exists, stop and report `PLAN-NN already executed`. If it does not, execute. To rerun a plan, delete its done-file manually. That is the entire recovery mechanism.

`BLOCKED.md` never marks a plan complete and does not alter the done-file recovery rule.

## Interrupted runs

H20 auto-recovers completed plans through done-files. It does not silently recover partial runs. If a coding agent crashed before writing `PLAN-NN--DONE.md`, the next executor run must first check for workspace drift: already-created deliverables from the plan, or unrelated dirty files in the worktree. If either is present, stop and ask the user whether to inspect, clean up, or intentionally continue.

## Blocked runs

If execution hits a durable blocker that makes the current plan unsafe to complete, the executor should write milestone-root `BLOCKED.md` and stop without writing a done-file or making a commit. Durable blockers include invalidated plan assumptions with no safe in-scope repair, missing external access or credentials, failed or unavailable capabilities or facilities with no safe fallback, or external constraints that change the implementation path.

Do not use `BLOCKED.md` for ordinary clarifying chat, dirty-worktree checks, suspected partial-run detection, or planned human-only verification pauses already covered elsewhere in the executor flow.

After the user chooses a recovery path and materializes it, delete `BLOCKED.md`. If the milestone is abandoned entirely, keeping `BLOCKED.md` as a tombstone is fine.

## Optional executor overlays

Optional convenience wrappers may append literal control lines after the plan path in executor input:

- `AUTOEXEC_MODE=1` — executor step 3 must use any already-available capabilities without pausing; if a required capability is missing or failing and no safe fallback exists, the executor should write `BLOCKED.md` and stop.
- `AUTOEXEC_SKIP_HUMAN=1` — human-only verification may be recorded as `⚠ skipped` after the executor performs all automatable setup. Without this marker, human-only verification still pauses for user input even in autoexec mode.

These overlays do not change the done-file recovery rule, partial-run detection, blocker semantics, or milestone schemas.
