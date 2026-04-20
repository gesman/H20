# H20 — Lean coding-agent harness

H20 is three markdown prompts and a directory convention for coding agents with filesystem access. It turns a vague idea into a working project through three pasteable meta-prompts, with fresh context per step so nothing rots. It is **not** an installer, **not** a framework, and **not** tied to one coding agent vendor. 

For copied payloads, the same contract also ships as `./H20/CONTRACT.md` so a project that receives only the `H20/` directory remains self-contained. In this source repo, the root `README.md` remains the authoritative edit target for the contract; keep the payload copy in sync.

Escape from bloated, opinionated, slow, agent-specific harnesses with hairy dependencies. Core H20 has no CLI, no hooks, and no runtime. Copy four files, paste into your coding agent of choice, done. Optional convenience scripts may exist under `./H20/Extras/`, but they are explicitly outside the core contract.

The files under `./H20/` are agent-only instruction files. User-facing usage guidance, examples, and workflow notes live in this README.

## Super quick start

1. Copy `./H20/` into your project root. Start your favorite coding agent, and:
2. Create a milestone:
   `@H20/1-create-prompt.md "Build me a website"` or `@H20/1-create-prompt.md @raw-prompt.txt`
   If your agent supports file references, include the `@`. A bare path like `H20/1-create-prompt.md` is just text in many agents and may cause the raw prompt to be executed directly instead of creating milestone artifacts. If file references are unavailable, paste the contents of `1-create-prompt.md` first, then the raw prompt.
3. Plan it:
   `@H20/2-planner.md @H20/01-my-feature/`
4. Execute one plan per fresh session:
   `@H20/3-executor.md @H20/01-my-feature/PLAN-01--do-this.md`
5. Repeat plan-by-plan. Clear context between runs. If execution writes `BLOCKED.md`, stop and either fix the issue, re-plan with `@H20/2-planner.md @H20/01-my-feature/ @H20/01-my-feature/BLOCKED.md`, or start a new milestone with the old `raw-prompt.txt` plus `BLOCKED.md`.
6. Optional: if you use Claude Code or Codex and want a thin loop wrapper around repeated executor runs, use one of:

   `./H20/Extras/3-autoexec-claude --milestone ./H20/01-my-feature --model opus --skiphuman [--steps 2]`
   
   `./H20/Extras/3-autoexec-codex --milestone ./H20/01-my-feature --model gpt-5.4 --skiphuman [--steps 2]`

   These are non-core convenience scripts, not part of the H20 contract. They repeatedly invoke the next pending plan(s), pass `AUTOEXEC_MODE=1`, and stop on `BLOCKED.md`, missing done-file creation, or a human-verification handoff. Add `--skiphuman` only when you want human-only checks recorded as skipped.

## Why H20

- **Context rot is the silent killer of complex projects, and H20 is built around defeating it.** Big goals die when one bloated session has to hold the whole product in its head. H20 shards the work into milestones, then into plans, and demands a fresh context window at every stage boundary. Each plan carries forward only the immediately prior done-file — a hand-written summary, not a conversation replay. Ambitious multi-month projects stay coherent because no single context ever has to.
- **Pick the right agent for the right plan.** The three meta-prompts use no agent-specific syntax, so a single milestone can flow across tools: scaffold the backend in Codex, design the UI in Claude Code, hand a tricky migration to Aider, verify in Cursor. Every handoff is just "paste the executor prompt into a different agent and name the next plan file." No lock-in, no re-setup, no translation layer.
- **The leanest, meanest harness you'll find — zero dependencies, zero bloat.** Four markdown files. No npm package, no Python wheel, no CLI binary, no config, no telemetry, no daemon, no state database. The entire state machine is "does `PLAN-NN--DONE.md` exist on disk?". If H20 ever stops being useful to you, `rm -rf H20/` deletes it without trace. Nothing about your project depends on it.

## Design axioms

