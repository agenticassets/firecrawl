---
agent: 'agent'
description: "Review recent Git commits, summarize changes, and identify incomplete or untested work to get back up to speed after time away from the codebase."
name: "catch-up"
---

# catch-up

Review recent Git commits, summarize changes, and identify incomplete or untested work to get back up to speed after time away from the codebase.

## Command Process

### Step 1: Recent Commit Analysis
Examine the last 5-10 commits to understand recent development activity:
- **Commit history**: Use `git --no-pager log` to retrieve recent commits with messages, authors, and dates (CRITICAL: use --no-pager to prevent paging)
- **File changes**: Analyze `git --no-pager diff --stat` to identify which files were modified (CRITICAL: use --no-pager to prevent paging)
- **Change patterns**: Categorize changes by type (features, bug fixes, refactoring, configuration)
- **Timeline context**: Note commit frequency and time gaps to understand development pace

### Step 2: File Change Summary
Provide a comprehensive overview of modified files:
- **File inventory**: List all changed files organized by directory/purpose
- **Change magnitude**: Indicate significant vs. minor changes per file
- **Related files**: Group related changes (e.g., component + test, route + handler)
- **Dependencies**: Note any new dependencies or package updates

### Step 3: Code Review for Completeness
Scan for incomplete work and potential issues:
- **TODO comments**: Search for `TODO`, `FIXME`, `XXX`, `HACK` comments indicating unfinished work
- **Console logs**: Identify `console.log`, `debugger`, or temporary debugging code
- **Commented code**: Flag large blocks of commented-out code that may need removal
- **Error handling**: Check for missing error handling or empty catch blocks
- **Type safety**: Note any `@ts-ignore`, `@ts-expect-error`, or `any` types that might need attention

### Step 4: Testing Coverage Analysis
Assess testing status for recent changes:
- **Test files**: Check if modified components/functions have corresponding test files
- **Test coverage**: Verify tests exist for new features or significant changes
- **Test status**: Note any skipped or disabled tests (`it.skip`, `describe.skip`, `test.skip`)
- **Integration points**: Identify areas where integration tests might be needed

### Step 5: Build and Quality Checks
Verify project health status:
- **Build status**: Check if recent changes compile successfully
- **Linter errors**: Identify any linting issues introduced in recent commits
- **Type errors**: Note TypeScript compilation errors or warnings
- **Documentation**: Check if new features have corresponding documentation updates

### Step 6: Comprehensive Summary
Generate a structured summary report:
- **Executive summary**: High-level overview of recent development focus
- **Key changes**: Bullet-point list of significant modifications
- **Incomplete items**: Prioritized list of TODOs, untested code, and potential issues
- **Recommended actions**: Suggested next steps for continuing development

## Deliverable Format

Organize the summary as:
1. **Recent Commits Overview** - Commit count, date range, main themes
2. **Files Changed** - Organized list with brief descriptions
3. **Incomplete Work** - TODOs, debugging code, missing tests
4. **Testing Status** - Coverage gaps and test file status
5. **Quality Checks** - Build, lint, and type errors
6. **Next Steps** - Recommended actions to resume work
