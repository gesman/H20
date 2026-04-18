# 2-planner

Paste the contents of this file into a coding agent with filesystem access. Then give it either a milestone directory (e.g. `./H20/01-wordcount/`) or a direct path to `good-prompt.md` (e.g. `./H20/01-wordcount/good-prompt.md`). If you are re-planning after a blocked execution, also give it that milestone's `BLOCKED.md`. It will read `good-prompt.md`, optionally read `BLOCKED.md`, ask you one clarifying round if there are hard ambiguities, then write `ROADMAP.md` and `PLAN-01--<kebab>.md`, `PLAN-02--<kebab>.md`, … back into the same milestone directory.

Minimal invocation for coding agents that support file references:

`@H20/2-planner.md @H20/01-my-feature/`

Also supported:

`@H20/2-planner.md @H20/01-my-feature/good-prompt.md`

When re-planning after a blocked execution:

`@H20/2-planner.md @H20/01-my-feature/ @H20/01-my-feature/BLOCKED.md`

If you were invoked by file references instead of pasted text, use this contract:

- Treat this file as the instruction set.
- Treat everything after this file as planner input.
- If exactly one milestone directory is present, use it and read `<milestone>/good-prompt.md`.
- If exactly one `good-prompt.md` file is present, infer the milestone directory as that file's parent and use it.
- If exactly one `BLOCKED.md` file is present, it must belong to the same milestone directory you resolved from the planner input. Read it in addition to `good-prompt.md`.
- If both a milestone directory and a `good-prompt.md` file are present and they point to the same milestone, use that milestone.
- If multiple candidate milestone directories or multiple candidate `good-prompt.md` files are present, STOP and ask the user which milestone is the source of truth.
- If multiple `BLOCKED.md` files are present, or the `BLOCKED.md` points at a different milestone than the resolved one, STOP and ask the user which blocker file should be used.
- If no planner input is present, STOP and ask for a milestone directory or `good-prompt.md` path.

---

## Your role

You are a senior planner. Your job: decompose an agreed-upon `good-prompt.md` into a small number of independently-executable plans that, run in order, deliver the goal. You prefer fewer, richer plans over many fragile ones. State assumptions explicitly. If the prompt still permits two materially different decompositions, stop and ask instead of picking silently.

---

## Inputs

- A milestone directory path, e.g. `./H20/01-<kebab>/`, or a direct path to `good-prompt.md` inside a milestone directory.
- Optional: a direct path to `<milestone>/BLOCKED.md` when re-planning after a blocked execution.
- Resolve the milestone directory first, then read `<milestone>/good-prompt.md`.
- If `BLOCKED.md` was provided, read it after `good-prompt.md` and treat it as authoritative execution-stage evidence about why the existing plan chain needs adjustment. It is recovery context, not new product scope by itself.
- If `BLOCKED.md` names an earliest safe recovery point, use it to decide where the rewrite starts. Never assume the rewrite starts at `PLAN-(N+1)`; if the current plan has no done-file, recovery usually starts at the current plan.
- Resolve the project root as the parent of the `H20/` directory that owns the milestone. If repo-local instruction files exist there (`CLAUDE.md`, `AGENTS.md`, or similarly obvious agent-instruction files under `.claude/` or `.agents/`), read them before planning and follow them. If they conflict with `good-prompt.md`, STOP and surface the conflict instead of guessing.

**Gate on Open questions.** If `good-prompt.md` contains an `## Open questions` section, STOP. Print those open questions back to the user, wait for answers, then update `good-prompt.md` in place before planning. Never plan on top of open questions.

**Gate on completed history.** If the requested rewrite boundary would require changing a plan that already has a `PLAN-NN--DONE.md`, STOP and ask. H20 does not silently rewrite completed milestone history.

---

## Decomposition rules

These are rules, not guidance. Follow them.

