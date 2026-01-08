---
agent: 'agent'
description: "**Research-first task execution** — Understand the request and codebase specifications, gather version-compatible context through sequential tool calls, analyze findings, then execute the requested changes or edits."
name: "mcp-search-and-think"
---

# mcp-search-and-think

**Research-first task execution** — Understand the request and codebase specifications, gather version-compatible context through sequential tool calls, analyze findings, then execute the requested changes or edits.

## Process Flow

### Step 1: Understand the Task
Analyze the request to identify what needs to be done, what files/components are involved, and what context is needed.

### Step 1.5: Understand Codebase Specifications (Before Searching)
**CRITICAL**: Before any searches, read configuration files to understand codebase specs and dependencies:
- `package.json` — Framework versions, library dependencies, package manager
- `tsconfig.json` — TypeScript configuration and compiler options
- `next.config.js` / `next.config.ts` — Next.js configuration
- `.cursor/rules/` or project docs — Architecture patterns and conventions
- Other relevant config files (tailwind.config, eslint config, etc.)

**Note**: Use this information to filter and prioritize search results — only use code/docs compatible with your codebase versions and specs.

### Step 2: Local Codebase Exploration (Recommended First)
Use **local tools** to understand the codebase context:
- `codebase_search` — Semantic search for patterns, implementations, architecture
- `grep` — Find specific functions, types, imports, or patterns
- `read_file` — Read relevant files, configs, or documentation

**Purpose**: Understand what exists, how it's structured, and what patterns are used.

### Step 3: MCP Code Documentation & Examples (Recommended Second)
Use **MCP tools** for code examples and library documentation:
- `mcp_exa_get_code_context_exa` — Search code examples and API patterns (specify versions from Step 1.5)
- `mcp_Context7_get-library-docs` — Get library/framework documentation (use exact versions from package.json)
- **shadcn MCP tools** — Component documentation and examples (if working with shadcn/ui)
- **prompt-kit MCP tools** — Prompt library documentation and patterns (if applicable)
- **Other library-specific MCP tools** — Use when relevant to the task

**Purpose**: Learn best practices, API usage, and implementation patterns.

**Critical**: When searching for code examples or documentation:
- Specify exact framework/library versions from Step 1.5 (e.g., "Next.js 16", "React 19", "AI SDK 5")
- Filter results to match your codebase versions and TypeScript configuration
- Only use code examples compatible with your dependency versions
- Verify API patterns match your installed library versions

**Note**: Use library-specific MCP tools (shadcn, prompt-kit, etc.) only when applicable to the task.

### Step 4: Web/Internet Search (Recommended Third)
Use **web search tools** for broader context and solutions:
- `mcp_exa_web_search_exa` — Web search for best practices, solutions, or approaches (include version info from Step 1.5)
- `mcp_firecrawl-mcp_firecrawl_search` — Search and scrape relevant content

**Purpose**: Discover industry standards, alternative approaches, or external solutions.

**Note**: When searching, include framework/library versions from Step 1.5 to find compatible solutions (e.g., "Next.js 16 React 19", "AI SDK 5 patterns").

**Note**: Steps 2-4 are **recommended sequential order** but flexible — adapt based on task needs. Some tasks may not require all steps.

### Step 5: Analysis & Thinking
After initial searches:
- **Analyze findings**: What did you learn? What patterns exist?
- **Identify gaps**: What additional information is needed?
- **Decide**: Can you proceed, or do you need more context?

### Step 6: Additional Research (Optional, 1-2 More Searches)
If needed, perform **1-2 additional searches** from any tool category:
- Fill knowledge gaps identified in Step 5
- Verify assumptions or check edge cases
- Research specific implementation details

**Stop condition**: Proceed when you have sufficient context to execute confidently.

### Step 7: Execute Task
With context gathered:
- **Make the requested changes** — Implement edits, revisions, or new code
- **Follow project patterns** — Use existing conventions and architecture
- **Apply best practices** — Based on research findings
- **Verify completeness** — Ensure the task is fully addressed

## Usage Examples

```
/mcp-search-and-think Add error handling to the chat API route

/mcp-search-and-think Refactor the message component to use CSS variables

/mcp-search-and-think Update the authentication middleware to support guest users

/mcp-search-and-think Fix the streaming response issue in the chat endpoint
```

## Tool Selection Guidelines

**Recommended sequential flow**: Local tools → MCP code/docs → Web search

| Task Type | Step 2 (Local) | Step 3 (MCP) | Step 4 (Web) | Additional (if needed) |
|-----------|----------------|---------------|--------------|------------------------|
| Code changes | `codebase_search` + `grep` | `mcp_exa_get_code_context_exa` | Skip or `mcp_exa_web_search_exa` | `read_file` for specific files |
| Feature addition | `codebase_search` | `mcp_exa_get_code_context_exa` + library MCPs (if applicable) | `mcp_exa_web_search_exa` | `mcp_Context7_get-library-docs` |
| UI/Component work | `codebase_search` + `grep` | **shadcn MCP** + `mcp_exa_get_code_context_exa` | Skip or `mcp_exa_web_search_exa` | Component-specific docs |
| Bug fix | `grep` + `codebase_search` | Skip or `mcp_exa_get_code_context_exa` | `mcp_exa_web_search_exa` | Additional codebase search |
| Documentation | `codebase_search` + `read_file` | `mcp_Context7_get-library-docs` + library MCPs | Skip | Additional file reads |
| Architecture | `codebase_search` | `mcp_exa_get_code_context_exa` | `mcp_exa_web_search_exa` | `mcp_firecrawl-mcp_firecrawl_search` |

## Quality Standards

- **Version compatibility**: Always verify code examples and documentation match your codebase versions (from Step 1.5)
- **Research depth**: Gather enough context to make informed decisions
- **Efficiency**: Don't over-search — 2-4 total searches should suffice
- **Action-oriented**: Research serves execution, not endless exploration
- **Pattern matching**: Use existing codebase patterns when possible
- **Best practices**: Apply industry standards discovered through research, filtered for your versions

## Output

After research and execution:
- **Summary**: Brief explanation of what was researched and why
- **Changes**: Clear description of modifications made
- **Rationale**: Why this approach was chosen based on research