1. **Coding-agent-agnostic.** The three meta-prompts are written for coding agents with filesystem access (Claude Code, Codex, and similar tools). No agent-specific syntax ever.
2. **Zero install, zero runtime in the core.** Copy-paste is the install. No Node, Python, bash, or dependencies are required for the core flow. Optional helpers under `./H20/Extras/` are convenience tooling, not part of the contract.
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
    │     knowledge). Presents numbered choice cards per decision
    │     axis, with recommendation + reply format.
    │     User picks options. Decisions captured for good-prompt.
    │
    │   Phase 4 — Grilling
    │     LLM asks 3–7 clarifying questions in a compact numbered
    │     batch, waits for answers. Up to 3 rounds.
    │
    │   Phase 5 — Writing
    │     LLM picks next NN, creates ./H20/NN-<kebab>/, writes:
    │       - raw-prompt.txt (input + research+Q&A transcript)
    │       - good-prompt.md (structured, per contract schema)
    │
    ▼   paste 2-planner.md + point at ./H20/NN-<kebab>/
    │   coding agent writes:
    │     - ROADMAP.md
    │     - PLAN-01--<kebab>.md, PLAN-02--<kebab>.md, …
    │
    ▼   paste 3-executor.md + name one plan file
    │   LLM checks PLAN-NN--DONE.md; if exists, stops.
    │   Otherwise loads context, uses available
    │   tools/MCPs/skills proactively, executes with
    │   best-effort tests, escalates only on real
    │   environment blockers or human-only verification,
    │   writes PLAN-NN--DONE.md, commits
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
├── Extras/                    (optional convenience prompts and scripts; non-contractual)
│   ├── 2a-env-checker
│   ├── 3-autoexec-claude
│   ├── 3-autoexec-codex
│   ├── 4-review.md
│   ├── README.md
│   └── helpers/               (support files used by optional extras)
├── Reviews/                   (optional review snapshots; non-contractual)
│   └── 01-<first-milestone>/
│       ├── REVIEW-01.md
│       └── raw-review-prompt-01.md
├── CONTRACT.md
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
- **Review snapshots:** optional `./H20/Reviews/NN-<kebab>/REVIEW-NN.md`, where the directory name matches the reviewed milestone and the review file number is local to that review directory.
- **Review follow-up prompts:** optional `./H20/Reviews/NN-<kebab>/raw-review-prompt-NN.md`, paired with the review snapshot that produced it.

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
- `## Prerequisite` — either `none` or a single line naming the immediately prior done-file, e.g. `./H20/01-my-feature/PLAN-01--DONE.md`. H20 enforces **at most one prerequisite per plan**. If a plan seems to need two upstream done-files, the planner should merge plans or fold context into the nearest done-file's gotchas.
- `## Goal` — one paragraph; what this plan achieves end-to-end.
- `## Steps` — numbered list; each step small, specific, verifiable.
- `## Deliverables` — files created or modified, with relative paths.
- `## Verification` — concrete commands/checks the executor must run (e.g. `pytest tests/test_feature.py`, or "open http://localhost:3000 and confirm the dashboard loads"). If a verification item needs human judgment, the executor must do the setup first (start server, seed data, print URL/steps), then stop for `approved` or `skip`.
- `## Done signal` — literal: "On full verification pass, write `PLAN-NN--DONE.md` in this directory per the README done-file schema, then commit if in a git repo."

### PLAN-NN--DONE.md schema

- `# PLAN-NN DONE: <title>`
- `## Summary` — 3–6 bullets: what was built, key decisions, **plus** bullets (when applicable) noting (a) the capability-use outcome from executor Step 3 (`used`, `best-effort fallback`, `blocked`, or `not needed`), (b) any best-effort tests added during Step 4 or a line that tests were not applicable, and (c) any human-verification outcome from Step 5 (`approved`, `skip`, or `not needed`).
- `## Files changed` — bullet list of paths (including any executor-added test files).
- `## Verification results` — one line per verification check: `✅`, `❌`, or `⚠ skipped`, plus the command/check (includes executor-added tests even when the plan did not list them).
- `## Gotchas for next plan` — anything the next plan needs to know: APIs added, signatures differing from plan assumptions, env vars required, known limitations, test-file locations and fixtures. Write full sentences so a fresh-context agent can absorb it without reading upstream code. Empty is OK but usually means you under-documented.
- `## Commit` — if in a git repo, record `same commit as this done-file — subject: plan-NN: <title>`; otherwise `not a git repo — no commit`. The executor's final handoff should print the actual SHA separately because a tracked file cannot contain its own final commit ID without changing that ID.

### BLOCKED.md schema

- `# BLOCKED: PLAN-NN <title>` — names the incomplete plan that hit the blocker.
- `## What happened` — one paragraph: what stopped execution and why the current plan could not safely continue.
- `## Evidence` — bullet list of concrete observations: commands, errors, file paths, API responses, or contradictions in the codebase / environment.
- `## Earliest safe recovery point` — one of `resume current plan`, `replan from current plan`, `redo good-prompt`, or `start new milestone`, followed by one-sentence reasoning. The executor must never point recovery at a later plan while the current plan has no done-file.
- `## Workspace state` — bullets covering files already touched, what is safe to keep, what is safe to discard, and any verification already run.
- `## Suggested user actions` — 2 or 3 labeled options (`A.`, `B.`, optional `C.`), with exactly one marked recommended. Each option names the exact next move (edit, planner invocation, create-prompt invocation, or external action) and a one-sentence why.

