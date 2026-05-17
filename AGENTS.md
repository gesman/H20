# Repository Guidelines

## Project Structure & Module Organization

This repository is a lean markdown-and-script harness for H20. Core prompt files live in `H20/`: `1-clarify-task.md`, `2-generate-master-plan.md`, `3-emit-steps.md`, and `4-execute-step.md`. The root `README.md` is the authoritative contract documentation; keep `H20/CONTRACT.md` in sync when changing schemas, recovery rules, or helper behavior. Optional scripts and prompts live under `H20/Extras/`, with shared helper code in `H20/Extras/helpers/`. `H20/UserDocs/` is a placeholder for user-supplied reference material.

## Build, Test, and Development Commands

There is no package manager, build step, daemon, or runtime for core H20. Use focused syntax and smoke checks:

```bash
bash -n H20/Extras/pullh20
/bin/bash -n H20/Extras/4-autoexec-codex
python3 -m py_compile H20/Extras/helpers/stream-formatter.py
git diff --check
```

For wrapper behavior, prefer `--dry-run` where available, for example:

```bash
H20/Extras/4-autoexec-codex --milestone H20/01-example --dry-run
```

## Coding Style & Naming Conventions

Keep markdown instructional, direct, and schema-stable. Preserve documented file names exactly: `TASK.md`, `MASTER-PLAN.md`, `ROADMAP.md`, `STEP-NN--<kebab>.md`, and `STEP-NN--DONE.md`. Milestones use `NN-<kebab>/`, zero-padded. Shell scripts should be portable across macOS Bash 3.2 and Ubuntu Bash; avoid GNU-only assumptions unless guarded. Use two or four spaces consistently within the touched file.

## Testing Guidelines

No formal test suite exists. Validate changes with the narrowest relevant command plus at least one realistic smoke test for helper scripts. For sync behavior, use temporary directories with a fake `.git` directory and verify preserved paths such as `UserDocs/`, `Reviews/`, `RawPrompts/`, and `NN-*` milestones.

## Commit & Pull Request Guidelines

Recent history uses short subjects such as `Backup`, `Docs update`, and `bu.yaml update`, plus occasional descriptive changes. Prefer concise, descriptive commit subjects for non-backup work, e.g. `Update pullh20 portability`. PRs should explain the contract or helper behavior changed, list verification commands, and call out any migration impact for copied `./H20/` payloads.

## Agent-Specific Instructions

Do not treat `H20/Extras/` as core contract unless the change explicitly targets helpers. When editing contract semantics, update both `README.md` and `H20/CONTRACT.md`. Avoid creating milestone artifacts in this source repo unless the task is specifically about exercising H20 itself.
