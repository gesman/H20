# H20 — Lean coding-agent harness

H20 is a small set of markdown prompts and a directory convention for coding agents with filesystem access. It turns a vague idea into a working project through a four-stage flow with fresh context at every boundary:

```text
raw prompt -> TASK.md -> MASTER-PLAN.md -> STEP-NN--<kebab>.md -> execution
```

For copied payloads, the same contract also ships as `./H20/CONTRACT.md` so a project that receives only the `H20/` directory remains self-contained. In this source repo, the root `README.md` remains the authoritative edit target for the contract; keep the payload copy in sync.

Core H20 has no CLI, hooks, runtime, package manager, telemetry, or daemon. Copy the `./H20/` directory into a project and paste the stage prompts into any coding agent that can read and write files. Optional convenience scripts may exist under `./H20/Extras/`, but they are explicitly outside the core contract.

The core prompt files under `./H20/` are agent-only instruction files. User-facing usage guidance, examples, and workflow notes live in this README.

## Super quick start

1. Copy `./H20/` into your project root. Start your favorite coding agent.
2. Clarify the task:
   `@H20/1-clarify-task.md "Build me a website"` or `@H20/1-clarify-task.md @raw-prompt.txt`
   If your agent supports file references, include the `@`. A bare path like `H20/1-clarify-task.md` is just text in many agents and may cause the raw prompt to be executed directly instead of creating milestone artifacts. If file references are unavailable, paste the contents of `1-clarify-task.md` first, then the raw prompt.
3. Generate the master plan:
   `@H20/2-generate-master-plan.md @H20/01-my-feature/`
4. Emit executable steps:
   `@H20/3-emit-steps.md @H20/01-my-feature/`
5. Execute one step per fresh session:
   `@H20/4-execute-step.md @H20/01-my-feature/STEP-01--do-this.md`
6. Repeat step-by-step. Clear context between runs. If execution writes `BLOCKED.md`, stop and either fix the issue, re-emit steps with `@H20/3-emit-steps.md @H20/01-my-feature/ @H20/01-my-feature/BLOCKED.md`, redo the master plan, or start a new milestone with the old `raw-prompt.txt` plus `BLOCKED.md`.
7. Optional: if you use Claude Code or Codex and want a thin loop wrapper around repeated executor runs, use one of:

   `./H20/Extras/4-autoexec-claude --milestone ./H20/01-my-feature --model opus --skiphuman [--steps 2]`

   `./H20/Extras/4-autoexec-codex --milestone ./H20/01-my-feature --model gpt-5.5 --reasoning xhigh --skiphuman [--steps 2]`

   These are non-core convenience scripts, not part of the H20 contract. They repeatedly invoke the next pending step(s), pass `AUTOEXEC_MODE=1`, and stop on dirty git worktrees, `_LOCKED.md`, `BLOCKED.md`, missing done-file creation, unrecoverable partial state, or a human-verification handoff. Add `--skiphuman` only when you want human-only checks recorded as skipped. Add `--dry-run` to preview the resolved milestone and selected steps without launching the agent.

## Why H20

- **Context rot is the silent killer of complex projects, and H20 is built around defeating it.** Big goals die when one bloated session has to hold the whole product in its head. H20 shards work into milestones, then into execution steps, and demands a fresh context window at every stage boundary. Each step carries forward only the immediately prior done-file — a hand-written summary, not a conversation replay.
- **The what and the how are now separate artifacts.** `TASK.md` captures the cleaned, agreed "what". `MASTER-PLAN.md` captures the reviewed per-milestone "how" before any `STEP-NN` files exist. Larger work gets an explicit strategy checkpoint instead of jumping straight from a task brief into many executable files.
- **Pick the right agent for the right step.** The core prompts use no agent-specific syntax, so a single milestone can flow across tools: scaffold the backend in Codex, design the UI in Claude Code, hand a tricky migration to Aider, verify in Cursor. Every handoff is just "paste the executor prompt into a different agent and name the next step file."
- **The harness stays lean.** The completion state machine is still file existence: a step is done iff `STEP-NN--DONE.md` exists. `_LOCKED.md` is a separate hard-stop state marker, not completion. If H20 ever stops being useful to you, `rm -rf H20/` deletes it without trace. Nothing about your project depends on it.