### Optional review artifacts

These artifacts are produced only by non-core helpers such as `./H20/Extras/4-review.md`. They live under `./H20/Reviews/` and do **not** change milestone completion semantics, done-file recovery, or executor behavior.

### REVIEW-NN.md schema

- `# Review NN: <reviewed milestone title>`
- `## Reviewed scope` — the reviewed milestone path, whether the run covered the whole milestone or a specific completed plan, and any explicit exclusions.
- `## Review basis` — review run date, reviewer / agent label if known, done-files used to derive scope, and files actually inspected.
- `## Seeded concerns` (optional) — concerns injected by the user as pasted text and/or referenced files. Each entry should record the original concern, its source, the outcome (`confirmed`, `disproved`, `not applicable`, or `inconclusive`), and one-sentence reasoning.
- `## Independent findings` — numbered list, ordered by severity. Each finding should include: severity, issue, evidence, affected files or interfaces, and recommended disposition (`carry forward`, `defer`, `cross-cutting`, or `acceptable tradeoff pending user confirmation`).
- `## Deferred or acceptable tradeoffs` (optional) — items the reviewer believes may be acceptable for now but that should be made explicit for the user.
- `## Cross-cutting or unrelated observations` (optional) — important observations that do not cleanly belong in the next milestone derived from this review.
- `## Recommended follow-up milestones` — 1 to 3 concrete next-milestone options, with exactly one marked recommended. Each option should name a narrow goal and the findings it would absorb.

### raw-review-prompt-NN.md schema

- `# Raw review prompt NN: <proposed follow-up title>`
- `## Source review` — path to the paired `REVIEW-NN.md` and one sentence describing the review scope.
- `## Goal` — one paragraph describing the follow-up milestone to create.
- `## Findings included` — numbered list of the review findings intentionally carried into this follow-up scope.
- `## Findings explicitly excluded` — numbered or bulleted list of reviewed findings intentionally left out, deferred, or treated as unrelated.
- `## Constraints` — explicit scope fences, assumptions, and boundaries for the next milestone.
- `## Success criteria` — bulleted, verifiable outcomes expected from the follow-up milestone.

## Recovery rule

Before executing `PLAN-NN--<kebab>.md`, check if the sibling `PLAN-NN--DONE.md` exists in the same milestone directory. If yes, stop and report `PLAN-NN already executed`. If no, execute. To re-run a plan, **delete its done-file** manually. That is the entire recovery mechanism. `BLOCKED.md` never marks a plan complete and does not alter the done-file recovery rule; it is only a user-directed handoff artifact.

## Interrupted runs

H20 auto-recovers **completed** plans via done-files. It does **not** silently recover partial runs. If a coding agent crashed before writing `PLAN-NN--DONE.md`, the next executor run should first check for workspace drift: already-created deliverables from the plan, or unrelated dirty files in the worktree. If either is present, stop and ask the user whether to inspect, clean up, or intentionally continue. Do not bulldoze through suspected partial state.

## Blocked runs

If execution hits a durable blocker that makes the current plan unsafe to complete, the executor should write milestone-root `BLOCKED.md` and stop without writing a done-file or making a commit. Durable blockers include invalidated plan assumptions with no safe in-scope repair, missing external access or credentials, failed or unavailable capabilities or facilities with no safe fallback, or external constraints that change the implementation path.

Do **not** use `BLOCKED.md` for ordinary clarifying chat, dirty-worktree checks, suspected partial-run detection, or planned human-only verification pauses already covered elsewhere in the executor flow.

`BLOCKED.md` is consumed only when the user explicitly passes it into `2-planner.md` or `1-create-prompt.md`. Its presence on disk alone does not auto-replan anything.

After the user chooses a recovery path and materializes it, delete `BLOCKED.md`. If the milestone is abandoned entirely, keeping `BLOCKED.md` as a tombstone is fine.

## Optional executor overlays

Optional convenience wrappers may append literal control lines after the plan path in executor input:

- `AUTOEXEC_MODE=1` — executor Step 3 must use any already-available capabilities without pausing; if a required capability is missing or failing and no safe fallback exists, the executor should write `BLOCKED.md` and stop.
- `AUTOEXEC_SKIP_HUMAN=1` — human-only verification may be recorded as `⚠ skipped` after the executor performs all automatable setup. Without this explicit marker, human-only verification still pauses for user input even in autoexec mode.

