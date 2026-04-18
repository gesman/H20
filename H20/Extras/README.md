# Extras

Optional convenience prompts and scripts live here. They are **not** part of H20's core contract, do not change the contract schemas in `./H20/CONTRACT.md`, and can be ignored entirely.

Current extras:

- `1-create-prompt-assume-defaults.md` — non-core fast-path prompt writer for small, local, low-ambiguity tasks where the user wants a planner-ready `good-prompt.md` without an interactive research / grilling round.
- `2a-env-checker` — scans either a milestone's unfinished plans or one specific plan file and prints a manual checklist of likely environment capabilities to validate before execution.
- `3-autoexec-claude` — Claude Code wrapper that executes the next pending plan(s) for a milestone in a loop using the current user's Claude subscription.
- `3-autoexec-codex` — Codex CLI wrapper that executes the next pending plan(s) for a milestone in a loop using the current user's Codex login.

Notes:

- `1-create-prompt-assume-defaults.md` is still agent-agnostic, but it is intentionally a convenience shortcut rather than part of core H20. It writes normal milestone artifacts and may refuse broad or ambiguous requests.
- `3-autoexec-claude` is Claude-specific by design. It is a user conveniencer, not part of the core H20 payload.
- `3-autoexec-codex` is Codex-specific by design. It is a user conveniencer, not part of the core H20 payload.
- Autoexec runs pass literal control lines into `3-executor.md`:
  - `AUTOEXEC_MODE=1`
  - `AUTOEXEC_SKIP_HUMAN=1` when `--skiphuman` is used
- Autoexec still honors H20 recovery semantics. `BLOCKED.md` stops the loop. Missing done-file creation after a run is treated as a handoff / stop condition.

`1-create-prompt-assume-defaults.md` usage:

- file-reference example:
  - `@H20/Extras/1-create-prompt-assume-defaults.md "Make background of all pages under /Settings be #123456"`
- also works with referenced source files:
  - `@H20/Extras/1-create-prompt-assume-defaults.md @raw-prompt.txt`
- do not use a bare path like `H20/Extras/1-create-prompt-assume-defaults.md` and expect the agent to load it; use `@...` or paste the file contents
- accepted use case: small local changes where conservative defaults are safe
- refusal cases: broad features, architecture choices, integrations, migrations, or anything that would need real clarification
- output: normal milestone artifacts under `./H20/NN-<kebab>/`, including `raw-prompt.txt` and schema-conforming `good-prompt.md`

`2a-env-checker` usage:

- no args: prints color-coded syntax help
- `2a-env-checker <milestone-dir>`: scans unfinished plans inside that milestone
- `2a-env-checker <plan-file>`: scans that specific plan file
- accepted path styles include `./H20/01-my-feature`, `./01-my-feature`, and direct `PLAN-NN--*.md` paths

`3-autoexec-codex` usage:

- no args: prints color-coded syntax help
- `3-autoexec-codex --milestone <milestone-dir>`: loops Codex over pending plans inside that milestone
- accepted path styles include `./H20/01-my-feature` and `./01-my-feature`
- optional flags:
  - `--steps N`: stop after N plans
  - `--model <model-id>`: override the Codex CLI default model for this run; the current tested explicit model is `gpt-5.4`
  - `--skiphuman`: pass `AUTOEXEC_SKIP_HUMAN=1` so human-only checks are recorded as skipped
- Codex runs use `-a never`, `--sandbox danger-full-access`, `--ephemeral`, and `--skip-git-repo-check`
- If `--model gpt-5-codex` is passed, the wrapper rewrites it to `gpt-5.4` before launching Codex because ChatGPT-backed Codex CLI rejects the older alias.
