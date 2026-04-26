# 4-review

Agent-only instruction file for H20 review stage. Use it to review exactly one completed milestone or one completed `PLAN-NN--<kebab>.md`, then write immutable review artifacts under `./H20/Reviews/`.

## Invocation contract

- Treat this file as the instruction set.
- Treat the material supplied after this file, or after an explicit operator handoff telling you to read this file from disk, as review control input.
- If exactly one completed milestone directory is present, review that milestone.
- If exactly one completed `PLAN-NN--*.md` file is present, review that completed plan.
- If both a milestone directory and a plan file are present and they point to the same milestone, STOP and ask the user whether to review the full milestone or only the plan.
- If multiple candidate milestone directories or multiple candidate plan files are present, STOP and ask the user which one to review.
- If no review target is present, STOP and ask for a completed milestone directory or completed plan file.
- Treat everything else after the review target as optional seeded review concerns.
- Seeded concerns may be pasted free text, one or more referenced text files, or both.
- The review control input is review-stage input only. Do not execute implementation work, modify milestone state, or create a second completion marker.

---

## Your role

You are an independent reviewer. Your job is to review what was actually produced by a completed H20 plan or milestone, surface concrete defects and inconsistencies, and write two immutable artifacts:

- `REVIEW-NN.md` — exhaustive, human-facing review snapshot.
- `raw-review-prompt-NN.md` — narrower, machine-facing draft prompt for a possible follow-up milestone.

Your primary pass is a review of the implementation **as it exists**, not a certification that it matched the original plan. You may consult milestone context later to classify findings and to draft a sane follow-up scope, but you must not let the original plan excuse defects during the independent pass.

If the user supplied seeded review concerns, treat them as review hints, not as scope redefinition. They should steer your attention, not replace the independent review.

Run the six phases below in order. Do not merge them.

---

## Phase 1 — Resolve target and review root

1. Resolve whether the target is:
   - a milestone directory `./H20/NN-<kebab>/`; or
   - a plan file `./H20/NN-<kebab>/PLAN-NN--<kebab>.md`.
2. Resolve the owning milestone directory.
3. Resolve the project root as the parent of the `H20/` directory that owns the milestone.
4. Resolve the review output directory as:
   - `./H20/Reviews/<owning-milestone-dir-name>/`
5. Pick the next free review number local to that review output directory:
   - `01` if no prior review artifacts exist;
   - otherwise `max(existing review numbers) + 1`.
6. The output pair must be:
   - `REVIEW-NN.md`
   - `raw-review-prompt-NN.md`
7. Build a seeded-concerns list from any optional review hints that accompanied the target:
   - preserve the original wording where possible;
   - if a seeded concern came from a referenced file, read that file and include each distinct concern it contains;
   - if no seeded concerns were supplied, record that explicitly.

If your runtime cannot read or write files, STOP and say H20 review expects a coding agent with filesystem access.

Before proceeding, print one short line naming:

- the reviewed scope;
- the owning milestone;
- the review output pair you are about to write;
- whether seeded concerns were supplied.

---

## Phase 2 — Build review scope from completed work

Read only the minimum milestone artifacts needed to derive the implementation scope:

- always read `good-prompt.md` in the owning milestone;
- if present, read `ROADMAP.md`;
- if the target is a plan file:
  - require the sibling `PLAN-NN--DONE.md`;
  - read the plan file and its done-file;
  - derive the review scope from that done-file's `## Files changed`.
- if the target is a milestone directory:
  - read every `PLAN-NN--DONE.md` in stable numeric order;
  - derive the review scope from the union of every done-file's `## Files changed`;
  - incomplete plans with no done-file are out of scope and must be called out explicitly in `## Reviewed scope`.

Rules:

- If a target plan file has no sibling done-file, STOP and say review expects a completed plan or a milestone with at least one completed plan.
- If a milestone has no done-files at all, STOP and say there is nothing reviewable yet.
- Use done-files to discover scope, not as proof that the work is correct.
- Do not silently review the whole repo. Review only:
  - files named in done-files;
  - tests named there;
  - adjacent files you must read to understand correctness of those outputs.
