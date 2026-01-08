---
description: "Review, validate, and refresh existing Cursor AI slash commands to ensure accuracy, completeness, and adherence to project standards."
---

# review-command

Review, validate, and refresh existing Cursor AI slash commands to ensure accuracy, completeness, and adherence to project standards.

## Command Review Process

### Step 1: Command Identification
Locate and analyze the target command:
- **File location**: Identify the specific `.md` command file in `.cursor/commands/`
- **Current content**: Extract and parse the existing command structure
- **Version tracking**: Note creation date and any recent modifications
- **Usage patterns**: Check for references in project documentation or workflows

### Step 2: Structural Validation
Verify command architecture meets markdown standards:
- **Title format**: Single H1 heading matching command name (e.g., `# review-command`)
- **Description**: Brief one-line summary directly after title
- **Section organization**: Logical flow with appropriate H2/H3 headers
- **Content structure**: Clear process steps, deliverables, and usage examples
- **Formatting consistency**: Proper markdown syntax and readability

### Step 3: Content Accuracy Assessment
Review command content for:
- **Technical accuracy**: Verify all instructions, paths, and file references are current
- **Project alignment**: Ensure compliance with workspace conventions and file structure
- **Clarity assessment**: Evaluate instruction clarity and actionability
- **Completeness check**: Confirm all necessary process steps are present

### Step 4: Content Refinement
Apply best practices:
- **Conciseness**: Remove redundant or unnecessary content
- **Specificity**: Replace vague instructions with concrete, actionable steps
- **Examples**: Ensure usage examples are relevant and demonstrate actual use cases
- **Anti-pattern correction**: Remove any identified problematic patterns

## Deliverable Requirements
Produce an updated command file that:
- **Maintains focus**: No scope creep or unnecessary additions
- **Improves accuracy**: Corrects outdated paths, references, or instructions
- **Enhances clarity**: Refines wording for better understanding
- **Preserves functionality**: Maintains all original command capabilities
- **Follows conventions**: Adheres to project markdown and documentation standards

## Quality Assurance
Validate the updated command through:
- **Syntax check**: Verify proper markdown formatting
- **Functionality test**: Ensure command executes as intended when invoked
- **Integration check**: Confirm compatibility with existing workflows
- **Documentation sync**: Update any references in CLAUDE.md or README files

## Usage Examples
- `/review-command create-command` - Review and update the create-command slash command
- `/review-command data-analysis` - Validate data analysis command accuracy
- `/review-command latex-compile` - Refresh LaTeX compilation command

Review and update slash commands to maintain accuracy and project standards compliance.
