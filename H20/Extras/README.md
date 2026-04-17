# Extras

Optional convenience scripts live here. They are **not** part of H20's core contract, do not change the README schemas, and can be ignored entirely.

Current extras:

- `2a-env-checker` — scans either a milestone's unfinished plans or one specific plan file and prints a manual checklist of likely environment capabilities to validate before execution.
- `3-autoexec-claude` — Claude Code wrapper that executes the next pending plan(s) for a milestone in a loop using the current user's Claude subscription.

Notes:

- `3-autoexec-claude` is Claude-specific by design. It is a user conveniencer, not part of the core H20 payload.
- Autoexec runs pass literal control lines into `3-executor.md`:
  - `AUTOEXEC_MODE=1`
  - `AUTOEXEC_SKIP_HUMAN=1` when `--skiphuman` is used
- Autoexec still honors H20 recovery semantics. `BLOCKED.md` stops the loop. Missing done-file creation after a run is treated as a handoff / stop condition.

`2a-env-checker` usage:

- no args: prints color-coded syntax help
- `2a-env-checker <milestone-dir>`: scans unfinished plans inside that milestone
- `2a-env-checker <plan-file>`: scans that specific plan file
- accepted path styles include `./H20/01-my-feature`, `./01-my-feature`, and direct `PLAN-NN--*.md` paths
