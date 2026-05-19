# CLAUDE.md

This file provides local guidance to Claude Code when working in this repository.

## What This Repo Is

H20 is a lean coding-agent harness, not an application. The core payload is four agent-only meta-prompts under `./H20/`:

- `1-clarify-task.md`
- `2-generate-master-plan.md`
- `3-emit-steps.md`
- `4-execute-step.md`

The repo-root `README.md` is the authoritative user-facing contract document. `H20/CONTRACT.md` is the copied payload contract that keeps target projects self-contained. There is no build system, runtime, package manager, or application test suite in the core repo. The prompts and docs are the product.

End users copy `./H20/` into a target project and invoke each stage through file-reference syntax in a coding agent, for example:

```text
@H20/1-clarify-task.md @raw-prompt.txt
```

Fresh context between stages is part of the design.

## Four-Stage Pipeline

1. **`1-clarify-task.md`** turns raw source material into `raw-prompt.txt` and `TASK.md`. It judges whether research is needed, optionally presents research choices, grills the user with source evidence first, challenges fuzzy terminology, probes ambiguous workflows with concrete scenarios, then writes the milestone task brief.
2. **`2-generate-master-plan.md`** turns `TASK.md` into `MASTER-PLAN.md`. It reads task-relevant repo context/docs, uses `raw-prompt.txt` only for source-fidelity details already in scope, checks terminology and documented decisions against repo evidence, surfaces material strategy choices, then writes the per-milestone strategy.
3. **`3-emit-steps.md`** compiles `TASK.md` and `MASTER-PLAN.md` into `ROADMAP.md` and `STEP-NN--<kebab>.md` files. It enforces a linear, single-prerequisite step chain and covers every requirement, success criterion, master-plan outline item, and execution-critical literal.
4. **`4-execute-step.md`** executes exactly one step. It checks `_LOCKED.md` and the matching done-file first, loads only the required context, executes actions, adds lightweight tests for code-producing steps, verifies, writes `STEP-NN--DONE.md` only on full pass, and commits locally if in a git repo.

## Load-Bearing Conventions

- **Done-file recovery is the state machine.** A step is done iff `STEP-NN--DONE.md` exists. No manifest or hidden state may replace that.
- **Locked milestones win.** If a milestone contains `_LOCKED.md`, every H20 stage and helper must stop before reading or modifying any other artifact in that milestone.
- **Single-prerequisite rule.** Each step references at most the immediately prior done-file. If more context is needed, enrich the prior done-file's `## Gotchas for next step`.
- **Self-contained inside `./H20/`.** Every H20 artifact lives under `./H20/` in the target project. Nothing spills to the project root.
- **Milestone naming:** `NN-<kebab>/`, where `NN` is `01`..`99`.
- **Literal artifact names:** `raw-prompt.txt`, `TASK.md`, `MASTER-PLAN.md`, `ROADMAP.md`, `STEP-NN--<kebab>.md`, `STEP-NN--DONE.md`, `BLOCKED.md`, `_LOCKED.md`.
- **`BLOCKED.md` never marks success.** It is a user-directed recovery handoff, consumed only when explicitly passed to stage 1, 2, or 3. It does not alter done-file recovery or auto-replan anything.

## Schema Fidelity

The repo-root `README.md` `## Schemas` section is authoritative for editing this source repo. `H20/CONTRACT.md` must stay aligned for copied payloads. Each core prompt ends with a `Contract: ./H20/CONTRACT.md` reference because copied target projects may not have the source repo README.

When editing core prompts, keep these files mutually consistent in the same change:

- `README.md`
- `H20/CONTRACT.md`
- `H20/1-clarify-task.md`
- `H20/2-generate-master-plan.md`
- `H20/3-emit-steps.md`
- `H20/4-execute-step.md`

## Editing The Meta-Prompts

- Keep shipped prompts agent-agnostic. Do not add Claude-only syntax, slash commands, or tool-name assumptions to the core payload.
- Each prompt is pasted into a fresh context and must stand alone. Cross-reference other H20 artifacts by path, not assumed memory.
- Phase ordering is load-bearing. Stage 4 phase 1 must remain the locked-milestone and done-file recovery check.
- Anti-drift and anti-footgun sections are regression fences. Add to them only when a concrete failure mode needs coverage.
- Make surgical edits. Do not rewrite adjacent prose or examples unless needed for contract coherence.
- Preserve execution-critical literals. Exact commands, config blocks, env vars, ignore patterns, file/path lists, validation queries, rollback steps, and security exclusions must not become vague references.

## Extras

Optional helpers live under `./H20/Extras/`. They are outside the core contract and must not redefine schemas, recovery semantics, or the core/non-core boundary.

Current helpers:

- `1-clarify-task-assume-defaults.md` — fast-path task writer for small, local, low-ambiguity tasks. It writes normal milestone artifacts, but refuses broad, architecture-shaping, or terminology-conflicting requests.
- `3a-env-checker` — advisory shell script that scans a milestone or step file and prints likely environment capabilities to validate.
- `4-autoexec-claude` — Claude Code wrapper that loops over pending steps.
- `4-autoexec-codex` — Codex CLI wrapper that loops over pending steps.
- `5-review.md` — independent review helper that writes immutable review artifacts under `./H20/Reviews/`.
- `pullh20` — payload sync helper for copied H20 directories.

Autoexec wrappers may append these executor overlay lines:

- `AUTOEXEC_MODE=1`
- `AUTOEXEC_SKIP_HUMAN=1`

These overlays do not change `_LOCKED.md`, done-file recovery, partial-run recovery, blocker semantics, or schemas.

## Maintenance Checks

Useful checks after prompt or doc edits:

```bash
rg -n "## Schemas|Contract:|AUTOEXEC_MODE|AUTOEXEC_SKIP_HUMAN" README.md H20/CONTRACT.md H20/*.md H20/Extras/*.md
git diff -- README.md H20/CONTRACT.md H20/*.md H20/Extras/*.md H20/RawPrompts/0_placeholder-for-raw-user-prompts.txt
bash -n H20/Extras/3a-env-checker H20/Extras/4-autoexec-claude H20/Extras/4-autoexec-codex H20/Extras/pullh20 H20/Extras/helpers/claude-stream
python3 -m py_compile H20/Extras/helpers/stream-formatter.py
```

Optional helper scripts should print syntax help when run with no args:

```bash
./H20/Extras/3a-env-checker
./H20/Extras/4-autoexec-claude
./H20/Extras/4-autoexec-codex
```

## Working Principles

These principles apply when editing H20 itself and are the behavior H20 should encourage in downstream coding agents.

### Think Before Editing

- State assumptions explicitly.
- If two interpretations would change the contract, stop and surface them.
- If a simpler task shape fits the user's goal, say so.

### Simplicity First

- Add the minimum text or code that solves the actual problem.
- Do not add speculative features, abstractions, or workflow layers.
- If prose can be shorter without losing precision, make it shorter.

### Surgical Changes

- Touch only files needed for the request.
- Match existing style.
- Clean up only the mess created by your own edits.
- Mention unrelated issues instead of silently fixing them.

### Verifiable Goals

- For multi-file edits, define the check before editing.
- Prefer concrete verification over vague confidence.
- A prompt change is not done until docs and copied contract artifacts are coherent with it.
