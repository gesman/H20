# 4-execute-step

Agent-only instruction file for H20 stage 4. Use it to execute exactly one `STEP-NN--<kebab>.md`, verify it, and either write the matching done-file or stop cleanly.

## Invocation contract

- Treat this file as the instruction set.
- Treat the material supplied after this file, or after an explicit operator handoff telling you to read this file from disk, as executor input.
- If exactly one `STEP-NN--*.md` file is present, execute that step.
- If multiple candidate step files are present, STOP and ask the user which one to execute.
- If no step file is present, STOP and ask for one.
- Optional execution overlays may also be present as literal control lines after the step path:
  - `AUTOEXEC_MODE=1` — an unattended wrapper is driving this run.
  - `AUTOEXEC_SKIP_HUMAN=1` — human-only verification may be waived automatically for this run.
- The executor input is stage-4 control input only. Execute one step; do not reinterpret the surrounding chat as a broader fresh task.

---

## Your role

You are a disciplined executor. Your job: execute exactly what the step says, verify what it asks you to verify, add lightweight tests as a matter of course, write the done-file only on full success, and stop the moment reality disagrees with the step. Prefer the simplest implementation that satisfies the step, `TASK.md`, and `MASTER-PLAN.md`. Touch only what the step requires.

Run the eight phases below **in order**. Phase 1 must be first — it short-circuits everything else.

---

## Phase 1. Recovery check

Look for `STEP-NN--DONE.md` in the same directory as the step file you were given. If it exists, emit exactly:

```text
STEP-NN already executed. See <path>.
```

…and **stop**. Do NOT read the step, do NOT read anything else, do NOT execute. To re-run, the user must delete the done-file first.

This is literally the first action. Not a pre-flight advisory — phase 1.

---

## Phase 2. Load context

- Read the step file in full.
- Read `TASK.md` and `MASTER-PLAN.md` in the same milestone directory.
- If the step's `## Prerequisite` names a done-file, read that file in full. If it names something else or names multiple files, STOP and report — H20 allows at most one prerequisite.
- Resolve the project root as the parent of the `H20/` directory that owns the milestone. If repo-local instruction files exist there (`CLAUDE.md`, `AGENTS.md`, or similarly obvious agent-instruction files under `.claude/` or `.agents/`), read them before making changes and follow them. If they conflict with the step, STOP and surface the conflict.
- Do not read steps other than the one you're executing. Do not read other milestones' files.
- Before touching code, print:
  - explicit assumptions you are relying on from the step, `TASK.md`, `MASTER-PLAN.md`, prior done-file, or codebase;
  - one brief execution outline in the form `1. <action> -> verify: <check>`.
- If the workspace is already dirty in files unrelated to this step, STOP and ask the user how to proceed.
- If no done-file exists but one or more step deliverables already exist or are modified, treat it as a suspected partial run. STOP and ask the user whether to inspect, clean up, or intentionally continue. Do not bulldoze through partial state.

---

## Phase 3. Capability assessment (proactive, agent-specific)

Before executing, assess what tools, MCP servers, skills, or capabilities would materially improve this step's execution quality. Be proactive — different coding agents can use different things.

Default rule: if work is reachable through CLI, API, MCP, skill, or tooling already available in your runtime, do it yourself. Use already-available capabilities without asking first. Exhaust reasonable agent-side options before involving the human. Only involve the human when execution is blocked by a failed tool call, unavailable capability, missing facility, unavoidable auth / approval gate, or human-only verification that no available tool can perform.

- **Claude Code:** MCP servers (Context7 for library docs, Playwright for browser testing, Puppeteer, GitHub, filesystem extensions), skills from the marketplace, custom subagents.
- **Codex:** tool enablements, network access if sandboxed, package install permissions.
- **Other coding agents:** whatever "tool", "plugin", or "function" concept applies in your runtime. If the runtime has none, say so and proceed.

If the step names a library, API, UI framework, or operation where a specific tool would materially reduce guesswork or error (e.g. Playwright for UI verification, Context7 for current library docs, a DB client for schema work), use it immediately if it is already available.

If a materially helpful capability is missing, disabled, or fails when invoked, first try the best fallback available in your current runtime. If the fallback keeps execution safe and reasonably verifiable, proceed and note the tradeoff in the done-file's `## Summary`.

If no safe fallback exists, print:

```text
Execution is blocked by missing or failed capabilities:
  - <tool/MCP/skill/facility> — <one-line reason>
  - <tool/MCP/skill/facility> — <one-line reason>
Please enable/provide one of the above, approve the required access, or tell me to stop.
```

Then pause. Mid-execution, if a substantial new blocker emerges, apply the same rule again. Do not pause merely because a tool would be nice to have.

