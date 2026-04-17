# H20 — lean coding-agent harness

H20 is three markdown prompts and a directory convention for coding agents with filesystem access. It turns a vague idea into a working project through three pasteable meta-prompts, with fresh context per step so nothing rots. It is **not** an installer, **not** a framework, and **not** tied to one coding agent vendor. There is no CLI, no hooks, no runtime. Copy four files, paste into your coding agent of choice, done.

## Why H20

- **Context rot is the silent killer of complex projects, and H20 is built around defeating it.** Big goals die when one bloated session has to hold the whole product in its head. H20 shards the work into milestones, then into plans, and demands a fresh context window at every stage boundary. Each plan carries forward only the immediately prior done-file — a hand-written summary, not a conversation replay. Ambitious multi-month projects stay coherent because no single context ever has to.
- **Pick the right agent for the right plan.** The three meta-prompts use no agent-specific syntax, so a single milestone can flow across tools: scaffold the backend in Codex, design the UI in Claude Code, hand a tricky migration to Aider, verify in Cursor. Every handoff is just "paste the executor prompt into a different agent and name the next plan file." No lock-in, no re-setup, no translation layer.
- **The leanest, meanest harness you'll find — zero dependencies, zero bloat.** Four markdown files. No npm package, no Python wheel, no CLI binary, no config, no telemetry, no daemon, no state database. The entire state machine is "does `PLAN-NN--DONE.md` exist on disk?". If H20 ever stops being useful to you, `rm -rf H20/` deletes it without trace. Nothing about your project depends on it.

## Design axioms

1. **Coding-agent-agnostic.** The three meta-prompts are written for coding agents with filesystem access (Claude Code, Codex, and similar tools). No agent-specific syntax ever.
2. **Zero install, zero runtime.** Copy-paste is the install. No Node, Python, bash, or dependencies.
3. **Self-contained inside `./H20/`.** Every artifact H20 touches — meta-prompts, raw prompts, plans, summaries — lives under `./H20/` of the target project. Nothing spills to the project root.
4. **Numbered milestones track evolution.** `./H20/01-<kebab>/`, `./H20/02-<kebab>/`, … give you a scannable history of what you've built and when.
5. **File-existence recovery.** A plan is "done" iff its `PLAN-NN--DONE.md` exists. No state machinery, no manifest drift.
6. **Shallow dependencies.** Each plan references at most the immediately prior done-file. Rich summaries kill spiderweb chains.

## Flow

```
raw prompt (verbal or ./H20/NN-<kebab>/raw-prompt.txt)
    │
    ▼   paste 1-create-prompt.md + raw prompt into a coding agent
    │
    │   Phase 1 — Research-need judgment
    │     LLM evaluates: does this prompt need tech/framework/
    │     platform research? (underspecified stack, multiple
    │     reasonable implementation paths, external integrations,
    │     ambiguous runtime, domain-specific tooling)
    │
    │   Phase 2 — Research offer (conditional)
    │     If needs-research: print recommendation + opt-in prompt.
    │     User picks: (a) research now, (b) skip — I'm opinionated.
    │     If not-needed: proceed straight to grilling.
    │
    │   Phase 3 — Research (conditional on opt-in)
    │     LLM researches (web search if available, else training
    │     knowledge). Presents a pros/cons table per decision axis.
    │     User picks options. Decisions captured for good-prompt.
    │
    │   Phase 4 — Grilling
    │     LLM asks 3–7 clarifying questions (multi-choice where
    │     possible), waits for answers. Up to 3 rounds.
    │
    │   Phase 5 — Writing
    │     LLM picks next NN, creates ./H20/NN-<kebab>/, writes:
    │       - raw-prompt.txt (input + research+Q&A transcript)
    │       - good-prompt.md (structured, per README schema)
    │
    ▼   paste 2-planner.md + point at ./H20/NN-<kebab>/
    │   coding agent writes:
    │     - ROADMAP.md
    │     - PLAN-01--<kebab>.md, PLAN-02--<kebab>.md, …
    │
    ▼   paste 3-executor.md + name one plan file
    │   LLM checks PLAN-NN--DONE.md; if exists, stops.
    │   Otherwise loads context, requests tools/MCPs/skills
    │   (agent-specific), executes with best-effort tests,
    │   runs verification, writes PLAN-NN--DONE.md, commits
    │   (if git repo).
    │
    ▼   next plan reads only the immediately prior done-file
```

