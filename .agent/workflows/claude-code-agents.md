---
description: "Manage, create, and audit specialized Claude Code subagents to ensure peak performance and codebase alignment."
---

# claude-code-agents

Manage, create, and audit specialized Claude Code subagents to ensure peak performance and codebase alignment.

## Prerequisites
**MANDATORY**: 
1. **Rule Discovery (FIRST STEP)**: Search and review any **Cursor Rules** (@.cursor/rules/*.mdc) that are related to the agent's domain or mission to ensure alignment with project-specific standards.
2. Always read and adhere to the standards in @.claude/subagents-guide.md before beginning any agent creation or review task.

## Primary Objective
Act as a Senior AI Orchestrator to either generate a new specialized subagent or perform a deep architectural audit of an existing one. You are expected to **directly edit the files** in the codebase to implement your findings or creations.

## Mode Detection
1. **Agent Review Mode**: Triggered if the user includes a file from `.claude/agents/`.
2. **Agent Creation Mode**: Triggered if no existing agent file is provided.

## Workflow: Agent Creation
If no agent file is provided:
- **Rule & Requirement Analysis (FIRST)**: 
  - Analyze the user's request to define the agent's "Mission."
  - **Look at all related Cursor Rules** (@.cursor/rules/*.mdc) that provide domain-specific constraints or instructions for the mission.
- **Codebase Context**: Search the repo to identify:
  - Relevant directories and files.
  - Technical standards and architectural patterns.
- **Spec Generation**: Propose a new agent file including:
  - **YAML Frontmatter**: Precise `name`, `model` (default sonnet), and a highly specific `description` starting with "Use when..." for optimal auto-delegation.
  - **System Prompt**: Follow the structure: **Role**, **Mission**, **Constraints**, **Method** (step-by-step), and **Output Format**.
  - **Tool Gating**: Restrict to only the tools necessary for the mission.

## Workflow: Agent Review
If an agent file is provided:
- **Rule Alignment (FIRST)**: Search and review any **Cursor Rules** (@.cursor/rules/*.mdc) that apply to the agent's specific domain (e.g., UI, Auth, DB) to establish the current architectural baseline.
- **Description Audit**: Verify the `description` is specific enough for auto-delegation.
- **Technical Verification**: Check all file paths and architectural claims (e.g., "Use Drizzle for DB") against the actual codebase and the discovered Cursor Rules.
- **Prompt Optimization**:
  - Ensure the mission is clear and focused.
  - Check for "ample context but not too much"—move large static details to referenced documentation files or Cursor rules rather than embedding them.
  - Verify the **Method** section provides actionable, step-by-step tool usage instructions.
- **Model Check**: Ensure the selected `model` matches the complexity of the task. Most agents should use `haiku`. reserve `sonnet` only for agents handling key architectural components or complex, mission-critical logic.

## Quality Standards
- **Model Selection**: Default to `haiku`. Only use `sonnet` for subagents handling key architectural parts or mission-critical code transformations.
- **Length**: Aim for 100-200 lines for the total agent definition. This ensures enough context without causing excessive token overhead or dilution of focus.
- **DRY**: Don't repeat instructions that are already in root rules unless mission-critical.
- **Focus**: Subagents should have a single, clear responsibility.
- **Safety**: Ensure instructions include guardrails against anti-patterns (e.g., "NEVER use npm").

## Output Requirements
- **Direct Action**: Do not just propose changes; **actually edit the files** in `.claude/agents/` using the appropriate tools.
- **Creation**: Write the complete markdown content for the new agent file in `.claude/agents/`.
- **Review**: Provide a detailed "Audit Report" followed by the implementation of the "Refined Agent File."
- **Registry Update**: After creating or significantly modifying an agent, you **MUST** update @CLAUDE_AGENTS.md to keep the Quick Reference Table and Agent Details in sync.