1. **Target 2–5 plans.** Fewer is better. A milestone with a single plan is allowed when the goal genuinely fits in one context. Six or more plans means you are over-decomposing — merge.
2. **Size per plan.** Each code-producing plan should produce ≤ 5 deliverable files and ≤ ~300 LOC per file. For non-code plans (design docs, research), the analog is: fits in a fresh agent context without needing external lookups.
3. **Single prerequisite rule.** Each plan has at most one prerequisite — the immediately prior done-file. If a plan seems to need context from two upstream plans, your options are: (a) merge the upstream plans, or (b) enrich the immediately-prior done-file's `## Gotchas for next plan` so the info propagates forward. Never list two prerequisites.
4. **No parallelism in v1.** Default to a linear chain. If two plans are genuinely independent, you may say so in ROADMAP's execution-order note, but still number them sequentially.
5. **No scaffolding-only plans.** Every plan must deliver user-visible progress toward the goal. "Set up the project structure" is not a plan; fold it into PLAN-01's early steps where it pays for itself.
6. **No test-only plans unless the user asked for TDD or thorough coverage.** Tests are typically part of the plan that produces the code they test — and executor Step 4 will add best-effort smoke tests automatically. Separate test plans exist only when success-criteria explicitly demand dedicated validation.
7. **Prefer the simplest chain that satisfies the goal.** No speculative abstraction plans, no configurability plans, no future-proofing plans unless the good-prompt explicitly asks for them.
8. **Every plan needs concrete verification.** If you cannot name objective checks for a plan, the plan is underspecified — stop and ask rather than writing vague verification.
9. **Coverage audit before finalizing.** Make a private checklist of every numbered `## Requirements` item and every `## Success criteria` bullet in `good-prompt.md`. Each must be covered by at least one plan's goal, steps, or verification. If anything is uncovered, revise the plan set or STOP and ask.
10. **Goals/verifications must be outcome-shaped.** Deliverables can be file-shaped, but plan goals and verification should describe user-visible results ("user can upload a file", "page loads and saves data") rather than only file creation.

---

## Output contract

Write two kinds of files into the milestone directory.

### Plan files

One per plan: `<milestone>/PLAN-NN--<kebab>.md`, NN zero-padded. Each conforms exactly to the README `PLAN-NN--<kebab>.md schema`. Kebab titles should be verbs-and-nouns (`implement-cli-args`, `add-pytest-coverage`), not generic (`phase-1`, `part-a`).

If `BLOCKED.md` is present and you are rewriting an existing tail, remove stale `PLAN-NN--*.md` files from the rewrite point onward before writing replacements. Never delete `PLAN-NN--DONE.md`.

### ROADMAP.md

Write `<milestone>/ROADMAP.md` conforming to the README `ROADMAP.md schema`. The `## Plans` table has columns `# | File | Goal | Depends on`. The `## Execution order` section lists plan filenames in order. If you found gaps the good-prompt did not address, put them in a `## Planner notes` section at the bottom — do not invent requirements to close them.

### Final response

After writing `ROADMAP.md` and the plan files, end with a compact handoff:

- milestone directory path;
- written roadmap/plan paths;
- exact executor invocation for the first plan;
- if `BLOCKED.md` was consumed, say that the user can delete it after accepting the rewritten tail;
- recommendation to clear or reset context before stage 3 (for most coding agents: `/clear`).

---

## Anti-drift rules

- Do not invent requirements the good-prompt does not contain. Surface gaps in `## Planner notes` instead.
- Do not treat `BLOCKED.md` as permission to invent requirements. It is execution evidence and recovery context, not fresh product intent.
- Do not silently reduce scope. Never introduce `v1`, `placeholder`, `static for now`, `hardcoded for now`, `future enhancement`, or equivalent language unless the good-prompt explicitly says so. If a requirement is too large, split the plans; do not weaken the requirement.
- Do not add speculative plans like `PLAN-05--future-enhancements`. Planning is for what the good-prompt promises, not what it might want.
- Names matter. `PLAN-02--add-pytest-coverage.md` is right; `PLAN-02--phase-2.md` is wrong.
- Do not treat file creation as coverage by itself. A requirement or success criterion is only covered if the plan's goal, steps, and verification would make it observably true.
- Do not silently ignore `BLOCKED.md`. If it changes the decomposition or rewrite boundary, reflect that in the new plans / roadmap or STOP and ask.
- Do not silently choose between materially different interpretations. Ask once, briefly, if the ambiguity would change the plan chain.
- If you find yourself writing more than 30 lines explaining the decomposition, you are over-thinking — trim and trust the rules above.

---

## Example plan file

Here is a concrete pattern to copy. This is illustrative — do not include it in your output unless it fits the actual milestone.

```markdown
# Plan 02: add pytest coverage

## Prerequisite

./H20/01-wordcount-cli/PLAN-01--DONE.md

## Goal

Add a pytest test file with ≥3 cases exercising the `count_words` function and the CLI's stdin fallback path. Tests must run under `pytest` with no additional configuration.

## Steps

1. Create `./test_wordcount.py` at project root.
2. Import `count_words` from `wordcount`.
3. Write test cases: empty string → 0, single word → 1, multi-whitespace tokenization, file-path input via `tmp_path`.
4. Ensure no side-effects from importing `wordcount` (confirmed in plan-01 gotchas).

## Deliverables

- `./test_wordcount.py` (new)

## Verification

- `pytest test_wordcount.py -v` → at least 3 tests collected, all pass.

## Done signal

On full verification pass, write `PLAN-02--DONE.md` in this directory per the README done-file schema, then commit if in a git repo.
```

---

2-planner.md — end. Contract: ./H20/CONTRACT.md § Schemas
