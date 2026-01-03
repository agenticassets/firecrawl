# create-project-claude

Generate or update comprehensive project root CLAUDE.md as single source of project truth with essential context and rules.

## Usage

```bash
/create-project-claude [refresh|analyze|validate|condense]
```

## Parameters

- `mode` (optional): Operation mode - "refresh" (regenerate from current state), "analyze" (review existing), "validate" (check completeness), or "condense" (create compact version 150-200 lines). Defaults to "refresh".

## Procedure
1. **Parse mode and arguments**: Determine operation type and validate project structure exists.
2. **Extract core context**: Identify critical rules, tech stack, architecture decisions from codebase.
3. **Assemble documentation**: Compile essential project information using standardized template structure.
4. **Apply mode-specific logic**:
   - **refresh**: Generate comprehensive CLAUDE.md with all essential context
   - **analyze**: Review existing CLAUDE.md and suggest improvements
   - **validate**: Check completeness against project standards
   - **condense**: Create compact version (150-200 lines) preserving critical rules
5. **Format output**: Ensure flat bullet lists, clear headings, no nested structures beyond 2 levels.
6. **Write to disk**: Save as root-level CLAUDE.md with proper frontmatter.

## Deliverables

- **Updated CLAUDE.md**: Production-ready documentation file as single source of project truth.
- **Console summary**: Brief report of operation performed, sections generated, and line count.
- **Mode-specific outputs**: Analysis report, validation results, or condensed version as appropriate.

## Validation
- **Length control**: Target 150-200 lines for condensed mode, comprehensive for refresh mode.
- **Structure compliance**: Verify sections follow project sequencing and naming conventions.
- **Content quality**: Ensure critical rules are front-loaded and non-negotiable instructions are bolded.
- **Freshness check**: Validate against current codebase state and flag outdated information.
- **Token efficiency**: Use declarative bullet points, avoid rambling prose, maintain scannable format.
