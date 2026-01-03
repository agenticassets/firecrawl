# documentation-accuracy

Review and verify accuracy of documentation files (including README.md, CLAUDE.md, and related Markdown guides across subfolders) against actual codebase implementation, removing outdated information without increasing documentation complexity.

## Role

You are an expert codebase engineer specializing in maintaining, refining, and updating codebase context to make it easy to understand and facilitate continued development. Your expertise includes documentation accuracy, codebase structure analysis, and ensuring consistency across documentation, code, and development tools.

## Command Process

### Step 0: Create Task List

Before doing anything else, create a comprehensive todo list with separate, actionable todo items.

Your todo list must include, at minimum:

- **Documentation discovery tasks**: Find all in-scope docs (including `AGENTS.md`, `**/README.md`, `**/CLAUDE.md`, and related Markdown guides)
- **Per-document review tasks**: Create one todo item per doc file to verify and update
- **Consolidation tasks**: Identify overlaps and propose consolidation targets
- **Stale/deletion candidate tasks**: Identify deletion candidates and produce the candidate list (no deletion without approval)
- **Rules review tasks**: Identify and verify related Cursor/Windsurf rule files
- **Codebase verification tasks**: Identify entry points, scripts, files, and workflows to verify claims against
- **Update tasks**: Apply specific corrections/removals (and cross-reference updates)
- **Validation tasks**: Re-verify file references, instructions, and workflows after edits

Use the todo_write tool to create and track this task list throughout the process.

### Step 1: Documentation Discovery

Identify documentation files to review:

- **Folder input**: Scan the target folder (and subfolders) for:
  - `AGENTS.md`
  - `README.md`
  - `CLAUDE.md`
  - `**/README.md`
  - `**/CLAUDE.md`
  - `docs/**/*.md`
  - `**/*.md` files that appear to be guides, architecture notes, or operational runbooks
- **Repo-wide related docs**: If the user provides a topic (feature name, module name, route, tool, integration, etc.), also discover related docs across the repo by:
  - searching for the topic keyword(s)
  - searching for referenced file paths/modules imported by the code under review
  - searching for key nouns (API route names, package names, environment variables)
- **Rules and operational docs**: Include rule/config docs that impact “how to work on the repo”, such as:
  - `.cursorrules`
  - `.cursor/commands/**/*.md`
  - `.windsurf/rules/**/*.md`
  - `.windsurf/workflows/**/*.md` (when relevant to the topic)
- **File input**: Use explicitly provided documentation files directly (always include them)
- **Scope**: Prefer a bounded, topic-related set of docs; avoid reviewing unrelated Markdown files; include deeply nested `README.md`/`CLAUDE.md` files when they are related to the topic or within the selected folder scope
- **Context**: Identify what each doc claims to describe (folder/module, workflows, APIs, tooling)

### Step 2: Documentation Consolidation Assessment

Evaluate whether documentation files should be consolidated:

- **Overlap analysis**: Identify redundant content, duplicate sections, or repeated information across multiple files
- **Topic separation**: Determine if files cover distinct topics that warrant separate documentation
- **Consolidation decision**:
  - **Consolidate if**: Significant overlap exists (>30% duplicate content), files cover same domain/topic, or multiple files create maintenance burden
  - **Keep separate if**: Files cover different topics, serve distinct purposes, or separation improves clarity
- **Consolidation approach**: Merge overlapping content into 1-2 concise but robust files, preserving all unique information while eliminating redundancy
- **File organization**: Maintain logical structure with clear sections when consolidating multiple files

### Step 2.5: Stale / Duplicate Documentation Handling (Safe Deletion Flow)

Handle removal of outdated or duplicate docs safely:

- **Candidate list first**: Produce a list of deletion candidates with:
  - file path
  - why it is outdated/duplicative
  - what replaces it (new canonical doc) if applicable
- **No silent deletion**: Do not delete any files until the candidate list is reviewed and explicitly approved
- **Prefer consolidation over deletion**: If the content is still valuable but duplicated, consolidate instead of deleting
- **Deletion rules**:
  - delete only when content is clearly obsolete, contradicted by code, or fully superseded
  - if a file is referenced anywhere (other docs, code comments, workflows), update those references or do not delete

### Step 3: Codebase Analysis

Examine actual implementation to verify documentation claims:

- **Implementation inventory**: Identify the relevant entry points (routes, actions, components, libraries, scripts)
- **File structure**: Verify documented file paths and naming patterns exist
- **Workflow verification**: Trace documented workflow steps through actual code
- **Variable tracking**: Check documented variable names against code
- **Function validation**: Verify documented functions and their signatures exist

### Step 4: Accuracy Verification

Compare documentation against codebase:

- **File references**: Verify all file paths, script names, and output files exist
- **Workflow steps**: Confirm documented sequence matches actual script execution order
- **Variable names**: Validate documented variables match code implementation
- **Functionality claims**: Test documented behaviors against code logic
- **Configuration details**: Verify documented settings match code defaults
- **API and env references**: Verify any mentioned API routes, headers, env vars, and config flags exist and match current names
- **Tooling instructions**: Verify command snippets match actual package manager / scripts (e.g. `pnpm` scripts in `package.json`)

