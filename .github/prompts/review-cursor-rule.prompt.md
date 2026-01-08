---
agent: 'agent'
description: "Review and **refresh existing Cursor rules** to keep them accurate, deduplicated, and aligned with the current codebase and documentation. This command never creates new rules; it refines what already exists."
name: "review-cursor-rule"
---

# review-cursor-rule

Review and **refresh existing Cursor rules** to keep them accurate, deduplicated, and aligned with the current codebase and documentation. This command never creates new rules; it refines what already exists.

## Source of Truth

- **Read first**: `@.cursor/rules/RULES-GUIDE-V2.md` governs structure, modes, and metadata.
- Use it to validate frontmatter, application modes, size limits (50-250 lines), and file reference hygiene.

## Required Kickoff

Create a todo list before changes (use `todo_write`) that covers: reading the guide, inspecting each target rule, metadata/content checks, codebase/doc sweep, fixes, and final validation.

## End-to-End Review Flow

1. **Identify scope**: Locate the command arguments’ rule files and note recent edits.
2. **Read & map intent**: Capture each rule’s purpose, audience, and mode (Always, Auto Attached, Agent Requested, Manual). Ensure only one mode is used.
3. **Metadata check**: Frontmatter has clear one-line `description`, precise `globs` (or `description` for Agent Requested), correct `alwaysApply`, numeric filename prefix.
4. **Content audit**: Keep within 50-250 lines. Remove redundancy/wordiness, ensure bullets are specific and actionable, tighten examples. Delete stale or conflicting guidance.
5. **Codebase & doc sweep**: Search the repo for referenced files, globs, and patterns to verify they exist and match current architecture. Update or drop references that are wrong or outdated. Refresh linked docs (`@...`) or consolidate duplicates when needed.
6. **Cross-rule consistency** (when multiple targets): Detect overlapping guidance, conflicting globs, or duplicated content; consolidate or clarify boundaries.
7. **Fixes**: Apply corrections directly to the rule files; prune or add detail only where necessary to restore accuracy. Remove obsolete sections.
8. **Validation**: Re-run checklist against RULES-GUIDE-V2. If `--validate-only`, produce findings without edits.

## Checklist (apply to each rule)

- Title matches file; single H1.
- One-line description; no mixed modes (globs vs description vs alwaysApply).
- Globs are unquoted, comma-separated, and point to real paths; `alwaysApply` only when universally safe.
- Content is concise, imperative, non-duplicative, and sized appropriately.
- All `@path/to/file` references exist and remain relevant; large files avoided.
- Duplicates/conflicts resolved across reviewed rules; doc references updated or removed.

## Output Expectations

- Updated rule file(s) (unless `--validate-only`).
- Summary of changes or validation findings.
- Noted follow-ups for any broken references or docs that need separate updates.

## Sync to Windsurf (required)

After updating `.cursor/rules/*.mdc` files, sync them into `.windsurf/rules/*.md` by running:

```bash
python scripts/sync-cursor-rules-to-windsurf.py
```