## Design axioms

1. **Coding-agent-agnostic.** The meta-prompts are written for coding agents with filesystem access. No agent-specific syntax ever.
2. **Zero install, zero runtime in the core.** Copy-paste is the install. Optional helpers under `./H20/Extras/` are convenience tooling, not part of the contract.
3. **Self-contained inside `./H20/`.** Every artifact H20 touches — prompts, task briefs, master plans, steps, reviews — lives under `./H20/` of the target project. Nothing spills to the project root.
4. **Numbered milestones track evolution.** `./H20/01-<kebab>/`, `./H20/02-<kebab>/`, … give you a scannable history of what you built and when.
5. **File-existence recovery.** A step is "done" iff its `STEP-NN--DONE.md` exists. No state machinery, no manifest drift.
6. **Shallow dependencies.** Each step references at most the immediately prior done-file. Rich done-file summaries kill spiderweb chains.
7. **Per-milestone planning only.** `MASTER-PLAN.md` is the current milestone's implementation strategy, not a global product roadmap or long-lived state database.

## Flow

```text
raw prompt (verbal, pasted, or referenced source material)
    │
    ▼   paste 1-clarify-task.md + raw prompt into a coding agent
    │
    │   Phase 1 — Research-need judgment
    │     LLM evaluates whether the task needs tech/framework/
    │     platform research before clarification.
    │
    │   Phase 2 — Research offer (conditional)
    │     If useful: print decision axes and ask whether to research.
    │
    │   Phase 3 — Research (conditional on opt-in)
    │     Present compact options and capture decisions.
    │
    │   Phase 4 — Grilling
    │     Ask 3–7 concrete clarification questions, up to 3 rounds.
    │
    │   Phase 5 — Writing
    │     Write:
    │       - raw-prompt.txt (input + research + Q&A transcript)
    │       - TASK.md (clean, structured "what")
    │
    ▼   paste 2-generate-master-plan.md + point at milestone
    │
    │   LLM reads TASK.md and repo context, surfaces material
    │   strategy choices if any, then writes:
    │       - MASTER-PLAN.md (reviewable per-milestone "how")
    │
    ▼   paste 3-emit-steps.md + point at milestone
    │
    │   LLM compiles TASK.md + MASTER-PLAN.md into:
    │       - ROADMAP.md
    │       - STEP-01--<kebab>.md, STEP-02--<kebab>.md, …
    │
    ▼   paste 4-execute-step.md + name one step file
    │
    │   LLM checks STEP-NN--DONE.md; if exists, stops.
    │   Otherwise loads context, executes the step's actions,
    │   uses available tools proactively, adds best-effort tests,
    │   verifies, writes STEP-NN--DONE.md, and commits
    │   if in a git repo.
    │
    ▼   next step reads only the immediately prior done-file
```

## Directory layout

Inside a target project using H20:

```text
./H20/
├── 1-clarify-task.md              (meta-prompt)
├── 2-generate-master-plan.md      (meta-prompt)
├── 3-emit-steps.md                (meta-prompt)
├── 4-execute-step.md              (meta-prompt)
├── Extras/                        (optional convenience prompts and scripts; non-contractual)
│   ├── 1-clarify-task-assume-defaults.md
│   ├── 3a-env-checker
│   ├── 4-autoexec-claude
│   ├── 4-autoexec-codex
│   ├── 5-review.md
│   ├── pullh20
│   ├── README.md
│   └── helpers/
├── RawPrompts/                    (optional raw-source stash; non-contractual)
│   └── 0_placeholder-for-raw-user-prompts.txt
├── Reviews/                       (optional review snapshots; non-contractual)
│   └── 01-<first-milestone>/
│       ├── REVIEW-01.md
│       └── raw-review-prompt-01.md
├── CONTRACT.md
├── 01-<first-milestone>/
│   ├── raw-prompt.txt
│   ├── TASK.md
│   ├── MASTER-PLAN.md
│   ├── ROADMAP.md
│   ├── _LOCKED.md                (optional; locks this milestone against all H20 work)
│   ├── BLOCKED.md                 (optional; only when a blocked execution writes it)
│   ├── STEP-01--<kebab>.md
│   ├── STEP-01--DONE.md           (only after successful execution)
│   ├── STEP-02--<kebab>.md
│   └── STEP-02--DONE.md
├── 02-<second-milestone>/
│   └── …
```