### Step 5: Outdated Information Detection

Identify and flag outdated content:

- **Removed files**: Scripts or outputs that no longer exist
- **Changed workflows**: Process steps that have been modified or reordered
- **Deprecated variables**: Variables that have been renamed or removed
- **Obsolete notes**: Comments about issues that have been resolved
- **Incorrect references**: File paths or script numbers that don't match current structure
- **Deprecated tooling**: Commands, flags, or packages that no longer exist in `package.json` or tooling configs

### Step 6: Documentation Updates

Apply corrections while maintaining brevity:

- **Remove outdated sections**: Delete references to non-existent files or obsolete processes
- **Update file paths**: Correct any path references that have changed
- **Fix script numbers**: Update script numbering if scripts have been reordered
- **Correct variable names**: Fix any variable name mismatches
- **Update workflow order**: Adjust sequence if scripts have been reordered
- **Remove resolved issues**: Delete notes about bugs or issues that are fixed
- **Preserve structure**: Maintain existing section organization and formatting
- **Consolidate when appropriate**: Merge overlapping documentation files into concise, robust single files
- **Update cross-references**: If any file is renamed/merged/deleted, update inbound links and references across the doc set

### Step 7: Cursor Rules Review

Identify and verify related Cursor/Windsurf rules that govern how to work in this repo:

- **Rule identification**: Find rule files related to the topic/folder via globs, descriptions, or file references
- **Primary rule locations**:
  - `.cursorrules`
  - `.cursor/commands/**/*.md`
  - `.windsurf/rules/**/*.md`
  - `.windsurf/workflows/**/*.md` (only where relevant to the topic)
- **Accuracy verification**: Compare rule content against actual codebase and documentation
- **Workflow validation**: Verify described developer workflows match actual scripts/configs
- **File reference check**: Ensure all file paths and referenced files in rules exist
- **Best practices compliance**: Ensure rules follow local best-practice guidance (brevity, structure, actionable constraints)
- **Update rules**: Fix outdated references, remove obsolete information, correct inaccuracies
- **Preserve brevity**: Maintain rule length and complexity - remove outdated content, don't expand

## Critical Constraints

**DO NOT:**

- Add new sections or expand existing content unnecessarily
- Increase documentation length or complexity
- Add explanatory text beyond what's necessary for accuracy
- Create new documentation patterns or structures
- Add examples or usage instructions unless correcting errors
- Expand cursor rules beyond their current scope
- Consolidate files that cover distinct topics or serve different purposes

**DO:**

- Remove outdated information completely
- Update incorrect references precisely
- Fix factual errors in existing content
- Preserve all accurate, current information
- Maintain existing documentation style and tone
- Consolidate overlapping documentation files into 1-2 concise but robust files when significant redundancy exists
- Keep documentation files separate when they cover different topics or serve distinct purposes
- Follow RULES-GUIDE-V2.md best practices when updating cursor rules (keep under 500 lines, maintain MDC structure, verify globs/descriptions)

## Deliverable Requirements

Produce updated documentation and cursor rules that:

- **Accuracy**: All file references, workflows, and claims match codebase
- **Brevity**: Same or shorter length than original (no expansion)
- **Clarity**: Maintains existing structure and readability
- **Completeness**: Preserves all accurate information
- **Currency**: Removes all outdated or incorrect information
- **Consolidation**: Overlapping documentation files merged into 1-2 concise but robust files when appropriate; distinct topics kept separate
- **Rule compliance**: Cursor rules follow RULES-GUIDE-V2.md guidelines (optimal length 50-200 lines, proper MDC structure, appropriate globs/descriptions)

## Quality Assurance

Validate updates through:

- **File existence check**: All referenced files must exist in codebase
- **Workflow verification**: Documented steps must match actual script execution
- **Variable validation**: All documented variables must exist in code
- **Length comparison**: Updated docs should not exceed original length
- **Structure preservation**: Section organization should remain unchanged
- **Rule validation**: Rules verified for accurate file references, correct instructions, and consistency with the current codebase

## Usage Examples

- `/documentation-accuracy Code/Python/3---merge-ziman-compustat-open-assets-to-master` - Review docs in specified folder
- `/documentation-accuracy @README.md @CLAUDE.md` - Review specific documentation files
- `/documentation-accuracy Code/Python/4---Factors` - Verify factor computation documentation

Review and verify documentation accuracy against codebase implementation, removing outdated information while maintaining documentation brevity and structure. Consolidates overlapping documentation files into 1-2 concise but robust files when appropriate, while keeping distinct topics separate. Also reviews and updates related Cursor/Windsurf rules (for this repo: `.cursorrules`, `.cursor/commands/**`, `.windsurf/rules/**`, and relevant `.windsurf/workflows/**`).
