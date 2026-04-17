# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

H20 is a **lean coding-agent harness**, not an application. It ships four files under `./H20/` (`README.md`, `1-create-prompt.md`, `2-planner.md`, `3-executor.md`) that users copy into their own projects. There is no build, no tests, no runtime, no dependencies, no CLI — the meta-prompts *are* the product. Any "command" to run is a paste-into-agent instruction, not a shell command.

End-users copy `./H20/` into a target project and then invoke the three stages in order via file-reference syntax in a coding agent (e.g. `@H20/1-create-prompt.md @raw-prompt.txt`). Fresh context between stages is part of the design.

## The three-stage pipeline

1. **`1-create-prompt.md`** — turns raw input corpus into `./H20/NN-<kebab>/good-prompt.md`. Five phases: research-need judgment → research offer (opt-in) → pros/cons research → grilling (3–7 Qs, up to 3 rounds) → writing. Also emits `raw-prompt.txt` with the full source corpus + Q&A transcript.
2. **`2-planner.md`** — reads `good-prompt.md`, emits `ROADMAP.md` and `PLAN-NN--<kebab>.md` files. Targets 2–5 plans, strict single-prerequisite chain, coverage audit against every requirement and success criterion.
3. **`3-executor.md`** — executes one plan at a time. Seven steps, recovery check is Step 1. On full verification pass, writes `PLAN-NN--DONE.md` and commits (if git repo). Adds best-effort smoke tests automatically.

## Load-bearing conventions (do not break these when editing the meta-prompts)

- **Done-file recovery is the entire state machine.** A plan is done iff `PLAN-NN--DONE.md` exists. No manifests, no separate state. The literal filename `PLAN-NN--DONE.md` (no title suffix) must stay trivial to existence-check.
- **Single-prerequisite rule.** Each plan references *at most* the immediately prior done-file. If two upstream done-files are needed, planner merges plans or enriches the prior done-file's `## Gotchas for next plan` — never lists two prerequisites.
- **Self-contained inside `./H20/`.** Every artifact H20 touches (raw prompts, good prompts, roadmaps, plans, done-files) lives under `./H20/` of the target project. Nothing spills to project root.
- **Milestone naming:** `NN-<kebab>/` where NN is `01`..`99`, zero-padded. Plans: `PLAN-NN--<kebab>.md`, same zero-padding. Files `raw-prompt.txt`, `good-prompt.md`, `ROADMAP.md` are exact literal names.
- **Plans live inline in the milestone directory.** No `plans/` or `summaries/` subdirectory.

## Schema fidelity

`./H20/README.md` § Schemas is the contract. Each meta-prompt ends with `Contract: ./H20/README.md § Schemas`. When editing any of the four files, keep the three meta-prompts and README's schema section mutually consistent — the schemas in README are authoritative; the meta-prompts must produce conformant output.

## Editing the meta-prompts

- The target audience is a coding agent *with filesystem access* — Claude Code, Codex, and similar. Do not add agent-specific syntax (no Claude-only features, no slash commands, no tool-name assumptions). The "capability assessment" step in `3-executor.md` is where runtime differences get negotiated with the user.
- Each meta-prompt is pasted into a fresh agent context by the end-user — it must stand alone and not reference the others by assumed-loaded content. Cross-references are by file path only.
- Phase/step ordering is load-bearing. `3-executor.md` Step 1 (recovery check) must remain the first action; moving it breaks the recovery guarantee.
- Anti-drift and anti-footgun sections exist to prevent specific classes of LLM misbehavior (silent scope creep, silent interpretation choices, false done-files). Treat them as regression fences — add to them, do not weaken them.

## Example milestone

`./H20/` currently contains the three canonical meta-prompts, while the repo root `README.md` remains the contract document. The README references `./H20/example/01-wordcount-cli/` as a reference walkthrough illustrating the research-skip branch and executor's best-effort-tests behavior. If that example is absent in this checkout, do not fabricate it — either generate it deliberately as its own milestone or update the README to reflect reality.

## File layout note

This repo's git root keeps its existing on-disk directory name, but the branded payload that users copy is now `./H20/`. When the README says "copy `./H20/` into your project", it means that payload directory.
