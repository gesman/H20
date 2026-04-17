0: Super quick start:
  - Copy ./H20/* to be under project root: ./MyProject/H20/1-create-prompt.md, etc...


1: In Claude Code / Codex (will generate good-prompt.md):
  > @H20/1-create-prompt.md "My bad prompt: Build me a website!"        OR:
  > @H20/1-create-prompt.md @raw-prompt.txt                             OR:
  > @H20/1-create-prompt.md @raw-prompt1.txt @raw-prompt2.txt .. @raw-promptN.txt   OR:
  > @H20/1-create-prompt.md @raw-prompts/
  ----------------------------------------------------
  Outputs:
  - auto-creates next milestone dir: ./H20/NN-<kebab>/        (e.g. ./H20/01-my-feature/)
  - ./H20/NN-<kebab>/raw-prompt.txt    (original user inputs, verbatim)
  - ./H20/NN-<kebab>/good-prompt.md    (crafted, execution-ready prompt)
  - /clear before next stage


2: Planner:
  > @H20/2-planner.md @H20/01-my-feature/                                OR:
  > @H20/2-planner.md @H20/01-my-feature/good-prompt.md
  ----------------------------------------------------
  Outputs:
  - ./H20/01-my-feature/ROADMAP.md
  - ./H20/01-my-feature/PLAN-01--do-this.md
  - ./H20/01-my-feature/PLAN-02--do-that.md
  - ./H20/01-my-feature/PLAN-NN--and-so-on.md
  - /clear before next stage


3: Executor (one plan per session, manually, in order):
  > @H20/3-executor.md @H20/01-my-feature/PLAN-01--do-this.md            THEN:
  > @H20/3-executor.md @H20/01-my-feature/PLAN-02--do-that.md            THEN:
  > @H20/3-executor.md @H20/01-my-feature/PLAN-03--and-so-on.md
  ----------------------------------------------------
  Does the work, writes and executes tests, prompts for UAT.
  On success, writes ./H20/01-my-feature/PLAN-NN--DONE.md and commits (if git repo).
  /clear between plans.


MORE:
  Re-run a plan after crash/interruption:
    - delete ./H20/01-my-feature/PLAN-NN--DONE.md, then run executor again:
    > @H20/3-executor.md @H20/01-my-feature/PLAN-NN--some-feature.md "Part of the plan is implemented, verify and complete missing pieces"


BLOCKED.md / user-must-intervene flow:
  - If executor hits a durable blocker (bad plan assumption, missing access/credentials, product decision it cannot safely guess, external constraint that changes the path), it writes:
    - ./H20/01-my-feature/BLOCKED.md
  - BLOCKED.md does NOT mark success and does NOT replace PLAN-NN--DONE.md recovery logic.
  - BLOCKED.md should contain:
    - what happened
    - evidence
    - earliest safe recovery point
    - workspace state
    - suggested user actions:
      A. ... (recommended)
      B. ...
      C. ...    (optional)

  Typical follow-ups:
    - patch current plan / fix external issue, then delete BLOCKED.md and re-run same plan
    - re-plan from blocker point:
      > @H20/2-planner.md @H20/01-my-feature/ @H20/01-my-feature/BLOCKED.md
    - re-do prompt as a new milestone using prior raw prompt + blocker context:
      > @H20/1-create-prompt.md @H20/01-my-feature/raw-prompt.txt @H20/01-my-feature/BLOCKED.md

  Notes:
    - executor must not say "resume from PLAN-N+1" while current plan has no DONE file
    - delete BLOCKED.md once chosen recovery path is materialized
    - if abandoning the milestone entirely, keeping BLOCKED.md as a tombstone is fine
