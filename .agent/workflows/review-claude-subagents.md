---
description: "Review and validate **existing** Claude Code subagent files to ensure accuracy, correct file references, adherence to best practices, and compliance with the Subagents Guide. This command is for reviewing agents that already exist—it does not create new agents."
---

# review-claude-subagents

Review and validate **existing** Claude Code subagent files to ensure accuracy, correct file references, adherence to best practices, and compliance with the Subagents Guide. This command is for reviewing agents that already exist—it does not create new agents.

## Source of Truth: Subagents Guide

**⚠️ REQUIRED READING**: Before reviewing any subagent file, you **must** read `@.claude/subagents-guide.md` as the authoritative source of truth for Claude Code subagents. This guide covers:

- **Subagent Structure**: YAML frontmatter format (name, description, tools, model, permissionMode, skills)
- **File Format**: Markdown files with frontmatter metadata and system prompt content
- **Best Practices**: Focused responsibilities, specific descriptions, appropriate tool permissions, model selection
- **Description Guidelines**: Critical for auto-delegation—must clearly state when to use the agent with trigger terms
- **Tool Permissions**: Restrict to necessary tools for security and focus
- **Model Selection**: Choose appropriate model (haiku, sonnet, opus, inherit) based on task complexity
- **File Location**: Project agents (`.claude/agents/`) override user agents (`~/.claude/agents/`)

All validation should align with the standards and practices documented in this guide. Subagent markdown files **must** follow the patterns and requirements specified in `@.claude/subagents-guide.md`.

## Initial Setup: Create Todo List

**Before starting the review, create a todo list** with step-by-step instructions for completing the review process. Use the `todo_write` tool to create a structured task list that includes:

1. Read the Subagents Guide (`@.claude/subagents-guide.md`)
2. Read and analyze each specified subagent file
3. Validate frontmatter (name, description, tools, model, permissionMode, skills)
4. Validate content (system prompt clarity, expertise areas, file references)
5. Check description quality (specificity, trigger terms, auto-delegation readiness)
6. Verify tool permissions are appropriate and not overly broad
7. Validate model selection matches task complexity
8. If multiple agents: Check for duplicates, conflicts, and overlapping responsibilities
9. Verify all file references (`@path/to/file`) point to existing files
10. Check related documentation files for updates needed
11. Update, delete, or consolidate documentation as needed
12. Make necessary corrections and updates

The todo list should break down the review into clear, actionable steps that can be tracked and completed systematically.

## Usage

```bash
/review-subagent <agent-name> [<agent-name2> ...] [--validate-only]
/review-subagent @.claude/agents [--validate-only]
```

## Parameters

- `agent-name`: Name of **existing** subagent file(s) from `.claude/agents/` directory (e.g., `testing-expert`, `security-expert`). The agent file must already exist. Multiple agents can be specified for batch review.
- `@.claude/agents`: Review all subagent files in the `.claude/agents/` folder
- `--validate-only` (optional): Verify agent without making changes

## Reviewing Multiple Agents

When multiple agents are specified (or when reviewing the entire `.claude/agents/` folder), review **all** agents together and check for:

- **Duplicate responsibilities** — Identify overlapping expertise areas or conflicting guidance
- **Unnecessary complexity** — Look for redundant explanations, overly verbose sections, or duplicated file references across agents
- **Consistent patterns** — Ensure agents follow the same structure, formatting, and style conventions
- **Optimal organization** — Confirm agents are logically separated and each serves a distinct purpose without excessive overlap
- **Description conflicts** — Verify descriptions don't create ambiguity about when to use each agent
- **Tool permission consistency** — Ensure similar agents have consistent tool access patterns

The goal is to ensure the agent set as a whole is well-organized, non-redundant, and maintains clear boundaries between individual agents.

## Documentation Maintenance

When reviewing agents, also check and maintain related documentation files and guides referenced in the agents:

- **Update outdated documentation** — If agents reference documentation files (e.g., `@docs/guide.md`, `@CLAUDE.md`), verify those files are current and update them if they contain outdated information
- **Delete obsolete documentation** — If documentation files are completely outdated or no longer relevant, delete them rather than leaving stale references
- **Consolidate duplicates** — If multiple documentation files cover the same topic, consolidate them into a single authoritative source and update agent references accordingly
- **Verify file references** — Ensure all `@path/to/file` references in agents point to existing, up-to-date documentation

**Proceed intelligently** — Make these revisions and updates without asking for clarification. Use your judgment to determine what needs updating, what should be deleted, and how to best consolidate duplicate documentation. The goal is to maintain accurate, current documentation that supports the agents effectively.

## Review Checklist

**Purpose**: Validate accuracy and correctness—do NOT expand or make agents more complex. Keep existing length and scope.

**Frontmatter Validation:**
- `name` is lowercase with hyphens (e.g., `testing-expert`)
- `description` is clear, specific, and includes trigger terms for auto-delegation
- `tools` are appropriate and not overly broad (prefer restricted tool lists)
- `model` is appropriate for task complexity (haiku for simple, sonnet for balanced, opus for complex)
- `permissionMode` (if present) is correctly configured
- `skills` (if present) reference valid skill names
- Frontmatter follows YAML format with proper `---` delimiters

**Content Validation:**
- System prompt is clear and focused on specific expertise
- Expertise areas are well-defined and actionable
- File references (e.g., `@path/to/file`) point to actual existing files
- Code examples (if present) are accurate and follow project patterns
- No outdated patterns or deprecated approaches
- **When reviewing multiple agents**: Check for duplicate information, overlapping responsibilities, and unnecessary complexity across the agent set

**Description Quality Check:**
- Description clearly states when to use the agent
- Includes trigger terms users might mention
- Specific enough to avoid false positives
- Follows format: "Use when [specific scenario]" or similar clear pattern

**Tool Permissions Check:**
- Tools are restricted to necessary set (not inheriting all tools unless justified)
- Read-only agents use minimal tool sets (Read, Grep, Glob)
- Agents with write capabilities have appropriate restrictions
- Tool lists follow comma-separated format

**Model Selection Check:**
- Model choice matches task complexity
- Simple tasks use `haiku`
- Balanced tasks use `sonnet` (default)
- Complex reasoning uses `opus`
- `inherit` is used when appropriate

## Quick Examples

```bash
/review-subagent testing-expert

/review-subagent security-expert testing-expert ai-sdk-5-expert --validate-only

/review-subagent @.claude/agents

/review-subagent react-expert
```

## Validation Principles

- **No expansion or complexity increase** — Maintain agent length and scope exactly as-is
- **Accuracy only** — Correct outdated file references, fix broken paths, update deprecated patterns
- **Accurate descriptions** — Verify descriptions are specific and include trigger terms
- **Actionable content** — Ensure expertise areas, constraints, and patterns remain clear
- **Correct metadata** — Verify frontmatter format and values match agent purpose
- **File reference validation** — Confirm all `@path/to/file` references point to existing files
- **Documentation maintenance** — Update, delete, or consolidate related documentation files as needed
- **Guide compliance** — Ensure agents follow all patterns from `@.claude/subagents-guide.md`
- **Proceed autonomously** — Make intelligent revisions and updates without requesting clarification
