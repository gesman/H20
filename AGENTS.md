# Repository Guidelines

## Project Structure & Module Organization

This repository is documentation-first. The product payload lives in [`H20/`](/home/gesman/PROJECTS/H2/H20): `1-create-prompt.md`, `2-planner.md`, and `3-executor.md`. The root [`README.md`](/home/gesman/PROJECTS/H2/README.md) is the authoritative contract for directory layout, schemas, and recovery rules. [`CLAUDE.md`](/home/gesman/PROJECTS/H2/CLAUDE.md) contains repo-specific agent notes. `0_readme.txt` is a quick-start reference, not the source of truth.

## Build, Test, and Development Commands

There is no build system, runtime, or package manager in this repo. Useful maintenance commands:

- `cp -R H20 /tmp/demo-project/H20` copies the payload into a throwaway project for manual validation.
- `rg -n "## Schemas|Contract:" README.md H20/*.md` checks that prompt files still point at the README schema contract.
- `git diff -- README.md H20/*.md AGENTS.md` reviews the contributor-facing surface before commit.

## Coding Style & Naming Conventions

Edit in plain Markdown only. Match the existing style: ATX headings, short imperative paragraphs, hyphen bullets, and fenced code blocks for examples. Keep instructions agent-agnostic; do not introduce Claude-, Codex-, or tool-specific syntax into the shipped prompts. Preserve load-bearing names exactly: milestone dirs use `NN-<kebab>`, plans use `PLAN-NN--<kebab>.md`, and recovery files remain `PLAN-NN--DONE.md`.

## Testing Guidelines

There is no automated test suite yet. Validation is manual and contract-based:

- Re-read `README.md` `## Schemas` after changing any prompt file.
- Keep `README.md` and all three files in `H20/` mutually consistent in the same change.
- When changing executor behavior, confirm the done-file recovery rule and single-prerequisite rule still read clearly and consistently.

## Commit & Pull Request Guidelines

This repository currently has no commit history, so follow a simple convention: short imperative subjects, optionally scoped, such as `docs: tighten executor recovery wording`. Keep PRs narrow. Describe which files changed, what contract changed, and whether README schema text was updated to match. Screenshots are unnecessary; before/after prompt excerpts are more useful for review.

## Agent-Specific Notes

Assume contributors may edit these files through coding agents. Changes that silently weaken schema fidelity, filename conventions, or recovery semantics are regressions, even if the prose reads better.
