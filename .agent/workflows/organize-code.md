---
description: "Analyze and optimize codebase organization using research-backed strategies for workflow-based, feature-based, or hybrid architectures. Provides actionable recommendations and reorganization plans for TypeScript/Next.js projects (with Python/data science patterns included for mixed codebases)."
---

# organize-code

Analyze and optimize codebase organization using research-backed strategies for workflow-based, feature-based, or hybrid architectures. Provides actionable recommendations and reorganization plans for TypeScript/Next.js projects (with Python/data science patterns included for mixed codebases).

## Usage

```bash
/organize-code [folder-path]
```

## Parameters
- `folder-path` (optional): Target directory path for focused analysis. If omitted, analyzes entire codebase organization strategy.

## Procedure

### Step 1: Structure Analysis
1. **Inventory current organization**: List all files and subfolders in target scope
2. **Identify organizational pattern**: Classify as workflow-based, feature-based, layer-based, or mixed
3. **Count files per category**: Measure distribution to identify overcrowded sections (>5-7 files)
4. **Map dependencies**: Analyze import relationships and cross-folder dependencies
5. **Assess naming conventions**: Evaluate consistency of file naming patterns

### Step 2: Pattern Recognition
1. **Workflow indicators**: Identify sequential stages (e.g., `_0_*`, `_1_*`, `_2_*` prefixes)
2. **Feature boundaries**: Detect self-contained modules or domain-specific code clusters
3. **Shared utilities**: Locate cross-cutting concerns (config, utils, common functions)
4. **Data flow**: Map data pipeline stages (raw → processed → final → results)
5. **Execution order**: Determine if files follow clear sequential workflow

### Step 3: Issue Identification
1. **Overcrowded folders**: Flag categories with >7 files requiring subfolder organization
2. **Scattered features**: Identify related files split across multiple locations
3. **Deep nesting**: Detect folder hierarchies >3 levels deep (prefer flatter structures)
4. **Naming inconsistencies**: Find files that don't follow established conventions
5. **Circular dependencies**: Identify problematic import patterns
6. **Mixed concerns**: Detect folders mixing unrelated functionality

### Step 4: Strategy Recommendation
Apply research-backed decision framework:

**Use workflow-based organization when:**
- Sequential pipeline (data → features → analysis → export)
- Single researcher or small team
- Clear execution order matters
- Methodology documentation is important
- Research/data science project context

**Use feature-based organization when:**
- Multiple independent features/modules
- Large team working in parallel
- Features can be developed independently
- Need to easily remove/refactor features

**Use hybrid organization when:**
- Mix of shared utilities and feature-specific code
- Some stages have many files requiring subfolders
- Need both workflow clarity and feature isolation

### Step 5: Reorganization Plan Generation
1. **Proposed structure**: Design optimized folder hierarchy with rationale
2. **File mapping**: Create migration plan showing current → proposed locations
3. **Subfolder recommendations**: Suggest subfolders for overcrowded categories
4. **Naming improvements**: Propose consistent naming convention updates
5. **Dependency updates**: Identify import statements requiring updates
6. **Import and path preservation**: **CRITICAL** - Map all import statements and path references requiring updates
   - **TypeScript/Next.js imports**: Track all `import` and `export` statements, update relative paths (`./`, `../`) when files move
   - **TypeScript path aliases**: Verify `@/` aliases (configured in `tsconfig.json`) still resolve correctly after moves
   - **Next.js route references**: Check `app/`, `components/`, `lib/` imports and update if structure changes
   - **Python patterns** (if applicable): Identify `Path(__file__).resolve().parents[N]` patterns, `sys.path.insert()` statements, and relative imports
   - **Data file paths**: Identify any hardcoded paths to data/config files and update relative to new locations
   - **Cursor rules references**: Identify all file path references in `.cursor/rules/*.mdc` files that point to moved files
     - Search for references using `grep` to find file paths in rule files
     - Map old paths to new paths for all cursor rule documentation
     - Include this in path reference mapping inventory
7. **Execution order preservation**: Ensure workflow sequence maintained
8. **Plan document creation**: **MANDATORY** - Save comprehensive reorganization plan as markdown document:
   - **File location**: Save to `Docs/organization/reorganization_plan_[timestamp].md` or similar organized location
   - **Document length**: Must be approximately 160-240 lines (target ~200 lines)
   - **Content structure**: Include all deliverables (current structure, issues, recommendations, proposed structure, migration plan, path mappings)
   - **Conciseness**: Prioritize essential information; use bullet points and structured sections to maintain target length
   - **Completeness**: Ensure all critical details are captured within length constraint