## Directory layout

Inside a target project using H20:

```
./H20/
├── 1-create-prompt.md         (meta-prompt; copy from source or paste)
├── 2-planner.md               (meta-prompt)
├── 3-executor.md              (meta-prompt)
├── README.md
├── 01-<first-milestone>/
│   ├── raw-prompt.txt
│   ├── good-prompt.md
│   ├── ROADMAP.md
│   ├── BLOCKED.md                  (optional; only when a blocked execution writes it)
│   ├── PLAN-01--<kebab>.md
│   ├── PLAN-01--DONE.md            (only after successful execution)
│   ├── PLAN-02--<kebab>.md
│   └── PLAN-02--DONE.md
├── 02-<second-milestone>/
│   └── …
└── example/                       (reference walkthrough)
```

Milestones start at `01`, two-digit zero-padded, kebab-case title. Plans and their done-files live **inline** in the milestone dir — there is NO `plans/` or `summaries/` subdir.

## File-naming rules

- **Meta-prompts:** `N-<kebab>.md` at `./H20/` root, where `1` = create-prompt, `2` = planner, `3` = executor. The numbers guide first-time readers on the order to use them; they are otherwise cosmetic.
- **Milestones:** `NN-<kebab>/` where NN is `01`..`99`.
- **Plans:** `PLAN-NN--<kebab>.md`, NN `01`..`99`, zero-padded.
- **Done-files:** `PLAN-NN--DONE.md` — no title suffix, so existence check is trivial.
- **Raw prompt:** always exactly `raw-prompt.txt`.
- **Good prompt:** always exactly `good-prompt.md`.
- **Roadmap:** always exactly `ROADMAP.md`.
- **Blocked handoff:** optional milestone-root `BLOCKED.md`. At most one unresolved blocker file per milestone.

## Schemas

### good-prompt.md schema

- `# Goal` — one paragraph, imperative voice.
- `## Context` — tech stack, target runtime, relevant existing code, users. Research-phase decisions land here (e.g. "Framework: FastAPI — picked over Flask because …").
- `## Requirements` — numbered list. Each item is one testable requirement.
- `## Non-goals` — explicit scope exclusions.
- `## Success criteria` — bulleted, verifiable (command, test, observable behavior).
- `## Research notes` (optional) — only present if the create-prompt research phase ran. Briefly records each decision axis researched, the options considered (pros/cons), and the choice made. One short paragraph per axis. Omit entirely if research was skipped.
- `## Open questions` (optional) — only present if 1-create-prompt could not get answers despite grilling. Omit entirely when empty.

### ROADMAP.md schema

- `# Roadmap: <milestone title>`
- `## Plans` — table with columns: `# | File | Goal | Depends on`.
- `## Execution order` — linear list of plan filenames in execution order. Mention parallelism only if plans are truly independent; default is sequential.
- `## Planner notes` (optional) — gaps surfaced during planning that good-prompt did not address; for the executor or the user to resolve later. Omit if empty.

### PLAN-NN--<kebab>.md schema

