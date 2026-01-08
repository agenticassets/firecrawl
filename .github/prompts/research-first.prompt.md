---
agent: 'agent'
description: "Conduct comprehensive research and context gathering using MCP tools before proceeding with implementation. Ensures intelligent, well-informed solutions through iterative documentation search, codebase analysis, and external research."
name: "research-first"
---

# research-first

Conduct comprehensive research and context gathering using MCP tools before proceeding with implementation. Ensures intelligent, well-informed solutions through iterative documentation search, codebase analysis, and external research.

## Usage

```
/research-first [task-description]
```

## Parameters
- `task-description` (optional): Brief description of the task or problem to solve. If omitted, uses current conversation context.

## Command Process

### Step 0: Create Initial Todo List (FIRST - Before All Steps)
1. **Create initial todo list**: Use `todo_write` tool to create a structured task list with major main steps
   - **One todo item for each major step** in the research-first process:
     - Step 1: Initial Context Analysis
     - Step 2: Research and Context Gathering (Codebase Analysis, Documentation Search, Internet Research)
     - Step 3: Synthesis and Strategy Development
     - Step 4: Context Documentation
     - Step 5: Update Todo List with Implementation Tasks
     - Step 6: Implementation Execution
   - Mark the first step (Step 1: Initial Context Analysis) as `in_progress`
   - Mark all other steps as `pending`
   - This initial todo list provides structure and tracks progress through the entire research-first workflow

### Step 1: Initial Context Analysis
1. **Understand the problem**: Analyze the task description or current conversation context
2. **Identify knowledge gaps**: Determine what information is needed to proceed intelligently
3. **Map research domains**: Identify relevant areas:
   - Technical documentation (libraries, frameworks, APIs)
   - Codebase patterns and existing implementations
   - Academic literature or best practices
   - Industry standards and methodologies
   - Related solutions or case studies
4. **Update todo list**: Mark Step 1 as `completed` and Step 2 as `in_progress`

### Step 2: Research and Context Gathering

**Research process: Start with codebase analysis, then use MCP tools iteratively and comprehensively:**

#### 2a. Codebase Analysis (FIRST - Before MCP Tools)
- **Semantic codebase search**: Use `codebase_search` to find relevant implementations
  - **Understand the goal**: Search to understand what we're trying to do, what the issue is, or what we're trying to accomplish
  - Query: "How does X work?", "Where is Y implemented?", "What patterns exist for Z?", "What is the goal of this task?"
  - Search for similar patterns, functions, or approaches already in the codebase
  - Identify existing solutions, utilities, or configurations
- **Pattern discovery**: Search for:
  - Similar functionality or related features
  - Configuration patterns and settings
  - Data structures and models
  - Error handling approaches
  - Testing strategies
- **Context understanding**: Gain clear understanding of the task, goal, or issue before proceeding to external research

#### 2b. Documentation Search (MCP Tools)
- **Exa code context**: Use `get_code_context_exa` for programming-specific queries
  - Search for implementation examples, API usage patterns, SDK documentation
  - Query specific programming concepts, hooks, or features
  - Retrieve code examples and usage patterns
- **Context7 library docs**: Use `resolve-library-id` and `get-library-docs` for library-specific documentation
  - Search for relevant libraries, frameworks, or APIs mentioned in the task
  - Retrieve comprehensive documentation with appropriate token limits (5000+ for complex topics)
  - Focus on methods, patterns, and best practices

#### 2c. Internet Research (MCP Tools)
- **Exa web search**: Use `exa_web_search_exa` for comprehensive web research
  - Find current best practices and methodologies
  - Discover related solutions and implementations
  - Gather context from authoritative sources
- **Firecrawl search**: Use `firecrawl_search` for web-based research
  - Search for academic papers, technical articles, or case studies
  - Use search operators (`site:`, `intitle:`, etc.) to refine results
  - Scrape relevant pages for detailed information when needed
- **Update todo list**: After completing all research (2a, 2b, 2c), mark Step 2 as `completed` and Step 3 as `in_progress`

### Step 3: Synthesis and Strategy Development
1. **Compile findings**: Organize research results into coherent insights
2. **Identify patterns**: Recognize common approaches, best practices, and proven methods
3. **Evaluate options**: Compare different strategies and their trade-offs
4. **Select optimal approach**: Choose the most effective, elegant solution based on:
   - Alignment with project standards and conventions
   - Codebase consistency and existing patterns
   - Performance and maintainability considerations
   - Academic rigor (if applicable)
   - Reproducibility and documentation requirements
5. **Determine sufficient understanding**: Once enough research context and information has been gathered, proceed with the optimal path forward
6. **Update todo list**: Mark Step 3 as `completed` and Step 4 as `in_progress`

### Step 4: Context Documentation
1. **Summarize research**: Document key findings and insights
2. **Reference sources**: Note relevant documentation, papers, or code examples discovered
3. **Explain rationale**: Articulate why the chosen approach is optimal
4. **Note alternatives**: Briefly mention other options considered and why they were not selected
5. **Update todo list**: Mark Step 3 as `completed` and Step 4 as `in_progress`

### Step 5: Update Todo List with Implementation Tasks
1. **Update existing todo list**: Use `todo_write` tool to add additional implementation tasks to the existing todo list
   - **Add first implementation todo item (MANDATORY)**: Create and save a concise research summary markdown document (80-100 lines)
     - Summarize research findings and context gathered
     - Provide concise explanation of the optimal path forward
     - Save to appropriate location (e.g., `docs/Research-Process/[task-name]_research_summary.md` or similar)
     - Mark this first implementation todo as `in_progress`
   - **Add middle implementation todo items**: Break down the implementation into discrete, actionable steps
     - Organize tasks in logical sequence
     - Include research validation, implementation, testing, and documentation tasks
     - Mark all middle implementation tasks as `pending`
   - **Add last implementation todo item (MANDATORY)**: Update the research summary markdown document
     - Add approximately 80 more lines summarizing completion
     - Document any important information about what was accomplished
     - Note any deviations from original plan or important discoveries
     - Mark this last implementation todo as `pending`