Milestones start at `01`, two-digit zero-padded, kebab-case title. Steps and their done-files live **inline** in the milestone dir — there is NO `steps/`, `plans/`, or `summaries/` subdir.

## File-naming rules

- **Meta-prompts:** `N-<kebab>.md` at `./H20/` root, where `1` = clarify task, `2` = generate master plan, `3` = emit steps, `4` = execute step.
- **Milestones:** `NN-<kebab>/` where NN is `01`..`99`.
- **Raw prompt:** always exactly `raw-prompt.txt`.
- **Task brief:** always exactly `TASK.md`.
- **Master plan:** always exactly `MASTER-PLAN.md`.
- **Roadmap:** always exactly `ROADMAP.md`.
- **Locked milestone marker:** optional milestone-root `_LOCKED.md`. Empty is valid; any contents are optional human context only.
- **Steps:** `STEP-NN--<kebab>.md`, NN `01`..`99`, zero-padded.
- **Done-files:** `STEP-NN--DONE.md` — no title suffix, so existence check is trivial.
- **Blocked handoff:** optional milestone-root `BLOCKED.md`. At most one unresolved blocker file per milestone.
- **Review snapshots:** optional `./H20/Reviews/NN-<kebab>/REVIEW-NN.md`, where the directory name matches the reviewed milestone and the review file number is local to that review directory.
- **Review follow-up prompts:** optional `./H20/Reviews/NN-<kebab>/raw-review-prompt-NN.md`, paired with the review snapshot that produced it.
- **Raw source stash:** optional `./H20/RawPrompts/` for user-managed input files. H20 does not read it automatically; pass files from it explicitly.

## Schemas

### TASK.md schema

- `# Task: <milestone title>`
- `## Goal` — one paragraph, imperative voice.
- `## Context` — tech stack, target runtime, relevant existing code, users. Research-phase decisions land here.
- `## Requirements` — numbered list. Each item is one testable requirement. Preserve execution-critical source literals such as exact commands, config blocks, env vars, ignore patterns, file/path lists, validation queries, rollback steps, and security exclusions, or state the accepted supersession explicitly.
- `## Non-goals` — explicit scope exclusions.
- `## Success criteria` — bulleted, verifiable (command, test, observable behavior, API response, screenshot/DOM check, or equivalent).
- `## Research notes` (optional) — only present if the clarify-task research phase ran. Briefly records each decision axis researched, options considered, and the choice made.
- `## Open questions` (optional) — only present if `1-clarify-task.md` could not get answers despite grilling. Omit entirely when empty.

### MASTER-PLAN.md schema

- `# Master Plan: <milestone title>`
- `## Task source` — path to this milestone's `TASK.md`.
- `## Strategy` — the reviewed per-milestone implementation approach: architecture, data flow, major boundaries, sequencing rationale, exact source literals needed for execution, and key decisions. This is the clean long "how".
- `## Step outline` — ordered list of expected execution steps at the outcome level. These are not yet `STEP-NN` files, but they should be specific enough for `3-emit-steps.md` to compile mechanically.
- `## Requirement coverage` — table with columns: `Requirement | Covered by | Notes`.
- `## Success coverage` — table with columns: `Success criterion | Verification approach | Notes`.
- `## Risks and mitigations` — concrete implementation risks, assumptions, and how steps should reduce or verify them.
- `## Out of scope` — boundaries inherited from `TASK.md` plus any planning-specific exclusions.
- `## Planner notes` (optional) — unresolved planning gaps that do not invalidate the task but should be visible before step emission.