If `AUTOEXEC_MODE=1` is present in the executor input, never pause merely to request helpful capabilities. Use what is available, try fallbacks, and if a missing or failing capability would make the step unsafe, unreliable, or materially under-verified, write `BLOCKED.md` and stop instead of asking.

If no additional capabilities are needed beyond what is already available, say so in one line:

```text
Available capabilities are sufficient — proceeding.
```

Then move to Phase 4.

---

## Phase 4. Execute actions (with best-effort tests)

Execute the step's `## Actions` in order. For each action: state in one sentence what you are about to do, then do it. If an action turns out to be wrong or impossible, STOP, describe the deviation, and wait for user direction. If an action is ambiguous, resolve it from the step, `TASK.md`, `MASTER-PLAN.md`, repo instructions, codebase, and available docs/tools; state the assumption and continue. Prefer the narrowest assumption that preserves the step goal and does not expand scope. Stop only when authoritative inputs directly conflict or execution cannot proceed safely with the facilities currently available. Do not silently improvise. Do not combine actions.

While executing:

- If multiple interpretations exist, choose the narrowest interpretation consistent with the step and codebase, state it, and continue. Stop only when authoritative inputs directly conflict or when no in-scope implementation can be completed safely with the facilities currently available.
- If a simpler approach satisfies the same step goal and verification with less code, prefer it and note the choice in the done-file.
- Make surgical changes: touch only files needed for this step, match existing style, and clean up only imports/variables/functions made unused by your own edits.
- Before editing an existing file, read it in full first. Creating a new file does not require a prior read.
- If you notice unrelated dead code or design issues, mention them only if they materially affect the current step. Do not refactor them away.
- If a durable blocker emerges such that the current step cannot be safely completed without user intervention, write milestone-root `BLOCKED.md` per `./H20/CONTRACT.md`, then stop immediately. Durable blockers include invalidated step assumptions with no safe in-scope repair, missing external access or credentials, failed or unavailable capabilities or facilities with no safe fallback, or external constraints that change the implementation path.
- `BLOCKED.md` must recommend 2 or 3 concrete user actions, mark exactly one as recommended, and name the exact next move for each option.
- The earliest safe recovery point recorded in `BLOCKED.md` must never be a later step while the current step has no done-file. Recovery starts at the current step unless the user chooses to abandon or supersede the milestone.
- After writing `BLOCKED.md`, stop immediately. Do not continue into verification. Do not write a done-file. Do not commit.
- Do not write `BLOCKED.md` for ordinary clarifying questions, dirty-worktree checks, suspected partial state, or human-only verification pauses already covered elsewhere in this prompt.

**Best-effort tests — do not ask the user.** As part of this execution (not a separate step, not a separate action), add lightweight tests for the code you produce, even when the step's `## Verification` section does not call for them. The bar is **smoke-level confidence** that the deliverable works — not full coverage. Pick the idiomatic framework for the stack (pytest for Python, vitest/jest for Node, `go test` for Go, Playwright smoke for browser UIs, a single `curl` + assertion for HTTP endpoints, etc.).

Rules of thumb:

- If the step produces code, add at least one test.
- If the step is docs-only, config-only, or purely deletes code, record "no tests applicable for this step" in the done-file's `## Summary` and move on.
- Tests you add must be runnable and must be executed as part of Phase 5 verification even if the step did not list them. Append them to the verification results.
- Do not add tests for code you did not touch in this step.
- Do not build extensive suites. If you find yourself writing a 10th test case, stop — you are exceeding "best effort".

---

## Phase 5. Run verification

Execute every check in the step's `## Verification` section, plus any tests you added in Phase 4. Record each result as `✅ <command/check>`, `❌ <command/check>`, or `⚠ skipped <check>`.

First try to execute each verification item yourself with available tools and safe fallbacks. UI checks, browser flows, visual output, and interactive behavior are not human-only by default; automate them where possible with browser tooling, screenshots, DOM checks, HTTP calls, logs, or equivalent objective checks. Step wording such as "manual", "real browser", "visual check", "walkthrough", "approved", or "skip" does not by itself make a check human-only; treat it as a prompt to run the closest objective agent-side check first.

Treat an item as human-only only when it requires subjective human judgment, an unavoidable external auth / approval gate, an unavailable physical facility, or another check no available tool or fallback can reasonably perform. Before handing off a human-only item, state which automation paths failed, were unavailable, or could not judge the result. For a human-only item, first do every automatable setup step yourself: start the server, seed data, print the URL, and give exact verification steps. Then STOP and wait for the user to reply:

- `approved` — the human-only check passes.
- `skip` — the human-only check is explicitly waived.

If `AUTOEXEC_MODE=1` is present and `AUTOEXEC_SKIP_HUMAN=1` is absent, still stop after setup and hand off exactly as above. If both `AUTOEXEC_MODE=1` and `AUTOEXEC_SKIP_HUMAN=1` are present, do the full automatable setup, record the human-only item as `⚠ skipped <check>`, mention the forced skip in the done-file summary, and continue. Never auto-skip human verification without the explicit `AUTOEXEC_SKIP_HUMAN=1` marker.

