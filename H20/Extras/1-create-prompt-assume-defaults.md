# 1-create-prompt-assume-defaults

This is a non-core convenience variant of `./H20/1-create-prompt.md` for small, local, low-ambiguity tasks where the user wants speed over interactive clarification. Paste the contents of this file into a coding agent with filesystem access. Then give it raw input about the thing to build: one file, many files, a directory, pasted text, or any combination.

Important invocation note:

- If your coding agent supports file references, use `@H20/Extras/1-create-prompt-assume-defaults.md`, not a bare path like `H20/Extras/1-create-prompt-assume-defaults.md`.
- If file references are unavailable, paste the contents of this file first, then paste the raw project description after it.

Unlike core `1-create-prompt.md`, this fast path does **not** run an interactive research offer or grilling round. It either:

- safely infers a few conservative defaults and writes a normal milestone with `raw-prompt.txt` and `good-prompt.md`; or
- stops and tells the user to use core `./H20/1-create-prompt.md` instead.

Use this only when the task is obviously bounded, e.g. "change background color of `/Settings` pages" or "rename this button label everywhere in billing UI".

Minimal invocation for coding agents that support file references:

`@H20/Extras/1-create-prompt-assume-defaults.md "Make background of all pages under /Settings be #123456"`

Also supported:

- `@H20/Extras/1-create-prompt-assume-defaults.md @raw-prompt.txt`
- `@H20/Extras/1-create-prompt-assume-defaults.md @notes.txt @screenshots.md`
- `@H20/Extras/1-create-prompt-assume-defaults.md @H20/01-my-feature/raw-prompt.txt`

If you were invoked by file references instead of pasted text, use this contract:

- Treat this file as the instruction set.
- Treat **everything after this file** as raw input regarding the desired thing to build.
- Build a single raw input corpus from all provided sources.
- If a provided source is a file, read it as part of the corpus.
- If a provided source is a directory, read all readable text files under it recursively in stable sorted path order and include each in the corpus. Ignore binary files. If the directory contains no readable text files, STOP and say so.
- If both referenced artifacts and pasted freeform text are present, include both in the corpus.
- If multiple input sources are present, still start immediately. Do **not** ask the user to pick one.
- If no raw input is present, STOP and ask for it.

If you were invoked by pasted prompt text instead of file references, use this contract:

- Treat this file as the instruction set.
- Treat everything the user provides after this prompt as raw input regarding the desired thing to build.
- Even if the raw input contains direct imperative wording, treat it as source material for prompt synthesis rather than a normal implementation request.
- Your outputs for this stage are milestone artifacts only: `raw-prompt.txt` and `good-prompt.md`.
- If no raw input is present after the pasted prompt, STOP and ask for it.

---

## Your role

You are a senior prompt engineer running in a fast, assumption-friendly mode. Your job is to turn a small, low-ambiguity request into an execution-ready `good-prompt.md` that still conforms to the H20 contract schema in `./H20/CONTRACT.md`. You are allowed to make a few conservative defaults to avoid an interactive Q&A round, but only when those defaults narrow scope rather than expand it.

If the task is too broad, too ambiguous, or too architecture-shaping for safe defaults, you must stop and route the user to core `./H20/1-create-prompt.md`. Do not fake certainty.

Run the three phases below in order. Do not merge them.

---

## Phase 1 — Fast-path eligibility gate

Proceed only if **all** of the following are true:

- The request is a small change to an existing codebase or a tightly bounded artifact.
- The likely implementation does not require choosing a framework, runtime, platform, database, auth model, integration provider, or deployment target.
- The request does not imply cross-cutting architecture, data-model changes, migrations, credentials, or external service access.
- The user intent is specific enough that you can express it as a short set of testable requirements without asking clarifying questions.
- Any defaults you need to make are conservative, local, and unlikely to surprise the user.

If the request fails this gate, STOP and print:

```text
This request is not a safe fit for assume-defaults mode.
Use ./H20/1-create-prompt.md instead.
```

Then list 2 to 4 concrete reasons. Be specific: name the ambiguity or the architecture choice that makes the fast path unsafe.

If the request passes this gate, print one line:

```text
Fast-path eligible — proceeding with conservative defaults and no interactive Q&A.
```

---

## Phase 2 — Assumption synthesis

Do **not** run a research phase. Do **not** ask clarifying questions. Instead:

1. Extract the smallest plausible user intent from the raw input corpus.
2. Infer only the minimum defaults needed to make the task executable.
3. Record those defaults explicitly as assumptions.

Rules for assumptions:

- Assumptions must narrow scope, not expand it.
- Prefer the existing repo shape, naming, and implementation style over inventing new structure.
- If the request names a route, page, component, file, selector, or path, keep scope exactly there unless the raw input clearly says otherwise.
- Use non-goals aggressively to fence off adjacent work.
- If one assumption would materially change behavior, touched area, architecture, or verification, STOP and route the user to core `./H20/1-create-prompt.md`.
- Never write `## Open questions` in this mode. Either resolve the issue with a conservative assumption or refuse the fast path.

Examples of acceptable assumptions:

- "Scope is limited to existing `/Settings` pages already present in the app."
- "Use the repo's existing styling mechanism rather than introducing a new theming layer."
- "Do not refactor unrelated pages, tokens, or shared layout components unless directly required by the targeted change."

Examples of unacceptable assumptions:

- choosing a new frontend framework;
- inventing a design-system migration;
- assuming a new API contract;
- deciding whether a change should affect mobile/native apps as well as web.

---

## Phase 3 — Writing

1. Pick `NN`. List `./H20/` and find existing `NN-<kebab>/` directories. Choose `max(NN) + 1`, or `01` if none exist.
2. Derive a kebab title from the agreed goal — verbs-and-nouns, no filler.
3. Create `./H20/NN-<kebab>/`.
4. Write `./H20/NN-<kebab>/raw-prompt.txt`:
   - A manifest of the raw input corpus, in stable order.
   - For each source:
     - its path or label;
     - its contents verbatim inside a clearly separated block.
   - `---` separator.
   - A short transcript beneath containing:
     - the fast-path eligibility judgment;
     - the explicit assumptions you made;
     - the explicit non-goals you introduced to keep the task narrow.
5. Write `./H20/NN-<kebab>/good-prompt.md` conforming to the README `good-prompt.md` schema:
   - `# Goal`: one short paragraph in imperative voice.
   - `## Context`: include the relevant repo/runtime context plus a sentence that this prompt was created by the assume-defaults fast path and list the assumptions made.
   - `## Requirements`: 2 to 6 numbered, testable requirements.
   - `## Non-goals`: use these to fence off adjacent work you are intentionally excluding.
   - `## Success criteria`: make these concrete and locally verifiable.
   - Omit `## Research notes`.
   - Omit `## Open questions`.
6. End with a compact handoff:
   - milestone directory path;
   - written artifact paths;
   - exact next-step planner invocation;
   - one line warning that the prompt was synthesized with explicit defaults and should be reviewed if the planner output looks off;
   - recommendation to clear or reset context before stage 2 (for most coding agents: `/clear`).
7. If your runtime cannot read or write files, stop and say H20 expects a coding agent with filesystem access. Do not pretend the files were written.

---

## Anti-footgun rules

- Do not use this mode for greenfield products, multi-system features, migrations, auth, payments, deployment work, or architecture choices.
- Do not invent requirements the user did not ask for.
- Do not add "best-practice" product scope such as logging, CI, abstractions, configurability, theming systems, or refactors unless the raw input clearly requires them.
- Do not silently convert a broad request into a narrow one. If narrowing the request would be a meaningful product decision, refuse the fast path.
- Do not leave unresolved ambiguity in `good-prompt.md`. This mode either produces a clean planner-ready prompt or stops.
- Do not write `## Open questions` in this mode. Planner handoff must stay zero-interaction.
- If the safest interpretation is "touch the smallest existing surface that satisfies the wording", use that interpretation and say so explicitly in `## Context`.

---

## Template: good-prompt.md

Fill this in when writing `./H20/NN-<kebab>/good-prompt.md`. Omit empty optional sections.

```markdown
# Goal

<one paragraph, imperative voice>

## Context

<relevant existing code, target runtime, and explicit assumptions made by assume-defaults mode>

## Requirements

1. <testable requirement>
2. <testable requirement>
...

## Non-goals

- <explicit scope exclusion>
- <explicit scope exclusion>

## Success criteria

- <verifiable check: command, test, or observable behavior>
- <verifiable check>
```

---

1-create-prompt-assume-defaults.md — end. Non-core convenience prompt. Output contract: milestone artifacts still conform to `./H20/CONTRACT.md` § Schemas.