- `# Plan NN: <title>`
- `## Prerequisite` — either `none` or a single line naming the immediately prior done-file, e.g. `./H20/01-wordcount/PLAN-01--DONE.md`. H20 enforces **at most one prerequisite per plan**. If a plan seems to need two upstream done-files, the planner should merge plans or fold context into the nearest done-file's gotchas.
- `## Goal` — one paragraph; what this plan achieves end-to-end.
- `## Steps` — numbered list; each step small, specific, verifiable.
- `## Deliverables` — files created or modified, with relative paths.
- `## Verification` — concrete commands/checks the executor must run (e.g. `pytest tests/test_wordcount.py`, or "open http://localhost:3000 and confirm the dashboard loads"). If a verification item needs human judgment, the executor must do the setup first (start server, seed data, print URL/steps), then stop for `approved` or `skip`.
- `## Done signal` — literal: "On full verification pass, write `PLAN-NN--DONE.md` in this directory per the README done-file schema, then commit if in a git repo."

### PLAN-NN--DONE.md schema

- `# PLAN-NN DONE: <title>`
- `## Summary` — 3–6 bullets: what was built, key decisions, **plus** bullets (when applicable) noting (a) the capability-request outcome from executor Step 3, (b) any best-effort tests added during Step 4 or a line that tests were not applicable, and (c) any human-verification outcome from Step 5 (`approved`, `skip`, or `not needed`).
- `## Files changed` — bullet list of paths (including any executor-added test files).
- `## Verification results` — one line per verification check: `✅`, `❌`, or `⚠ skipped`, plus the command/check (includes executor-added tests even when the plan did not list them).
- `## Gotchas for next plan` — anything the next plan needs to know: APIs added, signatures differing from plan assumptions, env vars required, known limitations, test-file locations and fixtures. Write full sentences so a fresh-context agent can absorb it without reading upstream code. Empty is OK but usually means you under-documented.
- `## Commit` — if in a git repo, the commit SHA and subject; otherwise "not a git repo — no commit".

### BLOCKED.md schema

- `# BLOCKED: PLAN-NN <title>` — names the incomplete plan that hit the blocker.
- `## What happened` — one paragraph: what stopped execution and why the current plan could not safely continue.
- `## Evidence` — bullet list of concrete observations: commands, errors, file paths, API responses, or contradictions in the codebase / environment.
- `## Earliest safe recovery point` — one of `resume current plan`, `replan from current plan`, `redo good-prompt`, or `start new milestone`, followed by one-sentence reasoning. The executor must never point recovery at a later plan while the current plan has no done-file.
- `## Workspace state` — bullets covering files already touched, what is safe to keep, what is safe to discard, and any verification already run.
- `## Suggested user actions` — 2 or 3 labeled options (`A.`, `B.`, optional `C.`), with exactly one marked recommended. Each option names the exact next move (edit, planner invocation, create-prompt invocation, or external action) and a one-sentence why.

## Recovery rule

Before executing `PLAN-NN--<kebab>.md`, check if the sibling `PLAN-NN--DONE.md` exists in the same milestone directory. If yes, stop and report `PLAN-NN already executed`. If no, execute. To re-run a plan, **delete its done-file** manually. That is the entire recovery mechanism. `BLOCKED.md` never marks a plan complete and does not alter the done-file recovery rule; it is only a user-directed handoff artifact.

## Interrupted runs

H20 auto-recovers **completed** plans via done-files. It does **not** silently recover partial runs. If a coding agent crashed before writing `PLAN-NN--DONE.md`, the next executor run should first check for workspace drift: already-created deliverables from the plan, or unrelated dirty files in the worktree. If either is present, stop and ask the user whether to inspect, clean up, or intentionally continue. Do not bulldoze through suspected partial state.

## Blocked runs

If execution hits a durable blocker that makes the current plan unsafe to complete, the executor should write milestone-root `BLOCKED.md` and stop without writing a done-file or making a commit. Durable blockers include invalidated plan assumptions, missing external access or credentials, product decisions the current plan cannot safely guess, or external constraints that change the implementation path.

Do **not** use `BLOCKED.md` for ordinary clarifying chat, dirty-worktree checks, suspected partial-run detection, or planned human-only verification pauses already covered elsewhere in the executor flow.

`BLOCKED.md` is consumed only when the user explicitly passes it into `2-planner.md` or `1-create-prompt.md`. Its presence on disk alone does not auto-replan anything.