- If repo-local instruction files exist at the project root (`CLAUDE.md`, `AGENTS.md`, or similarly obvious agent-instruction files under `.claude/` or `.agents/`), read them before inspecting code and follow them.
- Read any referenced seeded-concern files in full before starting the review.

At the end of this phase, print:

- the completed plans included in scope;
- any plans excluded because they are incomplete;
- the concrete file list you intend to inspect;
- the seeded concerns list you will explicitly try to confirm, disprove, or retire.

---

## Phase 3 — Independent implementation review

Perform an implementation-first review of the scoped outputs.

Treat the reviewed code, schemas, tests, configs, migrations, interfaces, and logic as if they arrived for review with no backstory. At this stage:

- do **not** justify defects because the plan may have allowed them;
- do **not** ask whether the implementation merely matched the plan;
- do **not** rewrite code or fix anything;
- do **not** create follow-up work yet.

Look for concrete issues such as:

- logic bugs;
- broken or underspecified schemas;
- unsafe migrations or data assumptions;
- API or interface inconsistencies;
- missing or weak verification relative to the risk of the change;
- correctness gaps between code and tests;
- bad error handling, edge-case handling, or recovery semantics;
- contradictory behavior across files produced within the milestone.

Record findings in severity order. Use this severity scale:

- `critical` — likely broken, unsafe, or materially incorrect.
- `major` — real defect or inconsistency that should probably become follow-up work.
- `minor` — lower-risk issue, maintainability concern, or weak test gap.

Do not suppress findings just because they may later be accepted as tradeoffs.

For each seeded concern, explicitly try to classify it as one of:

- `confirmed`
- `disproved`
- `not applicable`
- `inconclusive`

This classification must be recorded in `REVIEW-NN.md` even if the concern produces no independent finding.

---

## Phase 4 — Scope classification and follow-up shaping

Only after the independent findings are frozen, use milestone context to classify them.

You may now use:

- `good-prompt.md`
- `ROADMAP.md`
- the reviewed plan file when the target was a specific plan

Your job in this phase is **not** to downgrade findings into non-issues. Your job is to classify them into one of:

- `carry forward` — should become work in a follow-up milestone.
- `defer` — real issue, but intentionally not carried into the follow-up prompt right now.
- `cross-cutting` — important but broader than the reviewed milestone's follow-up scope.
- `acceptable tradeoff pending user confirmation` — possibly acceptable, but only if made explicit to the user.

Then shape a narrow candidate next milestone:

- prefer one coherent follow-up scope;
- include only findings that belong together;
- exclude unrelated or broader concerns explicitly;
- if there are multiple plausible next milestones, propose 2 or 3 options and mark exactly one recommended.

The follow-up scope must be clean enough that the user can feed `raw-review-prompt-NN.md` into the normal `./H20/1-create-prompt.md` flow as a fresh milestone seed.

---

## Phase 5 — Write REVIEW-NN.md

Write `./H20/Reviews/<milestone>/REVIEW-NN.md` using the README / CONTRACT schema for `REVIEW-NN.md`.

Requirements:

- Use the exact reviewed milestone name in the title.
- `## Reviewed scope` must say whether this was a full-milestone review or a completed-plan review.
- `## Review basis` must name:
  - review date;
  - reviewer / agent label if known, otherwise `unknown`;
  - completed done-files used to derive scope;
  - concrete files inspected.
- `## Seeded concerns` is optional; omit it only if no concerns were supplied.
- Each seeded concern entry must include:
  - the original concern text;
  - its source (`pasted`, `<path>`, or both);
  - outcome (`confirmed`, `disproved`, `not applicable`, or `inconclusive`);
  - one-sentence reasoning or evidence.
- `## Independent findings` must be a numbered list in severity order.
- Each finding must contain:
  - severity;
  - issue;
  - evidence;
  - affected files or interfaces;
  - recommended disposition.
- `## Deferred or acceptable tradeoffs` is optional; omit it if empty.
- `## Cross-cutting or unrelated observations` is optional; omit it if empty.
- `## Recommended follow-up milestones` must contain 1 to 3 labeled options, with exactly one marked recommended.

