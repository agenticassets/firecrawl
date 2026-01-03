# review-and-consolidate-docs

Review, consolidate, and update documentation for a specific feature or component, ensuring accuracy and maintaining up-to-date cursor rules.

## Usage

```bash
/review-and-consolidate-docs <feature-name> [--validate-only]
```

## Parameters

- `feature-name`: Name or keyword identifying the feature/component (e.g., `citations`, `authentication`, `document-tools`)
- `--validate-only` (optional): Review and report without making changes

## Process Steps

### Step 1: Identify Documentation Files

- Search `docs/` directory and subdirectories for files related to the feature
- Use `glob_file_search` to locate likely files by keyword/extension
- Use `grep` to find mentions in existing documentation and code
- Use `codebase_search` for semantic search of related functionality
- List all relevant files and identify duplicates or overlapping content

### Step 2: Research Current Implementation

- Use `codebase_search` and `grep` to locate authoritative entry points (routes/components/lib)
- Read key implementation files identified in searches
- Verify data flows, architecture patterns, and key functions
- Check for recent changes or refactors not reflected in docs
- Document actual file paths and line numbers for key functions

### Step 3: Consolidate Documentation

- Merge related documentation into 1-2 comprehensive guides
- Remove duplicate or outdated information
- Organize by logical sections: architecture, usage, examples, troubleshooting
- Include file references with line numbers: `lib/path/file.ts` (lines 123-145)
- Keep guides concise (100-150 lines recommended, max 200)
- Save consolidated guides to appropriate `docs/` subdirectory

### Step 4: Verify Cursor Rules

- Search `.cursor/rules/` for mentions of the feature (via `grep_search`)
- Review globs to ensure they target correct files
- Update rules with accurate, current information
- Add missing functionality without adding complexity
- Keep rules within size guidelines (50-250 lines)
- Verify frontmatter (description, globs, alwaysApply) is correct

### Step 5: Clean Up

- Delete consolidated/outdated documentation files
- Verify no broken references or missing context
- Ensure new guides are properly formatted and accessible

## Principles

- **Accuracy First**: Documentation must reflect actual codebase implementation
- **Conciseness**: Prefer fewer, comprehensive guides over many fragmented files
- **File References**: Include specific file paths and line numbers for key functions
- **No Complexity**: Cursor rules should inform, not overwhelm with details
- **Maintainability**: Structure documentation for future updates

## Success Criteria

- All documentation is accurate and up-to-date with codebase
- Documentation consolidated into 1-2 focused guides
- Cursor rules reflect current implementation accurately
- No duplicate or conflicting information
- File references are accurate and helpful

## Example Usage

```bash
/review-and-consolidate-docs citations

/review-and-consolidate-docs authentication --validate-only

/review-and-consolidate-docs document-tools
```
