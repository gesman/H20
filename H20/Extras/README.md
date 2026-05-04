# Extras

Optional convenience prompts and scripts live here. They are **not** part of H20's core milestone state machine, do not change done-file recovery or completion semantics, and can be ignored entirely.

Current extras:

- `1-clarify-task-assume-defaults.md` — non-core fast-path task writer for small, local, low-ambiguity tasks where the user wants a master-plan-ready `TASK.md` without an interactive research / grilling round.
- `3a-env-checker` — scans either a milestone's unfinished steps or one specific step file and prints a manual checklist of likely environment capabilities to validate before execution.
- `4-autoexec-claude` — Claude Code wrapper that executes the next pending step(s) for a milestone in a loop using the current user's Claude subscription.
- `4-autoexec-codex` — Codex CLI wrapper that executes the next pending step(s) for a milestone in a loop using the current user's Codex login.
- `5-review.md` — review-stage prompt that writes immutable review snapshots and follow-up raw prompts under `./H20/Reviews/<milestone>/`.

Notes:

- `1-clarify-task-assume-defaults.md` is still agent-agnostic, but it is intentionally a convenience shortcut rather than part of core H20. It writes normal milestone artifacts and may refuse broad or ambiguous requests.
- `4-autoexec-claude` is Claude-specific by design. It is a user convenience, not part of the core H20 payload.
- `4-autoexec-codex` is Codex-specific by design. It is a user convenience, not part of the core H20 payload.
- `5-review.md` is agent-agnostic in wording, but it is intentionally non-core. It does not modify milestone state and only writes review artifacts under `./H20/Reviews/`.
- Autoexec runs pass literal control lines into `4-execute-step.md`:
  - `AUTOEXEC_MODE=1`
  - `AUTOEXEC_SKIP_HUMAN=1` when `--skiphuman` is used
- Autoexec still honors H20 recovery semantics. `BLOCKED.md` stops the loop. Missing done-file creation after a run is treated as a handoff / stop condition.
- Autoexec `--dry-run` prints the resolved milestone and selected pending steps without launching the agent or writing files.

`1-clarify-task-assume-defaults.md` usage:

- file-reference example:
  - `@H20/Extras/1-clarify-task-assume-defaults.md "Make background of all pages under /Settings be #123456"`
- also works with referenced source files:
  - `@H20/Extras/1-clarify-task-assume-defaults.md @raw-prompt.txt`
- do not use a bare path like `H20/Extras/1-clarify-task-assume-defaults.md` and expect the agent to load it; use `@...` or paste the file contents
- accepted use case: small local changes where conservative defaults are safe
- refusal cases: broad features, architecture choices, integrations, migrations, or anything that would need real clarification
- output: normal milestone artifacts under `./H20/NN-<kebab>/`, including `raw-prompt.txt` and schema-conforming `TASK.md`

`3a-env-checker` usage:

- no args: prints color-coded syntax help
- `3a-env-checker <milestone-dir>`: scans unfinished steps inside that milestone
- `3a-env-checker <step-file>`: scans that specific step file
- accepted path styles include `./H20/01-my-feature`, `./01-my-feature`, and direct `STEP-NN--*.md` paths

`5-review.md` usage:

- file-reference example:
  - `@H20/Extras/5-review.md @H20/05-my-milestone/`
- also works against one completed step:
  - `@H20/Extras/5-review.md @H20/05-my-milestone/STEP-03--api-hardening.md`
- also accepts optional seeded concerns after the target:
  - `@H20/Extras/5-review.md @H20/05-my-milestone/ "Also inspect whether /config.yaml could be world-accessible."`
  - `@H20/Extras/5-review.md @H20/05-my-milestone/ @other-concerns.txt`
- do not use a bare path like `H20/Extras/5-review.md` and expect the agent to load it; use `@...` or paste the file contents
- accepted use case: independent review of completed milestone outputs or one completed step's outputs
- done-files define review scope, but findings and clearances must come from inspected artifacts, concrete recorded verification, or fresh read-only checks when available
- seeded concerns are review hints only; they do not redefine review scope
- output: immutable review artifact pairs under `./H20/Reviews/<milestone>/`, such as `REVIEW-01.md` and `raw-review-prompt-01.md`
- repeated runs by different agents create `REVIEW-02.md`, `raw-review-prompt-02.md`, and so on; earlier review artifacts are never overwritten

`4-autoexec-claude` usage:

- no args: prints color-coded syntax help
- `4-autoexec-claude --milestone <milestone-dir>`: loops Claude Code over pending steps inside that milestone
- accepted path styles include `./H20/01-my-feature` and `./01-my-feature`
- optional flags:
  - `--steps N`: stop after N steps
  - `--model sonnet|opus|<full-model>`: override the Claude Code model; default is `opus`
  - `--skiphuman`: pass `AUTOEXEC_SKIP_HUMAN=1` so human-only checks are recorded as skipped
  - `--no-stream`: use plain Claude Code text output instead of the stream formatter
  - `--dry-run`: print the resolved milestone and selected pending steps without launching Claude or writing files

`4-autoexec-codex` usage:

- no args: prints color-coded syntax help
- `4-autoexec-codex --milestone <milestone-dir>`: loops Codex over pending steps inside that milestone
- accepted path styles include `./H20/01-my-feature` and `./01-my-feature`
- optional flags:
  - `--steps N`: stop after N steps
  - `--model <model-id>`: override the Codex CLI default model for this run; the current tested explicit model is `gpt-5.5`
  - `--reasoning minimal|low|medium|high|xhigh`: override the Codex CLI default reasoning effort for this run
  - `--skiphuman`: pass `AUTOEXEC_SKIP_HUMAN=1` so human-only checks are recorded as skipped
  - `--dry-run`: print the resolved milestone and selected pending steps without launching Codex or writing files
- Codex runs use `-a never`, optional `-c model_reasoning_effort=<level>`, `--sandbox danger-full-access`, `--ephemeral`, and `--skip-git-repo-check`
- If `--model gpt-5-codex` is passed, the wrapper rewrites it to `gpt-5.5` before launching Codex because ChatGPT-backed Codex CLI rejects the older alias.