This file is the exhaustive review record. It is for humans first. Do not trim it down merely to make the next step easier.

---

## Phase 6 — Write raw-review-prompt-NN.md and hand off

Write `./H20/Reviews/<milestone>/raw-review-prompt-NN.md` using the README / CONTRACT schema for `raw-review-prompt-NN.md`.

Rules:

- Keep it narrower than `REVIEW-NN.md`.
- Carry forward only the findings you recommend turning into a fresh milestone.
- Explicitly list excluded, deferred, or unrelated findings so the scope boundary is visible.
- Include seeded concerns in the follow-up prompt only if they survived review as `confirmed` or `inconclusive` and belong in the recommended next milestone.
- Write it as raw source material suitable for feeding into `./H20/1-create-prompt.md`, not as a replacement for `good-prompt.md`.
- Do not attempt to plan or execute the follow-up work here.
- Do not overwrite any earlier review artifacts.

End with a compact handoff:

- review artifact paths;
- one line stating whether the recommended next step is to use the generated raw review prompt as-is or to edit it first;
- exact next-step invocation:
  - `@H20/1-create-prompt.md @H20/Reviews/<milestone>/raw-review-prompt-NN.md`
- recommendation to clear or reset context before starting the next stage (for most coding agents: `/clear`).

---

## Anti-footgun rules

- Do not mutate any existing milestone artifacts.
- Do not create or delete `PLAN-NN--DONE.md`, `BLOCKED.md`, `good-prompt.md`, or `ROADMAP.md`.
- Do not create a second completion marker for milestones.
- Do not overwrite earlier review snapshots or follow-up prompts.
- Do not review incomplete plan outputs as if they were complete.
- Do not silently widen scope from one milestone into unrelated repo areas.
- Do not let seeded concerns replace the actual review scope derived from completed milestone outputs.
- Do not let plan intent excuse defects during the independent review pass.
- Do not auto-merge findings from multiple review runs. Each run is an immutable snapshot.
- Do not assume the generated `raw-review-prompt-NN.md` must carry every finding forward. Be explicit about exclusions.
- Do not fix code during review. Review produces artifacts only.

---

## Template: REVIEW-NN.md

Fill this in when writing `./H20/Reviews/<milestone>/REVIEW-NN.md`. Omit empty optional sections.

```markdown
# Review NN: <reviewed milestone title>

## Reviewed scope

<reviewed milestone path, whether this was a full-milestone or completed-plan review, and any exclusions>

## Review basis

<review date, reviewer / agent label if known, done-files used to derive scope, and files actually inspected>

## Seeded concerns

- Concern: <original concern text>
  Source: <pasted|path|both>
  Outcome: <confirmed|disproved|not applicable|inconclusive>
  Reasoning: <one sentence>

## Independent findings

1. Severity: <critical|major|minor>
   Issue: <what is wrong>
   Evidence: <concrete evidence>
   Affected files or interfaces: <paths / APIs / schemas>
   Recommended disposition: <carry forward|defer|cross-cutting|acceptable tradeoff pending user confirmation>

## Deferred or acceptable tradeoffs

- <item>

## Cross-cutting or unrelated observations

- <item>

## Recommended follow-up milestones

- A. <option>
- B. <option>
- Recommended: <A|B|C> — <one-sentence why>
```

## Template: raw-review-prompt-NN.md

Fill this in when writing `./H20/Reviews/<milestone>/raw-review-prompt-NN.md`.

```markdown
# Raw review prompt NN: <proposed follow-up title>

## Source review

<path to REVIEW-NN.md and one-sentence description of the review scope>

## Goal

<one paragraph describing the fresh follow-up milestone to create>

## Findings included

1. <finding intentionally carried forward>
2. <finding intentionally carried forward>

## Findings explicitly excluded

- <finding deferred, unrelated, or intentionally excluded from this follow-up scope>

## Constraints

- <scope fence or assumption>
- <scope fence or assumption>

## Success criteria

- <verifiable outcome>
- <verifiable outcome>
```

---

4-review.md — end. Non-core review-stage prompt. Output contract: review artifacts conform to `./H20/CONTRACT.md` § Schemas.
