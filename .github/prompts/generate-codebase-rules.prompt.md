---
agent: 'agent'
description: "**Analyze codebase and generate Cursor rules** — Reviews project structure, patterns, dependencies, and key files to create 4-8 comprehensive Cursor rules following the RULES-GUIDE-V2.md guide."
name: "generate-codebase-rules"
---

# generate-codebase-rules

**Analyze codebase and generate Cursor rules** — Reviews project structure, patterns, dependencies, and key files to create 4-8 comprehensive Cursor rules following the RULES-GUIDE-V2.md guide.

## Purpose

This command performs a comprehensive analysis of the codebase to understand:

- Project structure and organization patterns
- Technology stack and dependencies
- Component patterns (Server vs Client Components)
- API route patterns
- TypeScript type definitions and conventions
- Context and hooks usage
- Constants and utilities organization
- File naming conventions
- Import/export patterns

Then generates 4-8 focused Cursor rules (.mdc files) with appropriate:

- Application modes (Always, Auto Attached, Agent Requested, or Manual)
- Glob patterns (for Auto Attached rules)
- Descriptions (for Agent Requested rules)
- Content following best practices (50-250 lines optimal)

## Process

### Step 1: Codebase Analysis

Analyze the following areas systematically:

1. **Project Structure**
   - Directory organization (`app/`, `components/`, `hooks/`, `contexts/`, `types/`, `constants/`, `lib/`)
   - File naming conventions (kebab-case, PascalCase)
   - Entry points (`app/page.tsx`, `app/layout.tsx`)

2. **Technology Stack**
   - Framework: Next.js version and App Router usage
   - React version and patterns (Server Components, Client Components)
   - TypeScript configuration and strict mode settings
   - Styling: Tailwind CSS version and configuration
   - UI libraries: shadcn/ui, Radix UI components
   - Map library: Leaflet integration patterns

3. **Component Patterns**
   - Server Component vs Client Component usage (`'use client'` directive)
   - Component organization (feature-based directories)
   - Props interfaces and TypeScript types
   - Context providers and consumers
   - Custom hooks patterns

4. **API Routes**
   - Route handler patterns (`GET`, `POST`, etc.)
   - Request/response handling
   - Error handling
   - Data fetching and caching

5. **Type Definitions**
   - Type organization (`types/` directory)
   - Interface vs type usage
   - Generic types
   - Type exports

6. **Hooks and Contexts**
   - Custom hook patterns (`hooks/` directory)
   - Context creation and provider patterns
   - Hook naming conventions (`use-` prefix)

7. **Constants and Utilities**
   - Constants organization (`constants/` directory)
   - Utility functions (`lib/utils.ts`, `lib/utils/`)
   - Configuration patterns

8. **Dependencies**
   - Review `package.json` for key libraries
   - Understand integration patterns

### Step 2: Rule Generation Strategy

Generate 4-8 rules covering distinct areas:

**Suggested Rule Categories:**

1. **Next.js App Router** — Server Components, API routes, routing patterns
2. **Leaflet Map Integration** — Map initialization, context usage, event handling
3. **React Component Patterns** — Component structure, hooks, context providers
4. **TypeScript Conventions** — Type definitions, interfaces, type organization
5. **Styling and UI** — Tailwind CSS, shadcn/ui components, responsive design
6. **API Routes** — Route handlers, request/response patterns, error handling
7. **Project Structure** — File organization, naming conventions, imports
8. **Utilities and Constants** — Helper functions, configuration, constants

**Rule Application Modes:**

- **Always Apply**: Only for small, universally safe rules (rare)
- **Auto Attached**: Use globs for file-type-specific rules (e.g., `**/*.tsx` for React components)
- **Agent Requested**: Use descriptions for context-aware rules (e.g., "Map integration patterns")
- **Manual**: For specialized rules only invoked explicitly

### Step 3: Rule Creation

For each rule:

1. **Determine Application Mode**
   - Choose based on scope and usage patterns
   - Follow RULES-GUIDE-V2.md guidelines (one mode only)

2. **Set Frontmatter**

   ```markdown
   ---
   description: "Clear one-sentence purpose"
   globs: **/*.tsx,**/*.ts  # Only for Auto Attached
   alwaysApply: false  # Only true for Always mode
   ---
   ```

3. **Write Content**
   - Keep focused: 50-200 lines optimal (hard max 250 lines)
   - Be concrete: Provide examples, code snippets, patterns
   - Reference files: Use `@path/to/file` for existing code examples
   - Avoid duplication: Check existing rules first
   - Use imperative language: "Use X", "Avoid Y", "Prefer Z"

4. **Verify**
   - Glob patterns point to existing directories/files
   - File references (`@path`) point to actual files
   - No conflicts with existing rules
   - Follows naming convention (numeric prefix: `001-`, `002-`, etc.)

## Output

Creates 4-8 `.mdc` files in `.cursor/rules/` directory with:

- Proper frontmatter metadata
- Focused, actionable content
- Appropriate application mode
- File references to existing code examples
- Clear examples and patterns

## Example Usage

```bash
/generate-codebase-rules
```

The command will:

1. Analyze the codebase systematically
2. Identify key patterns and conventions
3. Generate appropriate rules following RULES-GUIDE-V2.md
4. Create rule files with proper naming and structure
5. Report which rules were created and their purposes

## Validation Checklist

Before finalizing rules, verify:

- ✅ Rules follow RULES-GUIDE-V2.md guidelines
- ✅ Optimal length: 50-200 lines (hard max 250)
- ✅ One application mode per rule (no mixing globs + description)
- ✅ Glob patterns are valid relative paths
- ✅ File references (`@path`) point to existing files
- ✅ No duplicate content with existing rules
- ✅ Numeric prefix naming (001-, 002-, etc.)
- ✅ Clear, actionable, imperative language
- ✅ Concrete examples and patterns included

## Notes

- **Read RULES-GUIDE-V2.md first** — This is the authoritative source for rule structure
- **Check existing rules** — Avoid duplicating existing guidance
- **Token awareness** — Keep rules concise to preserve context window budget
- **File references** — Use sparingly; each `@filename` consumes tokens
- **Proceed autonomously** — Make intelligent decisions about rule structure and content
