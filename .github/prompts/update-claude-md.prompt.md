---
agent: 'agent'
description: "Ensure CLAUDE.md files are comprehensive and provide effective context for Claude Code sessions."
name: "update-claude-md"
---

# update-claude-md

Ensure CLAUDE.md files are comprehensive and provide effective context for Claude Code sessions.

## Usage
```
/update-claude-md
```

## What it does
1. **Audit Documentation**: Review CLAUDE.md files for completeness and accuracy
2. **Sync with Codebase**: Update technical details to match current implementation
3. **Add Context**: Include recent patterns, methodologies, and optimizations
4. **Optimize for Research**: Structure for effective academic research workflows

## Files updated
- Project CLAUDE.md (core instructions and architecture)
- Global ~/.claude/CLAUDE.md (development preferences)
- Command documentation

## Key areas reviewed
- **Make commands**: `make process_data`, `make analyze`, `make pipeline`
- **Data processing**: CRSP pipeline, price efficiency calculations, checkpointing
- **Path management**: Auto-detection via setup.py, TEST_MODE environment variable
- **Statistical methods**: Staggered DiD, cross-autocorrelation measures, panel regressions
- **Code standards**: Black formatting, logging patterns, academic writing guidelines

## Example improvements
```markdown
## Recent Updates
- Updated Sun & Abraham regression specifications in 3---Tables and Figures_Updated.do
- Revised econometric model section in Main.tex (lines 184-187)
- Generated Sun & Abraham event study tables via Table_XX_SunAbraham_EventStudy_*.tex
- Added staggered DiD figures to Results/Figure_Files/ directory

## File Management
- Consolidated Stata results in Results/Table_Files/ with proper esttab formatting
- Updated Results.tex to include latest panel regression outputs
- Maintained LaTeX bibliography with JFE style (References/jfe)
```

## Validation
- Verify command examples work as documented
- Check file paths match current implementation
- Test new context improves Claude effectiveness