### ROADMAP.md schema

- `# Roadmap: <milestone title>`
- `## Steps` — table with columns: `# | File | Goal | Depends on`.
- `## Execution order` — linear list of step filenames in execution order. Mention parallelism only if steps are truly independent; default is sequential.
- `## Emitter notes` (optional) — gaps surfaced during step emission that `TASK.md` or `MASTER-PLAN.md` did not address. Omit if empty.

### STEP-NN--<kebab>.md schema

- `# Step NN: <title>`
- `## Prerequisite` — either `none` or a single line naming the immediately prior done-file, e.g. `./H20/01-my-feature/STEP-01--DONE.md`. H20 enforces **at most one prerequisite per step**.
- `## Goal` — one paragraph; what this execution step achieves end-to-end.
- `## Actions` — numbered list; each action small, specific, and verifiable.
- `## Deliverables` — files created or modified, with relative paths.
- `## Verification` — concrete commands/checks the executor must run. Prefer agent-runnable checks: commands, automated flows, API calls, screenshots, DOM checks, logs, or equivalent objective checks. Mark verification human-only only when no reasonable agent-side tool or fallback can judge it, and state that reason.
- `## Done signal` — literal: "On full verification pass, write `STEP-NN--DONE.md` in this directory per the README done-file schema, then commit if in a git repo."

### STEP-NN--DONE.md schema

- `# STEP-NN DONE: <title>`
- `## Summary` — 3–6 bullets: what was built, key decisions, capability-use outcome (`used`, `best-effort fallback`, `blocked`, or `not needed`), tests added or not applicable, and human-verification outcome when applicable.
- `## Files changed` — bullet list of paths (including any executor-added test files).
- `## Verification results` — one line per verification check: `✅`, `❌`, or `⚠ skipped`, plus the command/check.
- `## Gotchas for next step` — anything the next step needs to know: APIs added, signatures differing from step assumptions, env vars required, known limitations, test-file locations and fixtures. Write full sentences so a fresh-context agent can absorb it without reading upstream code.
- `## Commit` — if in a git repo, record `same commit as this done-file — subject: step-NN: <title>`; otherwise `not a git repo — no commit`. The executor's final handoff should print the actual SHA separately because a tracked file cannot contain its own final commit ID without changing that ID.

### BLOCKED.md schema

- `# BLOCKED: STEP-NN <title>` — names the incomplete step that hit the blocker.
- `## What happened` — one paragraph: what stopped execution and why the current step could not safely continue.
- `## Evidence` — bullet list of concrete observations: commands, errors, file paths, API responses, or contradictions in the codebase / environment.
- `## Earliest safe recovery point` — one of `resume current step`, `re-emit steps from current step`, `redo master plan`, `redo task`, or `start new milestone`, followed by one-sentence reasoning. The executor must never point recovery at a later step while the current step has no done-file.
- `## Workspace state` — bullets covering files already touched, what is safe to keep, what is safe to discard, and any verification already run.
- `## Suggested user actions` — 2 or 3 labeled options (`A.`, `B.`, optional `C.`), with exactly one marked recommended. Each option names the exact next move: edit, emit-step invocation, master-plan invocation, clarify-task invocation, or external action.

### Optional review artifacts

These artifacts are produced only by non-core helpers such as `./H20/Extras/5-review.md`. They live under `./H20/Reviews/` and do **not** change milestone completion semantics, done-file recovery, or executor behavior.

Done-files may define review scope, but they are not correctness evidence. Review findings and clearances must be backed by inspected artifacts, concrete recorded verification, or fresh read-only checks when available.

### REVIEW-NN.md schema

