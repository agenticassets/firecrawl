---
description: "Cursor Rules expert reference guide - MDC file structure, application modes, file references, best practices, and critical behaviors for creating project, user, and team rules"
name: "008-rules-guide-v2"
---

# Cursor Rules: Expert Guide

## Core Concept

Rules provide persistent, reusable instructions to Cursor's Agent and Inline Edit that are injected at the start of every AI context window. LLMs don't retain memory between completions—rules solve this by giving consistent guidance for code generation, edits, and workflows.

## Rule Types

| Type | Location | Scope | Version Control |
|------|----------|-------|-----------------|
| **Project Rules** | `.cursor/rules/*.mdc` | Project-specific | Yes |
| **User Rules** | Settings → Rules | All projects globally | No |
| **Team Rules** | Cursor Dashboard | Organization-wide | No |
| **AGENTS.md** | Project root | Simple alternative to `.mdc` | Yes |

## Project Rules (.mdc Files)

### Four Application Modes

**Always** (`alwaysApply: true`) - Included in every AI interaction across entire project.

**Auto Attached** (`globs: **/*.tsx`) - Automatically included when files matching glob patterns are *attached or mentioned in chat*. Does not trigger for new file creation or passive editing.[^10a]

**Manual** - Only included when explicitly invoked with `@ruleName` in chat.

**Agent Requested** (`alwaysApply: false` + `description`, no globs) - AI autonomously decides whether to fetch the rule based on description. The agent first evaluates the description, then requests the full rule if relevant.[^10]

### MDC File Structure

```markdown
---
description: RPC Service boilerplate
globs: **/*.ts,**/*.tsx
alwaysApply: false
---

- Use internal RPC pattern for services
- Always use snake_case for service names

@service-template.ts
```

**Metadata Rules:**

- Use **one mode only**: A rule cannot combine `globs` with `description` or be both Auto Attached and Agent Requested.[^17]
- Frontmatter uses `---` delimiters (MDC format, not YAML).

### Nested Rules

Place `.cursor/rules` directories in subdirectories to create scoped rules that automatically activate when files in that directory are referenced:

```markdown

project/
.cursor/rules/         \# Project-wide
backend/
.cursor/rules/       \# Backend-specific
frontend/
.cursor/rules/       \# Frontend-specific

```

## Creating Rules

**From Command Palette**: Use `New Cursor Rule` command.

**From Settings**: Navigate to `Cursor Settings > Rules` to see all rules and create new ones.

**From Chat**: Use `/Generate Cursor Rules` command to convert chat decisions into reusable rules.

## Team Rules (Team/Enterprise Plans)

Managed from Cursor Dashboard by admins.

**Enable immediately** - Activates rule for all members instantly.

**Enforce this rule** - Prevents team members from disabling the rule in their settings.

Team Rules are plain text (no MDC format) and apply globally across all projects. They take highest precedence: **Team Rules → Project Rules → User Rules**.

## AGENTS.md (Simple Alternative)

Plain markdown file in project root—no metadata, no complex configuration. Perfect for straightforward instructions without `.mdc` overhead. Supports nested `AGENTS.md` files in subdirectories, with nearest file taking precedence (like `.gitignore` behavior).

```markdown
# Code Style

- Use TypeScript for all new files
- Prefer functional components in React
- Use snake_case for database columns


## Architecture

- Follow the repository pattern
- Keep business logic in service layers
```

## User Rules

User rules are global preferences defined in **Cursor Settings → Rules** that apply across all projects. They're plain text and perfect for personal preferences:

```markdown
Please reply in a concise style. Avoid unnecessary repetition or filler language.
```

## Best Practices

**Keep focused**: Under 500 lines per rule.

**Split wisely**: Break large rules into composable, single-purpose rules.

**Be concrete**: Provide examples or use `@filename` references rather than vague guidance.

**Write like docs**: Clear, actionable instructions—not abstract principles.

**Reuse patterns**: When you repeat prompts in chat, convert them to rules.