### Step 6: Implementation Guidance
1. **Plan document saved**: Confirm markdown reorganization plan document has been saved (160-240 lines, target ~200 lines)
2. **Todo list creation**: **MANDATORY** - Immediately after saving plan document, create a structured todo list:
   - Use `todo_write` tool to create actionable todo items for reorganization execution
   - Break down migration into discrete, sequential tasks
   - Include path update tasks, file move operations, import fixes, and verification steps
   - **MUST include**: Review and update file paths/references in `.cursor/rules/*.mdc` files
     - Scan all `.mdc` files in `.cursor/rules/` for references to moved files
     - Update all file path references to reflect new locations
     - Verify cursor rules still reference correct files after reorganization
   - Prioritize critical path items (path updates, dependency fixes, cursor rules updates)
   - Set initial status: mark first actionable item as `in_progress`, others as `pending`
3. **Todo list execution**: **MANDATORY** - Work through todo list systematically:
   - Execute tasks in order, marking each as `completed` upon finish
   - Update status to `in_progress` for current task
   - Address any issues encountered and update todos accordingly
   - Do not proceed to next major phase until current phase todos are complete
4. **Migration steps**: Provide sequential steps for safe reorganization
5. **Import updates**: List files requiring import path changes
6. **Import and path updates**: **MANDATORY** - Explicitly update all import statements and path references:
   - **TypeScript import updates**: Update all `import` statements with relative paths (`./`, `../`)
     - Count directory levels: `./` = same directory, `../` = parent, `../../` = grandparent
     - Example: File moved from `components/ui/` to `components/ui/buttons/` requires `../` → `../../` for imports from `components/`
   - **Path alias verification**: Ensure `@/` aliases (from `tsconfig.json`) still resolve correctly
   - **Next.js route imports**: Verify `app/`, `components/`, `lib/` imports work from new locations
   - **Python patterns** (if applicable): Update `Path(__file__).resolve().parents[N]` depth calculations and `sys.path.insert()` statements
   - **Data/config paths**: Update any hardcoded relative paths to data or config files
   - **Cross-file references**: Verify all file-to-file references are updated (e.g., `open("../data/file.csv")` in Python, or relative imports in TypeScript)
7. **Connection verification**: **CRITICAL** - Verify all connections still work:
   - **TypeScript/Next.js**: Run `pnpm type-check` to verify all imports resolve correctly
   - **Import resolution**: Ensure all `import` statements work from new locations
   - **Path aliases**: Verify `@/` aliases resolve correctly (test with `tsc --noEmit`)
   - **Route resolution**: Confirm Next.js can resolve moved routes and components
   - **Data/config access**: Verify relative paths to data or config files still work
   - **Cross-module dependencies**: Ensure moved files can still import required modules
   - **Python** (if applicable): Test `Path(__file__).resolve().parents[N]` calculations and import resolution
8. **Testing checklist**: Identify scripts to verify after reorganization
9. **Documentation updates**: Flag documentation needing path updates:
   - Update references in README files, CLAUDE.md, and other documentation
   - **CRITICAL**: Review and update all file path references in `.cursor/rules/*.mdc` files
     - Search for references to moved files (e.g., `Code/python/CLAUDE.md`, `Code/Stata/2---Gen_Final_Dataset.do`)
     - Update paths to reflect new file locations
     - Verify all cursor rule references remain accurate after reorganization
     - Test that cursor rules still apply correctly to reorganized codebase
10. **Risk assessment**: Highlight potential breaking changes, especially path-related failures

## Deliverables

### For Folder-Level Analysis:
- **Current structure report**: Visual tree of current organization
- **Issue summary**: List of organizational problems identified
- **Recommendations**: Specific improvements with rationale
- **Proposed structure**: Optimized folder layout for target folder
- **Migration plan**: Step-by-step reorganization guide
- **Path reference mapping**: Complete inventory of all relative path references requiring updates (including `.cursor/rules/*.mdc` file references)
- **Saved plan document**: Markdown file (160-240 lines, target ~200 lines) containing complete reorganization plan saved to `Docs/organization/` or appropriate location