After the user chooses a recovery path and materializes it, delete `BLOCKED.md`. If the milestone is abandoned entirely, keeping `BLOCKED.md` as a tombstone is fine.

## Using H20 on a project

1. Copy `./H20/` into your project root. Files are already ordered by name (`1-…`, `2-…`, `3-…`) so `ls ./H20/` shows the pipeline left to right.
2. Gather raw source material. This can be one file, many files, a directory, pasted text, or any combination.
3. Paste `1-create-prompt.md` content into a coding agent, then your raw input corpus. The agent may recommend a tech/framework research phase — accept or skip based on how opinionated your source material already is. Then answer its grilling questions. You get `good-prompt.md`.
   Shortcuts for coding agents that support file references:
   `@H20/1-create-prompt.md @raw_prompt.txt`
   `@H20/1-create-prompt.md @raw-prompt1.txt @raw-prompt2.txt`
   `@H20/1-create-prompt.md @raw-prompts/`
   If a blocked milestone needs a fresh prompt pass, include the previous raw prompt plus `BLOCKED.md` to create a new milestone with the execution-learned constraint in context:
   `@H20/1-create-prompt.md @H20/01-my-feature/raw-prompt.txt @H20/01-my-feature/BLOCKED.md`
   Recommended after success: clear or reset context before stage 2. In most coding agents: `/clear`.
4. Paste `2-planner.md` into a coding agent, point it at the milestone dir or its `good-prompt.md`. The planner also reads repo-local instruction files if present (`CLAUDE.md`, `AGENTS.md`, or similarly obvious agent-instruction files) and audits that every requirement and success criterion is covered by at least one plan without silently shrinking scope. You get `ROADMAP.md` and the plan files.
   Shortcuts for coding agents that support file references:
   `@H20/2-planner.md @H20/01-my-feature/`
   `@H20/2-planner.md @H20/01-my-feature/good-prompt.md`
   If re-planning after a blocked execution, pass `BLOCKED.md` explicitly so the planner can rewrite the tail from the correct recovery point:
   `@H20/2-planner.md @H20/01-my-feature/ @H20/01-my-feature/BLOCKED.md`
   Recommended after success: clear or reset context before stage 3. In most coding agents: `/clear`.
5. For each plan, paste `3-executor.md` into a coding agent and name the plan file. The executor reads repo-local instruction files if present, may proactively request MCP servers / skills / specific tools that would materially help the plan — reply `ok` to enable, `skip` to proceed best-effort — and adds **best-effort smoke tests** for any code it produces, even if the plan did not call for them. Those smoke tests are implementation hygiene, not new product scope. If a verification check needs human judgment, the executor must prepare the environment first, then pause for `approved` or `skip`; no done-file is written until every human-only check is approved or explicitly waived. If a durable blocker invalidates the current plan, the executor should write `BLOCKED.md` and stop without writing a done-file or commit. If a prior run crashed before a done-file was written, the executor should stop on suspected partial state rather than rerun blindly. Rinse, repeat.
   Shortcut for coding agents that support file references:
   `@H20/3-executor.md @H20/01-my-feature/PLAN-01--build-api.md`
   Recommended after each successful plan: clear or reset context before executing the next plan. In most coding agents: `/clear`.

## Example

`./H20/example/01-wordcount-cli/` is a complete walkthrough of the H20 flow applied to a trivial word-count CLI. Read it top-to-bottom alongside the schemas in this document to see how every contract is exercised. This example illustrates the **research-skip** branch of 1-create-prompt (the raw prompt is opinionated enough that Phase 1 judgment declines research); the research-run branch appears naturally whenever a less-specified prompt is used. It also demonstrates the executor's **capability-request** and **best-effort tests** behaviors — see `PLAN-01--DONE.md`'s `## Summary` and the executor-added `test_wordcount_smoke.py` in `## Files changed`.