**Name with numbers**: Use prefix like `001-name.mdc` for rule ordering (higher numbers = higher precedence).[^11]

**Token awareness**: Normal mode uses 200k token context (~16,000 lines). Rules consume from this budget.[^12]

**Meaningful descriptions**: For Agent Requested rules, descriptions are how the AI decides when to fetch them.[^13]

**Optimal Rule File Length**: Sweet spot is 50-200 lines per rule file (roughly 1,000-4,000 tokens). Hard maximum: 250 lines—beyond this, AI coherence degrades and context consumption becomes excessive.

## Critical Behaviors & Gotchas

**Auto-attach limitation**: Glob-based rules only trigger when matching files are *attached or mentioned in chat*, NOT when creating new files.[^10a]

**Exclusive modes**: Rules cannot be both Auto Attached (globs) and Agent Requested (description) simultaneously.[^15]

**Rule evaluation**: Even when a rule is in context (via `alwaysApply` or glob match), the AI may still omit it if deemed irrelevant to the query.[^17]

## Context Inclusion Priority

Rules are merged in this order when contexts overlap:

1. Team Rules (highest precedence)
2. Project Rules
3. User Rules

Earlier sources win when guidance conflicts.

## File References in Rules

**⚠️ Context Window Warning**: Each `@filename` reference pulls the **entire file** into your context window budget. This consumes tokens immediately and reduces space for user code and chat history. Use sparingly and only for critical, concise files (< 2KB recommended). Avoid including large configuration files, documentation, or code files larger than 500 lines.[^16]

Use `@` symbol to automatically include files in context:

- `@/lib/guidelines-filename.md` - Pulls file into context when rule is active
- `/lib/guidelines-filename.md` - Just plain text, does NOT include file
- Backticks around references (`@/docs/setup-filename.md`) are just markdown formatting

**Best Practice**: Reference small, focused guide files (checklists, snippets) rather than entire modules. For large files, use inline code comments instead.

## Migration Notes

Legacy `.cursorrules` files in project root are still supported but **deprecated**—migrate to Project Rules (`.mdc`) or `AGENTS.md`.

This markdown guide is ready to copy and use. You can save it as a reference document or paste it directly into your project documentation.[^1][^2][^3][^4][^5][^6][^7][^8][^9][^10][^11][^12][^13][^14][^15][^16][^17]

[^1]: <https://cursor.com/docs/context/rules>

[^2]: <https://forum.cursor.com/t/optimal-structure-for-mdc-rules-files/52260>

[^3]: <https://kirill-markin.com/articles/cursor-ide-rules-for-ai/>

[^4]: <https://www.reddit.com/r/cursor/comments/1nqlb9a/best_way_to_use_a_large_10000_lines_company_style/>

[^5]: <https://trigger.dev/blog/cursor-rules>

[^6]: <https://forum.cursor.com/t/guide-a-simpler-more-autonomous-ai-workflow-for-cursor-new-update/70688>

[^7]: <https://www.youtube.com/watch?v=ABozvKmctkc>

[^8]: <https://github.com/PatrickJS/awesome-cursorrules>

[^9]: <https://www.lullabot.com/articles/supercharge-your-ai-coding-cursor-rules-and-memory-banks>

[^10]: <https://roman.pt/posts/cursor-under-the-hood/>

[^11]: <https://forum.cursor.com/t/optimal-structure-for-mdc-rules-files/52260/8>

[^12]: <https://cursor.com/docs/context/max-mode>

[^13]: <https://forum.cursor.com/t/cursor-rules-mdc-clarification/104879>

[^14]: <https://playbooks.com/rules>

[^15]: <https://forum.cursor.com/t/allow-rules-to-auto-attach-and-be-agent-requested-at-the-same-time/64319>

[^16]: <https://cursor.com/docs/context/max-mode>

[^17]: <https://forum.cursor.com/t/allow-rules-to-auto-attach-and-be-agent-requested-at-the-same-time/64319>

[^10a]: <https://forum.cursor.com/t/my-take-on-cursor-rules/67535>