These overlays do **not** change the done-file recovery rule, partial-run detection, blocker semantics, or milestone schemas.

## Using H20 on a project

1. Copy `./H20/` into your project root. Files are already ordered by name (`1-…`, `2-…`, `3-…`) so `ls ./H20/` shows the pipeline left to right.
2. Gather raw source material. This can be one file, many files, a directory, pasted text, or any combination.
3. Paste `1-create-prompt.md` content into a coding agent, then your raw input corpus. The agent may recommend a tech/framework research phase — accept or skip based on how opinionated your source material already is. Then answer its grilling questions, which should include clearly marked recommended options when a default is justified by the corpus. The grilling output should always separate the neutral reply format from the recommended-default answer set, rather than overloading one line to do both. You get `good-prompt.md`.
   Shortcuts for coding agents that support file references:
   `@H20/1-create-prompt.md @raw_prompt.txt`
   `@H20/1-create-prompt.md @raw-prompt1.txt @raw-prompt2.txt`
   `@H20/1-create-prompt.md @raw-prompts/`
   Do not use a bare path like `H20/1-create-prompt.md` and expect the agent to load it. In many agents that is only plain text; use `@H20/1-create-prompt.md` or paste the file contents.
   When using pasted mode, the project description that follows is source material for stage 1 only. The agent should synthesize `raw-prompt.txt` and `good-prompt.md`, not directly analyze, plan, or implement the project itself.
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
5. For each plan, paste `3-executor.md` into a coding agent and name the plan file. The executor reads repo-local instruction files if present, uses any already-available MCP servers / skills / specific tools proactively, and adds **best-effort smoke tests** for any code it produces, even if the plan did not call for them. Those smoke tests are implementation hygiene, not new product scope. The executor should involve the user only when a required capability or facility is missing or failing with no safe fallback, when an auth / approval gate is unavoidable, or when a verification check truly requires human judgment after the executor has already prepared all automatable setup. No done-file is written until every human-only check is approved or explicitly waived. If a durable blocker invalidates the current plan, the executor should write `BLOCKED.md` and stop without writing a done-file or commit. If a prior run crashed before a done-file was written, the executor should stop on suspected partial state rather than rerun blindly. Rinse, repeat.
   Shortcut for coding agents that support file references:
   `@H20/3-executor.md @H20/01-my-feature/PLAN-01--build-api.md`
   Recommended after each successful plan: clear or reset context before executing the next plan. In most coding agents: `/clear`.

## Optional helpers

`./H20/Extras/` contains convenience prompts and scripts only. They are outside the core H20 contract, may be agent-specific, and can be ignored completely if you prefer the pure copy-paste flow.

### 4-review

Purpose: run an independent review of code, schemas, tests, and logic produced by a completed plan or milestone, then write two immutable artifacts under `./H20/Reviews/`: a human-facing review snapshot and a machine-facing follow-up raw prompt. This helper is non-core by design and does **not** create a second completion state for milestones.

Syntax:

```bash
@H20/Extras/4-review.md @H20/05-my-milestone/
@H20/Extras/4-review.md @H20/05-my-milestone/PLAN-03--api-hardening.md
```

Accepted path styles include both `./H20/05-my-milestone` and `./05-my-milestone`, plus direct `PLAN-NN--*.md` paths.

Behavior:

- With a milestone dir, it reviews the union of files recorded by completed done-files in that milestone.
- With a completed plan file, it reviews that plan's recorded outputs only, while still writing artifacts under the parent milestone's review directory.
- It accepts optional seeded concerns after the target as pasted text and/or referenced files. These are review hints, not scope redefinition.
- It writes the next free immutable pair:
  - `./H20/Reviews/05-my-milestone/REVIEW-01.md`
  - `./H20/Reviews/05-my-milestone/raw-review-prompt-01.md`
- Re-running the review with a different agent creates `REVIEW-02.md` and `raw-review-prompt-02.md`, and so on. Older review artifacts are never overwritten.
- Its first pass is an implementation review of what exists, not a plan-compliance audit. It may consult milestone context later only to classify findings and draft a follow-up scope.
- The generated `raw-review-prompt-NN.md` is intentionally narrower than the full review and is meant for the user to read, trim, and then feed into the normal H20 pipeline via `@H20/1-create-prompt.md`.

### 2a-env-checker

