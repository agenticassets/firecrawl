---
description: "Generate a new Cursor rule (.mdc) file following project standards. This command creates new rules—ensure the rule doesn't already exist before creating."
---

# create-cursor-rule

Generate a new Cursor rule (.mdc) file following project standards. This command creates new rules—ensure the rule doesn't already exist before creating.

## Source of Truth: Cursor Rules Guide

**⚠️ REQUIRED READING**: Before creating any rule, you **must** read `@.cursor/rules/RULES-GUIDE-V2.md` as the authoritative source of truth for Cursor rules. This guide covers MDC file structure, four application modes (Always, Auto Attached, Agent Requested, Manual), frontmatter metadata rules, best practices (optimal file length 50-250 lines, token awareness, meaningful descriptions), critical behaviors and gotchas, file reference patterns, and context inclusion priority. Use this guide to ensure new rules follow correct patterns, use appropriate application modes, maintain optimal length, and reference files correctly.

## Usage

```bash
/create-cursor-rule "<rule-name>" --description "<concise-purpose>" [--globs pattern1,pattern2]
```

## Parameters

- `rule-name`: Hyphenated, lowercase with numeric prefix (e.g., `005-testing-standards`)
- `description`: One-sentence summary of rule purpose
- `globs` (optional): Comma-separated file patterns WITHOUT quotes (e.g., `app/**,lib/**,components/**`); never put an `@` sign in front of globs; include the full relative file or folder path of the globs.

## Glob Path Resolution

If user says "make a rule for the `@path` folder", resolve to actual folder structure:

- `@app/(chat)/api/` → globs: `app/(chat)/api/**`
- `@lib/ai/` → globs: `lib/ai/**`
- `@app/api,@app/actions` → globs: `app/api/**,app/actions/**`

Always verify glob paths exist in the project structure before generating the rule.

## Initial Setup: Create Todo List

**Before creating the rule, create a todo list** with step-by-step instructions for completing the creation process. Use the `todo_write` tool to create a structured task list that includes:

1. Read the Cursor Rules Guide (`@.cursor/rules/RULES-GUIDE-V2.md`)
2. Check if a similar rule already exists (avoid duplicates)
3. Determine appropriate application mode (Always, Auto Attached, Agent Requested, or Manual)
4. Verify glob paths exist if using Auto Attached mode
5. Create rule file with proper frontmatter (description, globs, alwaysApply)
6. Write focused, actionable content (50-250 lines optimal)
7. Verify file references (`@path/to/file`) point to existing files
8. Ensure rule follows naming conventions (numeric prefix)
9. Validate rule doesn't duplicate existing rule content

The todo list should break down the creation into clear, actionable steps that can be tracked and completed systematically.

## Rule Creation Principles

- **Keep focused and concise** — Optimal length: 50-200 lines (1,000-4,000 tokens); hard maximum 250 lines
- **Avoid duplication** — Check existing rules to ensure new rule doesn't overlap with existing guidance
- **One application mode only** — Cannot combine `globs` with `description` or be both Auto Attached and Agent Requested
- **Verify paths exist** — All glob patterns and file references must point to actual existing files/directories
- **Use appropriate mode** — Choose Always only for small, universally safe rules; prefer Auto Attached or Agent Requested for most cases
- **Proceed autonomously** — Make intelligent decisions about rule structure and content without requesting clarification

## Quick Examples

```bash
/create-cursor-rule "010-api-validation" --description "API route input validation patterns"

/create-cursor-rule "015-database-connections" --description "Database connection patterns" --globs lib/db/**,app/api/**

/create-cursor-rule "020-auth-security" --description "Auth and authorization security patterns" --globs middleware.ts,lib/auth/**
```

## Validation Checklist

**Before finalizing the rule, verify:**

- Rule name uses numeric prefix (001-099 range) and doesn't conflict with existing rules
- **Globs have NO quotes and are comma-separated** (if using Auto Attached mode)
- **Glob paths must be valid relative paths that exist in the project**
- **Optimal file length: 50-200 lines (1,000-4,000 tokens); hard maximum 250 lines**
- Frontmatter follows MDC format (see `@.cursor/rules/RULES-GUIDE-V2.md`)
- Description is clear, one-sentence, and accurately describes rule purpose
- Content is specific, imperative, and actionable (not vague)
- No duplicate information with existing rules
- File references (`@path/to/file`) point to existing files
- Appropriate application mode selected (Always only for small universal rules)

## Sync to Windsurf (required)

After creating a new `.cursor/rules/*.mdc` file, sync it into `.windsurf/rules/*.md` by running:

```bash
python scripts/sync-cursor-rules-to-windsurf.py
```
