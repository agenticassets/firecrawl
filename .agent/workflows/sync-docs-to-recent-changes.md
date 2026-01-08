---
description: "Use recent Git commits/diffs to identify what changed, then update all related code-based documentation and rule files (Cursor rules/commands, Windsurf workflows/rules, CLAUDE agents, READMEs, guides, any markdown files) so nothing is stale."
---

# sync-docs-to-recent-changes

Use recent Git commits/diffs to identify what changed, then update all related code-based documentation and rule files (Cursor rules/commands, Windsurf workflows/rules, CLAUDE agents, READMEs, guides, any markdown files) so nothing is stale.

## Usage

```bash
/sync-docs-to-recent-changes [--since <git-ref>] [--commits <n>] [--path <glob-or-folder>] [--validate-only]
```

## Parameters

- `--since <git-ref>`: Start point for changes (e.g. `HEAD~10`, `main`, `<sha>`). Default: `HEAD~10`.
- `--commits <n>`: Alternative to `--since` (e.g. `20`). If provided, treat as `--since HEAD~<n>`.
- `--path <glob-or-folder>`: Narrow scope (e.g. `app/(chat)`, `lib/ai/tools`, `.windsurf/workflows`). Default: repo-wide.
- `--validate-only`: Produce a report of required updates, but do not modify files.

## Process

### Step 0: Create a Task List

Create a todo list that includes:

- **Git change discovery**: commits, changed files, and high-level themes
- **Impact mapping**: identify which docs/rules are likely impacted
- **Per-file review**: one todo item per doc/rule file to verify and update
- **Cross-reference checks**: inbound links, file paths, scripts, env vars, and route references
- **Validation**: re-check claims against code after edits

### Step 1: Inspect Recent Git History (Authoritative Source)

**CRITICAL**: Always use `--no-pager` flag with git commands to prevent paging and ensure commands complete autonomously without requiring user interaction.

Use git tooling to determine exactly what changed:

- `git --no-pager log --oneline --decorate -n <n>`
- `git --no-pager diff --name-status <since>..HEAD`
- For important files: `git --no-pager diff <since>..HEAD -- <path>`

From this, produce:

- a list of changed areas (folders/modules)
- key behavior changes (APIs, schemas, workflows, tooling)
- deletions/renames that may break doc references

### Step 2: Identify Documentation + Rule Surfaces to Update

Always consider these categories:

- **Repo runbooks / canonical docs**:
  - `AGENTS.md`, `README.md`, `CLAUDE.md`, `Plan.md`
  - `**/README.md`, `**/CLAUDE.md`
- **Product/feature docs**:
  - `docs/**/*.md`
  - `app/**/docs/**/*.md`
- **Assistant rules/commands/workflows**:
  - `.cursor/rules/**/*.mdc`
  - `.cursor/commands/**/*.md`
  - `.windsurf/rules/**/*.md`
  - `.windsurf/workflows/**/*.md`
  - `.claude/agents/**/*.md`

Then, specifically map each changed code area to the likely doc/rule owners by:

- searching for changed path strings and symbols in docs/rules
- searching for route paths (e.g. `app/**/api/**/route.ts`) mentioned in docs
- searching for script names from `package.json`
- searching for env vars used in changed code

### Step 3: Update Docs + Rules (Accuracy-First)

For each impacted file:

- verify all referenced file paths exist
- verify described behavior matches actual code (routes, schemas, feature flags)
- verify `pnpm` scripts/commands match `package.json`
- remove stale/outdated content; do not add unnecessary new content
- if duplication exists, propose consolidation (do not delete without approval)

Important repo constraints to preserve when updating docs/rules:

- AI SDK 5 terminology (e.g. `maxOutputTokens`, `inputSchema`, streaming requirements)
- streaming invariants in chat routes (do not describe non-streaming patterns)
- dual database separation (App DB vs Supabase vector/storage)
- pnpm-only instructions

### Step 4: Validate

- Re-run targeted searches to ensure no stale references remain
- Verify all updated docs/rules reference existing files and correct commands
- If `--validate-only`, output a checklist of required edits instead of changing files

## Output Requirements

- A concise report:
  - what changed (from git)
  - which docs/rules were reviewed
  - what was updated and why
  - any remaining risks / follow-ups

## Examples

```bash
/sync-docs-to-recent-changes

/sync-docs-to-recent-changes --commits 25

/sync-docs-to-recent-changes --since main

/sync-docs-to-recent-changes --path .windsurf/workflows

/sync-docs-to-recent-changes --validate-only
```