### For Codebase-Level Analysis:
- **Architecture assessment**: Overall organizational pattern evaluation
- **Strategic recommendations**: High-level organization strategy (workflow/feature/hybrid)
- **Priority improvements**: Top 5-10 organizational enhancements
- **Best practices alignment**: Comparison with research-backed standards
- **Scalability analysis**: Assessment of current structure's growth capacity
- **Saved plan document**: Markdown file (160-240 lines, target ~200 lines) containing complete reorganization plan saved to `Docs/organization/` or appropriate location

## Quality Standards

### Analysis Rigor
- **Comprehensive inventory**: Complete file listing with categorization
- **Dependency mapping**: Full import relationship analysis
- **Import/path reference audit**: Complete identification of all import statements and path patterns (TypeScript imports, path aliases, Python patterns if applicable, data paths, cursor rules file references)
- **Pattern recognition**: Accurate classification of organizational approach
- **Research alignment**: Recommendations based on established best practices

### Recommendations Quality
- **Actionable**: Specific, implementable suggestions with clear rationale
- **Context-aware**: Tailored to research/data science project needs
- **Minimal disruption**: Preserve existing workflow and execution order
- **Path-safe**: All relative path references explicitly updated and verified to maintain file connections
- **Scalable**: Structure supports future growth without major refactoring

### Documentation Standards
- **Visual clarity**: Folder trees and structure diagrams
- **Clear rationale**: Explain why each recommendation improves organization
- **Migration safety**: Identify risks and provide mitigation strategies
- **Reproducibility**: Document analysis methodology for future reference
- **Plan document format**: Saved markdown document must be concise (160-240 lines, target ~200 lines) while maintaining completeness
- **Todo-driven execution**: After saving plan, immediately create and execute todo list for systematic implementation

## Best Practices Applied

1. **Flat over deep**: Prefer flatter structures (<3 levels) with clear naming
2. **Group by change**: Organize files that change together
3. **Workflow-first for research**: Prioritize sequential pipeline clarity
4. **Subfolders when needed**: Add subfolders only when category has >5-7 files
5. **Consistent naming**: Maintain clear, descriptive naming conventions
6. **Preserve execution order**: Maintain workflow sequence in research projects
7. **Documentation alignment**: Ensure structure supports methodology documentation
8. **Path integrity**: **CRITICAL** - Always verify and update import statements and path references when moving files:
   - Update TypeScript import paths (`./`, `../`) based on new directory structure
   - Verify `@/` path aliases still resolve correctly
   - Run `pnpm type-check` to validate all imports
   - Update Python patterns if applicable (`Path(__file__).resolve().parents[N]`, `sys.path.insert()`)
   - Test data/config file access paths
   - Ensure cross-file connections remain functional

## Usage Examples

```bash
# Analyze entire codebase organization strategy
/organize-code

# Analyze entire codebase organization
/organize-code

# Focus on specific directory
/organize-code components/

# Analyze app router structure
/organize-code app/
```

## Validation Checklist

- [ ] Complete file inventory generated
- [ ] Organizational pattern correctly identified
- [ ] Issues flagged with specific examples
- [ ] Recommendations align with research best practices
- [ ] Proposed structure maintains workflow order
- [ ] **All import statements and path references identified and mapped** (TypeScript imports, path aliases, Python patterns if applicable)
- [ ] **Import path calculations completed** for all moved files (relative path depth changes documented)
- [ ] Migration plan includes import updates
- [ ] **Migration plan includes explicit relative path updates** with before/after examples
- [ ] **Cursor rules file references identified** - all `.cursor/rules/*.mdc` files scanned for file path references
- [ ] **Cursor rules updates planned** - mapping of old paths to new paths for cursor rule documentation
- [ ] **Connection verification steps documented** (import resolution, data access, cross-module dependencies)
- [ ] **Reorganization plan document saved** (160-240 lines, target ~200 lines) to `Docs/organization/` or appropriate location
- [ ] **Todo list created** using `todo_write` tool with actionable migration tasks (including cursor rules updates)
- [ ] **Todo list execution initiated** - working through tasks systematically
- [ ] **Cursor rules updated** - all file path references in `.cursor/rules/*.mdc` files verified and updated
- [ ] Risk assessment completed (especially path-related breaking changes)
- [ ] Documentation updates identified

Analyze codebase organization and provide research-backed recommendations for optimal folder structure, file organization, and migration strategies.
