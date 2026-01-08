---
agent: 'agent'
description: "Create/update Plan.md with structured project planning. Discovery-first approach with accurate file references, status tracking, and risk assessment."
name: "plan"
---

# plan

Create/update Plan.md with structured project planning. Discovery-first approach with accurate file references, status tracking, and risk assessment.

Create/update Plan.md for $ARGUMENTS with structured project planning:

## Core Actions

1. **Discovery phase**: Search and analyze existing codebase, configs, and patterns
2. **Objective definition**: Clear, measurable goals with success criteria
3. **Architecture decisions**: Document choices with rationales and alternatives
4. **Phase breakdown**: Implementation plan with status tracking
5. **Risk assessment**: Blockers, impacts, and mitigation strategies
6. **Progress metrics**: Quantifiable measurements and completion tracking
7. **Standup integration**: Daily progress logs and blocker identification

## Information Accuracy Rules

- **Use exact file paths**: Reference actual files found in codebase (e.g., src/components/Button.tsx:42)
- **Never fabricate**: If information isn't available, mark as "TO INVESTIGATE" in plan
- **Search first**: Include discovery tasks to find existing patterns, dependencies, configs
- **Verify references**: Ensure all file paths, line numbers, and code examples exist
- **Document unknowns**: Be explicit about what needs to be researched or discovered

## Plan.md Template Structure

```markdown
# Project: [Feature Name]
Generated: YYYY-MM-DD
Status: [IN_PROGRESS|BLOCKED|COMPLETE]
Assignee: Claude + [Developer]

## 🎯 Objective
[Clear, measurable goal]

## 📋 Success Criteria
- [ ] Performance metrics met
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Security review completed

## 🏗️ Architecture Decisions
| Decision | Rationale | Alternative |
|----------|-----------|-------------|

## 📝 Implementation Plan

### Phase 0: Discovery [PENDING]
- [ ] Search existing codebase for similar patterns
- [ ] Identify relevant files and dependencies  
- [ ] Document current architecture constraints
- [ ] Map integration points with existing systems

### Phase 1: Foundation [Status]
### Phase 2: Implementation [Status] 
### Phase 3: Integration & Polish [Status]

## 🚧 Blockers & Risks
| Issue | Impact | Mitigation | Status |

## 📊 Progress Metrics
- Completion: X%
- Test Coverage: X%
- Performance Score: X/100

## 🔄 Daily Standup Log
### YYYY-MM-DD
- Completed: 
- Today:
- Blockers:
```

## Smart Features

- **Discovery-first**: Always start with search/analysis phase before implementation
- **Accurate references**: All file paths, line numbers verified against actual codebase
- **Status tracking**: Visual progress indicators and phase management
- **Decision archaeology**: Extract rationales from git history and discussions
- **Blocker management**: Impact assessment and mitigation planning
- **Metric integration**: Tie to actual codebase measurements
- **Honest unknowns**: Mark uncertain information as "TO INVESTIGATE" rather than guess
- **Standup automation**: Daily progress capture for team sync
- **Context linking**: Reference related CLAUDE.md sections

## Example Discovery Tasks

```markdown
### Phase 0: Discovery [IN_PROGRESS]
- [ ] Find existing authentication patterns (searching /src/auth/*)
- [ ] Locate test setup files (TO INVESTIGATE: jest.config.js vs vitest.config.ts)
- [ ] Identify current state management (searching for zustand/redux imports)
- [ ] Map API structure (TO INVESTIGATE: /api routes vs tRPC procedures)
```

Output: Accurate Plan.md with verified references and honest knowledge gaps