- `# Review NN: <reviewed milestone title>`
- `## Reviewed scope` — the reviewed milestone path, whether the run covered the whole milestone or a specific completed step, and any explicit exclusions.
- `## Review basis` — review run date, reviewer / agent label if known, done-files used to derive scope, and files actually inspected.
- `## Seeded concerns` (optional) — concerns injected by the user as pasted text and/or referenced files. Each entry records the original concern, its source, the outcome (`confirmed`, `disproved`, `not applicable`, or `inconclusive`), and one-sentence reasoning.
- `## Independent findings` — numbered list, ordered by severity. Each finding includes: severity, issue, evidence, affected files or interfaces, and recommended disposition (`carry forward`, `defer`, `cross-cutting`, or `acceptable tradeoff pending user confirmation`).
- `## Deferred or acceptable tradeoffs` (optional) — items the reviewer believes may be acceptable for now but should be explicit.
- `## Cross-cutting or unrelated observations` (optional) — important observations that do not cleanly belong in the next milestone derived from this review.
- `## Recommended follow-up milestones` — 1 to 3 concrete next-milestone options, with exactly one recommended.

### raw-review-prompt-NN.md schema

- `# Raw review prompt NN: <proposed follow-up title>`
- `## Source review` — path to the paired `REVIEW-NN.md` and one sentence describing the review scope.
- `## Goal` — one paragraph describing the follow-up milestone to create.
- `## Findings included` — numbered list of the review findings intentionally carried into this follow-up scope.
- `## Findings explicitly excluded` — numbered or bulleted list of reviewed findings intentionally left out, deferred, or treated as unrelated.
- `## Constraints` — explicit scope fences, assumptions, and boundaries for the next milestone.
- `## Success criteria` — bulleted, verifiable outcomes expected from the follow-up milestone.

## Locked milestones

A milestone-root `_LOCKED.md` is a state marker. Its presence means the milestone is inactive, incomplete, no longer needs H20 work, and must be ignored by H20 agents. The file may be empty. Any text inside is optional human context and is not part of the contract schema.

If `_LOCKED.md` exists, every H20 stage and helper must hard-stop before reading or modifying any other artifact in that milestone. The only allowed read is `_LOCKED.md` itself, solely to report a brief message. `_LOCKED.md` is not a completion marker, does not satisfy prerequisites, is not recoverable blocker context, and takes precedence over `BLOCKED.md`, done-files, review requests, autoexec flags, and any other intent. To unlock a milestone, delete `_LOCKED.md` manually.

## Recovery rule

After confirming the milestone is not locked, before executing `STEP-NN--<kebab>.md`, check if the sibling `STEP-NN--DONE.md` exists in the same milestone directory. If yes, stop and report `STEP-NN already executed`. If no, execute. To re-run a step, **delete its done-file** manually. That is the entire recovery mechanism. `BLOCKED.md` never marks a step complete and does not alter the done-file recovery rule; it is only a user-directed handoff artifact.

## Interrupted runs

H20 auto-recovers **completed** steps via done-files. It also attempts graceful recovery for interrupted partial runs. If a coding agent crashed before writing `STEP-NN--DONE.md`, the next executor run should check for workspace drift using git status, relevant diffs, declared deliverables, and file contents. Mere existence of a deliverable path is not partial state when the step is expected to modify an existing file.

If the partial state is coherent and in scope, the executor should state the recovery assumption, resume from the current state, run fresh verification, and write `STEP-NN--DONE.md` only on full pass. If recovery is ambiguous, unrelated, or unsafe, the executor should write milestone-root `BLOCKED.md` with current status, concrete evidence, block reasons, and 2 or 3 recovery options with exactly one recommended option when possible.

## Blocked runs

If execution hits a durable blocker that makes the current step unsafe to complete, the executor should write milestone-root `BLOCKED.md` and stop without writing a done-file or making a commit. Durable blockers include invalidated step assumptions with no safe in-scope repair, missing external access or credentials, failed or unavailable capabilities or facilities with no safe fallback, or external constraints that change the implementation path.

