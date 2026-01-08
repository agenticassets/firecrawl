---
agent: 'agent'
description: "Smartly implement an existing plan or recommendation list for this repo."
name: "implement-plan"
---

# implement-plan
Smartly implement an existing plan or recommendation list for this repo.

## When to Use
- You already have a written plan, recommendations, or checklist to execute.
- Tasks include refactors, new features, or maintenance work.
- You need careful execution with validation before and after changes.

## Preconditions
- Identify and quote the source plan/recommendations you will execute.
- Create or update a TODO list **before coding** that mirrors the plan (granular, ordered).
- Confirm repo state is clean enough to proceed; note any pre-existing changes.

## Execution Steps
1) **Understand scope**: Restate goals, constraints, and acceptance criteria from the plan.
2) **Plan to TODOs**: Convert the plan into TODO items (one active `in_progress` at a time). Update as you work.
3) **Context check**: Read relevant files; avoid unnecessary edits; follow project rules (AI SDK 5, Tailwind v4, etc.).
4) **Implement carefully**: Execute tasks sequentially; keep changes minimal and aligned to the plan; add succinct rationale comments only when helpful.
5) **Self-review per task**: After each task, skim for logic errors, type issues, and rule violations; adjust TODO status.
6) **Validation**: Run targeted checks (lint/type/tests) when scope warrants; note any unrun checks.
7) **Final review**: Inspect diffs for accidental changes, secrets, or style drift; ensure text sizing uses CSS vars; confirm streaming/AI SDK 5 patterns where relevant.

## Outputs to Provide
- Brief execution summary tied to the original plan items.
- Current TODO list status.
- Tests/checks run (or not run) with results.
- Notable risks, follow-ups, or unaddressed items.

## Quality Safeguards
- Prefer simple, direct solutions; avoid scope creep.
- No new CSS files; use existing patterns and CSS variables for sizing.
- Do not mix App DB and Supabase vector DB.
- No TODO/placeholder code left behind.
- Respect repo rules: AI Gateway + AI SDK 5, streaming patterns, Tailwind v4 practices.

## Failure Handling
- If blocked or plan is unclear, pause and ask for clarification.
- If pre-existing issues are encountered, describe them and propose a safe path before proceeding.