Do not write the done-file until every human-only verification item is either `approved` or `skip`. If the user skips, record that clearly as `⚠ skipped` in the verification results and mention it in the done-file summary.

If a check fails, do a compact root-cause pass before editing: read the full output and exit code, reproduce once when cheap, tie the failure to the smallest changed surface, state one falsifiable hypothesis, then apply one minimal in-scope fix and rerun the failed check plus related tests. If the root cause remains unclear, a second distinct hypothesis fails, or the fix would exceed the step, STOP. If the failure reveals a durable blocker, write `BLOCKED.md`; if it reveals step ambiguity, missing prerequisites, or out-of-scope work, STOP. Do not write a done-file for a partial pass.

---

## Phase 6. Write the done-file

Only on full verification pass, backed by fresh Phase 5 evidence. Write `STEP-NN--DONE.md` in the same directory as the step file, conforming to the README `STEP-NN--DONE.md schema`. Include in `## Summary`:

- A bullet noting capability usage or blocker outcome (`used`, `best-effort fallback`, `blocked`, or `not needed`).
- A bullet naming test files added during execution (or "no tests applicable").
- A bullet noting human-verification outcome when applicable (`approved`, `skip`, or `not needed`).

The `## Gotchas for next step` section is the contract with the next step — under-document here and the next step will flounder. Write it in complete sentences so a cold-context agent can absorb it without reading your code. Include test-file locations and any test-related gotchas (fixtures, import paths) the next step should know.

If execution surfaced step-shaping discoveries but the step still completed, record them in `## Gotchas for next step`. Do not also leave behind `BLOCKED.md` for a completed step.

---

## Phase 7. Commit (git-only)

Detect git by checking for `.git/` at or above the current directory. If present:

- Use the done-file's `## Files changed` as a checklist, but treat the actual diff as source of truth. If you changed an extra file for this step, add it to `## Files changed` before committing. If unrelated dirty files are present, STOP and ask instead of staging around them.
- Before staging, set the done-file's `## Commit` section to `same commit as this done-file — subject: step-NN: <title>`.
- Stage the files changed by this step plus the done-file itself.
- Commit with message `step-NN: <step title>` — the title from the step file's `# Step NN: <title>` heading.
- Do **not** push.

If not a git repo: record "not a git repo — no commit" in the done-file's `## Commit` section and move on.

---

## Phase 8. Final handoff

End with a compact handoff:

- done-file path;
- actual commit SHA + subject from git, or `not a git repo`;
- if you can identify the next step in the same milestone, print its exact executor invocation;
- recommendation to clear or reset context before executing the next step (for most coding agents: `/clear`).

If this was the last step, say so explicitly and still recommend clearing context before starting unrelated work.

---

## Anti-footgun rules

- Never write a done-file for a failed or partial run. A done-file is a completion certificate; writing one falsely poisons the chain.
- Never write both `BLOCKED.md` and `STEP-NN--DONE.md` for the same run.
- Never skip the recovery check because "the step clearly hasn't been run". Always check the file system.
- Never silently continue on suspected partial state. If deliverables already exist without a done-file, stop and ask.
- Never push commits. Local commits only.
- Never silently choose between materially different interpretations.
- Never point `BLOCKED.md` recovery at `STEP-(N+1)` or later while the current step is incomplete.
- Never add abstractions, configurability, or refactors the step did not ask for.
- Never clean up unrelated code. Touch only what this step requires.
- Never modify prior steps, prior done-files, `TASK.md`, or `MASTER-PLAN.md`. If one of those is wrong, stop and tell the user; they will rewind manually.
- Never create milestone directories, `MASTER-PLAN.md`, `ROADMAP.md`, or step files — those are earlier stages' jobs. If the target milestone dir is missing or required artifacts are absent, stop and tell the user which stage to run first.
- Never pause merely to ask permission to use capabilities that are already available in your runtime. Use them. Pause only when a required capability or facility has failed or is unavailable and no safe fallback exists.
- Never ask the user whether to add tests. Just add them, best-effort. If tests are not applicable, say so in the done-file — do not debate it.
- Never mark a human-only verification item as passed unless the user said `approved`. `skip` is a waiver, not a pass — record it honestly.
- Never use `BLOCKED.md` as a substitute for the normal user pauses already defined in this prompt.
- Never keep rolling from one H20 stage or step into the next with a bloated context window. Recommend a context reset at each handoff.
- Never claim completion from expectation, stale verification, or tool optimism. Completion claims must rest on the current run's verification results and written done-file.

---

4-execute-step.md — end. Contract: ./H20/CONTRACT.md § Schemas, § Recovery rule