Do **not** use `BLOCKED.md` for ordinary clarifying chat, interactive dirty-worktree checks, safely recoverable partial-run detection, or planned human-only verification pauses already covered elsewhere in the executor flow. In unattended `AUTOEXEC_MODE=1`, write `BLOCKED.md` when unrelated dirty files or ambiguous partial state require a human recovery choice.

`BLOCKED.md` is consumed only when the user explicitly passes it into `3-emit-steps.md`, `2-generate-master-plan.md`, or `1-clarify-task.md`. Its presence on disk alone does not auto-replan anything.

After the user chooses a recovery path and materializes it, delete `BLOCKED.md`. If the milestone is abandoned entirely, create `_LOCKED.md`; keeping `BLOCKED.md` as extra context is fine, but `_LOCKED.md` is the state marker.

## Optional executor overlays

Optional convenience wrappers may append literal control lines after the step path in executor input:

- `AUTOEXEC_MODE=1` — executor capability assessment must use any already-available capabilities without pausing; if a required capability is missing or failing and no safe fallback exists, the executor should write `BLOCKED.md` and stop.
- `AUTOEXEC_SKIP_HUMAN=1` — human-only verification may be recorded as `⚠ skipped` after the executor performs all automatable setup. Without this explicit marker, human-only verification still pauses for user input even in autoexec mode.

These overlays do **not** change the `_LOCKED.md` hard stop, done-file recovery rule, partial-run recovery assessment, blocker semantics, or milestone schemas.

## Using H20 on a project

1. Copy `./H20/` into your project root. Files are ordered by name (`1-…`, `2-…`, `3-…`, `4-…`) so `ls ./H20/` shows the pipeline left to right.
2. Gather raw source material. This can be one file, many files, a directory, pasted text, or any combination.
3. Paste `1-clarify-task.md` into a coding agent, then your raw input corpus. The agent may recommend a tech/framework research phase, then it grills you. You get `raw-prompt.txt` and `TASK.md`.
   Shortcuts for coding agents that support file references:
   `@H20/1-clarify-task.md @idea-notes.txt`
   `@H20/1-clarify-task.md @raw-prompt1.txt @raw-prompt2.txt`
   `@H20/1-clarify-task.md @raw-prompts/`
   If a blocked milestone needs a fresh task pass, include the previous raw prompt plus `BLOCKED.md`:
   `@H20/1-clarify-task.md @H20/01-my-feature/raw-prompt.txt @H20/01-my-feature/BLOCKED.md`
   Recommended after success: clear or reset context before stage 2. In most coding agents: `/clear`.
4. Paste `2-generate-master-plan.md` into a coding agent and point it at the milestone dir or `TASK.md`. The agent reads repo-local instruction files if present, uses same-milestone `raw-prompt.txt` only as a source-fidelity reference for already-agreed scope, surfaces material strategy choices, and writes `MASTER-PLAN.md`.
   Shortcuts:
   `@H20/2-generate-master-plan.md @H20/01-my-feature/`
   `@H20/2-generate-master-plan.md @H20/01-my-feature/TASK.md`
   If a blocked execution invalidated strategy, pass `BLOCKED.md` explicitly:
   `@H20/2-generate-master-plan.md @H20/01-my-feature/ @H20/01-my-feature/BLOCKED.md`
   Recommended after success: clear or reset context before stage 3.
5. Paste `3-emit-steps.md` into a coding agent and point it at the milestone dir. The agent compiles `TASK.md` and `MASTER-PLAN.md` into `ROADMAP.md` and `STEP-NN--<kebab>.md` files, preserving exact execution-critical literals rather than relying on source memory.
   Shortcuts:
   `@H20/3-emit-steps.md @H20/01-my-feature/`
   If re-emitting after a blocked execution, pass `BLOCKED.md` explicitly so the emitter can rewrite the tail from the correct recovery point:
   `@H20/3-emit-steps.md @H20/01-my-feature/ @H20/01-my-feature/BLOCKED.md`
   Recommended after success: clear or reset context before stage 4.
