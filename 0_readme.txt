0: Super quick start:
  - Copy ./H2/* to be under project root: ./MyProject/H2/1-create-prompt.md, etc...


1: In Claude Code / Codex (will generate good-prompt.md):
  > @H2/1-create-prompt.md "My bad prompt: Build me a website!"        OR:
  > @H2/1-create-prompt.md @raw-prompt.txt                             OR:
  > @H2/1-create-prompt.md @raw-prompt1.txt @raw-prompt2.txt .. @raw-promptN.txt   OR:
  > @H2/1-create-prompt.md @raw-prompts/
  ----------------------------------------------------
  Outputs:
  - auto-creates next milestone dir: ./H2/NN-<kebab>/        (e.g. ./H2/01-my-feature/)
  - ./H2/NN-<kebab>/raw-prompt.txt    (original user inputs, verbatim)
  - ./H2/NN-<kebab>/good-prompt.md    (crafted, execution-ready prompt)
  - /clear before next stage


2: Planner:
  > @H2/2-planner.md @H2/01-my-feature/                                OR:
  > @H2/2-planner.md @H2/01-my-feature/good-prompt.md
  ----------------------------------------------------
  Outputs:
  - ./H2/01-my-feature/ROADMAP.md
  - ./H2/01-my-feature/PLAN-01--do-this.md
  - ./H2/01-my-feature/PLAN-02--do-that.md
  - ./H2/01-my-feature/PLAN-NN--and-so-on.md
  - /clear before next stage


3: Executor (one plan per session, manually, in order):
  > @H2/3-executor.md @H2/01-my-feature/PLAN-01--do-this.md            THEN:
  > @H2/3-executor.md @H2/01-my-feature/PLAN-02--do-that.md            THEN:
  > @H2/3-executor.md @H2/01-my-feature/PLAN-03--and-so-on.md
  ----------------------------------------------------
  Does the work, writes and executes tests, prompts for UAT.
  On success, writes ./H2/01-my-feature/PLAN-NN--DONE.md and commits (if git repo).
  /clear between plans.


MORE:
  Re-run a plan after crash/interruption:
    - delete ./H2/01-my-feature/PLAN-NN--DONE.md, then run executor again:
    > @H2/3-executor.md @H2/01-my-feature/PLAN-NN--some-feature.md "Part of the plan is implemented, verify and complete missing pieces"