2. **Plan implementation approach**: Outline how the optimal solution will be implemented based on research findings
3. **Update todo list**: Mark Step 4 as `completed` and Step 5 as `completed`, Step 6 as `in_progress`

### Step 6: Implementation Execution
1. **Begin with first implementation todo**: Start with the first `in_progress` implementation task (creating research summary markdown document)
2. **Complete research summary**: Write and save concise 80-100 line markdown summarizing research and optimal path
3. **Work through implementation todos**: Proceed with middle implementation todo items systematically
4. **Apply research insights**: Use gathered knowledge to inform implementation
5. **Follow discovered patterns**: Align with codebase conventions and best practices found
6. **Reference documentation**: Apply methods and strategies from authoritative sources
7. **Maintain quality standards**: Ensure implementation meets project requirements
8. **Update todo list**: Mark completed tasks and update status as work progresses (both major steps and implementation tasks)
9. **Complete final implementation todo**: Update research summary markdown with ~80 lines documenting completion and important information

## Critical Requirements

**MUST DO:**
- **Create initial todo list first**: Use `todo_write` tool to create initial todo list with major steps BEFORE starting Step 1 (MANDATORY first action)
- **Codebase analysis first**: Always start with codebase search to understand the goal, task, or issue before using MCP tools
- **Use MCP tools iteratively**: Don't stop after one search - follow up with additional queries based on initial findings
- **Search comprehensively**: Cover documentation, codebase, and external sources
- **Think deeply**: Analyze findings and synthesize insights before implementing
- **Document research**: Summarize key findings and rationale for chosen approach
- **Update todo list at Step 5**: Add implementation tasks to existing todo list (don't create new one)
- **First implementation todo: Research summary markdown**: Create and save concise 80-100 line markdown document summarizing research and optimal path (MANDATORY first implementation todo item)
- **Proceed with optimal path**: Once enough research context is gathered, proceed with the chosen optimal approach
- **Begin implementation**: Start working through the implementation todos immediately after updating todo list, beginning with research summary markdown
- **Final implementation todo: Completion summary**: Update research summary markdown with ~80 lines documenting completion and important information (MANDATORY last implementation todo item)
- **Apply insights**: Use research to inform intelligent, elegant solutions

**MCP Tool Usage Guidelines:**
- **Codebase analysis first**: Always start with codebase search to understand the goal, task, or issue before using MCP tools
- **Start broad, then narrow**: Begin with general searches, then refine based on findings
- **Cross-reference**: Use multiple tools to verify and complement information
- **Follow leads**: If one search reveals relevant concepts, search for those too
- **Use appropriate depth**: Request sufficient token limits (5000+) for complex topics
- **Understand context before external research**: Gain clear understanding of codebase patterns and goals before searching external documentation

## Deliverables

### Research Summary Markdown Document
- **Location**: Saved to appropriate location (e.g., `docs/Research-Process/[task-name]_research_summary.md`)
- **Initial version (80-100 lines)**: Created as first todo item
  - Summary of research findings and context gathered
  - Concise explanation of optimal path forward
  - Key insights from documentation, codebase, and external research
- **Final version (+~80 lines)**: Updated as last todo item
  - Completion summary and important information about what was accomplished
  - Any deviations from original plan or important discoveries
  - Final status and outcomes

### Research Summary
- **Key findings**: Important insights from documentation, codebase, and external research
- **Relevant sources**: Documentation links, papers, or code examples discovered
- **Pattern analysis**: Existing codebase patterns and how they inform the solution
- **Strategy rationale**: Explanation of chosen approach and why it's optimal

### Implementation
- **Informed solution**: Code or analysis that reflects comprehensive research
- **Consistent patterns**: Aligns with codebase conventions and discovered best practices
- **Quality standards**: Meets project requirements for documentation, testing, and reproducibility

## Quality Assurance

Validate research process:
- [ ] Initial todo list created first (Step 0) with major steps before starting Step 1
- [ ] Codebase analysis conducted first to understand goal, task, or issue
- [ ] Multiple MCP tools used (documentation + internet + codebase)
- [ ] Iterative searches conducted (not just single queries)
- [ ] Codebase patterns identified and analyzed
- [ ] External best practices researched
- [ ] Findings synthesized into coherent strategy
- [ ] Rationale clearly documented
- [ ] Todo list updated at Step 5 with implementation tasks (not created new)
- [ ] Research summary markdown document created as first implementation todo (80-100 lines)
- [ ] Research summary markdown updated as final implementation todo (+~80 lines with completion info)
- [ ] Implementation reflects research insights

## Usage Examples

```bash
# Research before implementing a new feature
/research-first Implement conformal prediction intervals for XGBoost model

# Research before refactoring
/research-first Refactor assessment error analysis to use streaming approach

# Research before adding new dependency
/research-first Add SHAP interventional values with balanced background sampling

# Use current context
/research-first
```

## Integration with Project Standards

When researching, prioritize:
- **Project conventions**: Code structure, naming patterns, configuration management
- **Academic rigor**: Methodological soundness, reproducibility, documentation
- **Performance**: Memory efficiency, computational optimization for large datasets
- **Maintainability**: Clear code, proper error handling, comprehensive logging

Conduct comprehensive research using MCP tools to gather context from documentation, codebase, and external sources before proceeding with implementation. Ensures intelligent, well-informed solutions that align with project standards and best practices.
