---
agent: 'agent'
description: "Refine, update, and improve Claude Code subagent markdown files in this repo. You are my **Claude code agent expert**."
name: "refine-claude-subagents"
---

# refine-claude-subagents

Refine, update, and improve Claude Code subagent markdown files in this repo. You are my **Claude code agent expert**.

You must first read `@.claude/subagents-guide.md` and treat it as the authoritative source of truth for subagent format and best practices.

## What this command does

Depending on the user input, you will do one of the following:

1. **Refine existing agent file(s)** (single agent or multiple agents)
2. **Refine ALL agents in a referenced folder** (e.g. `@.claude/agents`)
3. **Create a new agent** (a new `.md` file) when the user explicitly requests a new agent

## Required reading (non-negotiable)

Before making any edits or creating any new agent:

- Read `@.claude/subagents-guide.md`

## Authoritative documentation freshness (required)

When refining agent files, you must ensure the agent’s guidance matches the most up-to-date authoritative documentation for that domain.

Requirements:

- Identify the domain(s) the agent covers (e.g. React, Next.js, Tailwind, Supabase, Vercel AI SDK, Drizzle, Playwright).
- Use available **MCP documentation/search tools** to retrieve and verify current best practices and APIs for the domain.
  - Prefer web search + scrape tools when validating vendor/framework docs.
  - Prefer domain-specific doc search tools when available (e.g., Supabase docs search for Supabase-related agents).
- Ensure there is an **authoritative repo documentation file** under `docs/` that captures the repo’s current stance for that domain.
  - If missing: create it.
  - If present but stale: update it.
- Update the agent prompt to reference the authoritative `docs/` file(s) using `@docs/...` paths.

## Inputs / Usage

Examples:

```bash
/refine-claude-subagents security-expert

/refine-claude-subagents security-expert testing-expert ai-tools-expert

/refine-claude-subagents @.claude/agents

/refine-claude-subagents create:new-agent-name "Use when …" "Primary responsibilities …"
```

## Behavior rules

### A) If user references a specific agent name

- Treat it as `.claude/agents/<agent-name>.md` unless the user provides a full path.
- Read the file before changing anything.
- Refine and update it for:
  - frontmatter correctness (YAML, required fields)
  - description quality for auto-delegation trigger terms
  - tool list appropriateness (least privilege)
  - model choice appropriateness (typically default to `haiku` for cost/quality; use `sonnet` for agents that truly need stronger intelligence)
  - prompt structure clarity (Role, Mission, Constraints, Method, Output contract)
  - correctness of any `@path` references (must exist)
  - correctness and freshness of domain guidance by:
    - validating against up-to-date authoritative sources via MCP tools
    - ensuring an up-to-date `docs/` authoritative reference exists
    - pointing the agent to `@docs/...` as the repo source of truth

### B) If user references a folder

- If the user references an entire folder (example: `@.claude/agents`), do a thorough review and improvement pass across **all agents in that folder**.
- Improve the set as a whole:
  - remove duplication and ambiguity across descriptions
  - ensure consistent structure and formatting across agents
  - ensure responsibilities are clearly partitioned
  - normalize tool lists and model choices (where appropriate)
  - ensure every domain represented by agents has an up-to-date authoritative `docs/` reference
  - update agent `@docs/...` references to point to those authoritative docs

### C) If user asks for a new agent file

When the user requests a new agent, you must create a new file under `.claude/agents/<name>.md` using the format from the Subagents Guide:

```markdown
---
name: <kebab-case-name>
description: <clear use-when description with trigger terms>
tools: <comma-separated tool list or blank to inherit>
model: <haiku|sonnet|inherit>
---

<Role>

<Mission>

<Constraints>

<Method>

<Output format>
```

Requirements:

- Use **lowercase kebab-case** for `name`.
- `description` must be specific enough for auto-delegation.
- Choose tools via least-privilege.
- Choose `model` based on complexity.
- The body must be concise, structured, and actionable.

## Quality bar

- Make changes directly in the repo (don’t just suggest them).
- Don’t add fluff; keep agents focused.
- Avoid contradictions across agents.
- Validate that referenced files exist.
- Validate that referenced documentation reflects current upstream authoritative docs (via MCP tools).

## Deliverables

- Updated agent file(s) (or a new agent file)
- A brief summary of what changed and why