6. For each step, paste `4-execute-step.md` into a coding agent and name the step file. The executor reads repo-local instruction files if present, uses already-available capabilities proactively, adds best-effort smoke tests for any code it produces, verifies, writes the done-file, and commits locally if in a git repo.
   Shortcut:
   `@H20/4-execute-step.md @H20/01-my-feature/STEP-01--build-api.md`
   Recommended after each successful step: clear or reset context before executing the next step.

## Optional helpers

`./H20/Extras/` contains convenience prompts and scripts only. They are outside the core H20 contract, may be agent-specific, and can be ignored completely if you prefer the pure copy-paste flow.

### 1-clarify-task-assume-defaults

Purpose: non-core fast path for small, local, low-ambiguity tasks where conservative defaults are safer than an interactive research / grilling round. It writes normal milestone artifacts: `raw-prompt.txt` and `TASK.md`.

Example:

```text
@H20/Extras/1-clarify-task-assume-defaults.md "Make background of all pages under /Settings be #123456"
```

### 3a-env-checker

Purpose: scan a milestone or one specific step file and print a manual checklist of likely environment capabilities worth validating before execution. It does **not** inspect your actual agent runtime, installed MCPs, or plugins.

If the target milestone contains `_LOCKED.md`, the checker stops without scanning milestone files.

Syntax:

```bash
./H20/Extras/3a-env-checker
./H20/Extras/3a-env-checker ./H20/01-my-feature
./H20/Extras/3a-env-checker ./01-my-feature
./H20/Extras/3a-env-checker ./H20/01-my-feature/STEP-02--ui.md
```

### 4-autoexec-claude

Purpose: Claude Code wrapper that executes the next pending H20 step(s) for one milestone in a loop using the current user's Claude subscription login.

If the milestone contains `_LOCKED.md`, the wrapper stops before dry-run or live execution.

Syntax:

```bash
./H20/Extras/4-autoexec-claude --milestone ./H20/01-my-feature [--steps N] [--model sonnet|opus|<full-model>] [--skiphuman] [--no-stream] [--dry-run]
```

### 4-autoexec-codex

Purpose: Codex CLI wrapper that executes the next pending H20 step(s) for one milestone in a loop using the current user's Codex login.

If the milestone contains `_LOCKED.md`, the wrapper stops before dry-run or live execution.

Syntax:

```bash
./H20/Extras/4-autoexec-codex --milestone ./H20/01-my-feature [--steps N] [--model <model-id>] [--reasoning minimal|low|medium|high|xhigh] [--skiphuman] [--dry-run]
```

### 5-review

Purpose: run an independent review of code, schemas, tests, and logic produced by a completed step or milestone, then write two immutable artifacts under `./H20/Reviews/`: a human-facing review snapshot and a machine-facing follow-up raw prompt. This helper is non-core by design and does **not** create a second completion state for milestones.

If the reviewed milestone contains `_LOCKED.md`, review stops before reading milestone artifacts or seeded concerns.

Syntax:

```text
@H20/Extras/5-review.md @H20/05-my-milestone/
@H20/Extras/5-review.md @H20/05-my-milestone/STEP-03--api-hardening.md
```

Accepted path styles include both `./H20/05-my-milestone` and `./05-my-milestone`, plus direct `STEP-NN--*.md` paths.

The generated `raw-review-prompt-NN.md` is intentionally narrower than the full review and is meant for the user to read, trim, and then feed into the normal H20 pipeline via `@H20/1-clarify-task.md`.

### pullh20

Purpose: update a project's copied `./H20/` payload from this source repo while preserving local milestone directories, `RawPrompts/`, and `Reviews/`.

Syntax:

```bash
./H20/Extras/pullh20 [source-dir]
PULLH20_SOURCE_DIR=/path/to/H20/H20 ./H20/Extras/pullh20
```

Run it from the target project root. It is a convenience sync helper, not part of the H20 contract.