Purpose: scan a milestone or one specific plan file and print a manual checklist of likely environment capabilities worth validating before execution. It does **not** inspect your actual agent runtime, installed MCPs, or plugins; it only infers likely needs from the milestone files already on disk.

Syntax:

```bash
./H20/Extras/2a-env-checker
./H20/Extras/2a-env-checker ./H20/01-my-feature
./H20/Extras/2a-env-checker ./01-my-feature
./H20/Extras/2a-env-checker ./H20/01-my-feature/PLAN-02--ui.md
```

Behavior:

- With no args, it prints its own syntax / help.
- With a milestone dir, it scans unfinished plans in that milestone.
- With a plan file, it scans only that specific plan.
- Output is a color-coded checklist plus evidence lines pulled from the prompt / roadmap / plan files so you can validate the environment manually before you run the executor.

### 3-autoexec-claude

Purpose: Claude Code wrapper that executes the next pending H20 plan(s) for one milestone in a loop using the current user's Claude subscription login. This helper is Claude-specific by design.

Syntax:

```bash
./H20/Extras/3-autoexec-claude --milestone ./H20/01-my-feature [--steps N] [--model sonnet|opus|<full-model>] [--skiphuman] [--no-stream]
```

Accepted milestone path styles include both `./H20/01-my-feature` and `./01-my-feature`.

Examples:

```bash
./H20/Extras/3-autoexec-claude --milestone ./H20/01-my-feature
./H20/Extras/3-autoexec-claude --milestone ./H20/01-my-feature --steps 2
./H20/Extras/3-autoexec-claude --milestone ./H20/01-my-feature --model opus
./H20/Extras/3-autoexec-claude --milestone ./H20/01-my-feature --skiphuman
```

Behavior:

- Streaming output is on by default; `--no-stream` disables it.
- The wrapper defaults Claude Code permissions to `--dangerously-skip-permissions`.
- It appends literal executor overlays: `AUTOEXEC_MODE=1`, plus `AUTOEXEC_SKIP_HUMAN=1` when `--skiphuman` is used.
- `BLOCKED.md` stops the loop immediately.
- If a run returns without creating the expected done-file, the wrapper treats that as a handoff / stop condition instead of blindly continuing.
- Without `--skiphuman`, the loop stops when a human-only verification checkpoint is reached.
- With `--skiphuman`, those human-only checks are forced to `⚠ skipped`, matching the executor overlay semantics documented above.

### 3-autoexec-codex

Purpose: Codex CLI wrapper that executes the next pending H20 plan(s) for one milestone in a loop using the current user's Codex login. This helper is Codex-specific by design.

Syntax:

```bash
./H20/Extras/3-autoexec-codex --milestone ./H20/01-my-feature [--steps N] [--model <model-id>] [--skiphuman]
```

Accepted milestone path styles include both `./H20/01-my-feature` and `./01-my-feature`.
If `--model` is omitted, `3-autoexec-codex` defers to your local Codex CLI default model. The current tested explicit model is `gpt-5.4`.

Examples:

```bash
./H20/Extras/3-autoexec-codex --milestone ./H20/01-my-feature
./H20/Extras/3-autoexec-codex --milestone ./H20/01-my-feature --steps 2
./H20/Extras/3-autoexec-codex --milestone ./H20/01-my-feature --model gpt-5.4
./H20/Extras/3-autoexec-codex --milestone ./H20/01-my-feature --skiphuman
```

Behavior:

- It uses the current user's Codex login (`ChatGPT` or API key).
- It re-runs Codex in a fresh ephemeral session per plan.
- Codex CLI progress output uses its normal defaults.
- The wrapper disables approval prompts with `-a never`.
- The wrapper defaults sandboxing to `--sandbox danger-full-access`.
- The wrapper defaults session persistence to `--ephemeral`.
- The wrapper passes `--skip-git-repo-check` so runs still start when the target repo is outside Codex's trusted-directory list.
- If `--model gpt-5-codex` is passed, the wrapper rewrites it to `gpt-5.4` before launching Codex because ChatGPT-backed Codex CLI rejects the older alias.
- It appends literal executor overlays: `AUTOEXEC_MODE=1`, plus `AUTOEXEC_SKIP_HUMAN=1` when `--skiphuman` is used.
- `BLOCKED.md` stops the loop immediately.
- If a run returns without creating the expected done-file, the wrapper treats that as a handoff / stop condition instead of blindly continuing.
- Without `--skiphuman`, the loop stops when a human-only verification checkpoint is reached.
- With `--skiphuman`, those human-only checks are forced to `⚠ skipped`, matching the executor overlay semantics documented above.
