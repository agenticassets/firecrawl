---
agent: 'agent'
description: "Comprehensive validation command for research project progress documentation. Systematically verifies that all claims, implementations, and deliverables described in a progress/todo file actually exist and function as stated."
name: "verify-progress"
---

# verify-progress

Comprehensive validation command for research project progress documentation. Systematically verifies that all claims, implementations, and deliverables described in a progress/todo file actually exist and function as stated.

## Purpose & Methodology

This command performs rigorous academic validation of project documentation by:
1. **Parsing Documentation Claims**: Extracts specific assertions about implementations, outputs, and achievements
2. **Codebase Verification**: Confirms that described code implementations exist and function correctly
3. **Artifact Validation**: Verifies that all mentioned output files, tables, and datasets actually exist
4. **Success Metric Confirmation**: Validates that claimed success rates, sample sizes, and performance metrics are accurate
5. **Cross-Consistency Checking**: Identifies any inconsistencies, errors, or incomplete implementations

## Validation Process

### Step 1: Documentation Analysis
- Parse the progress file to identify specific claims and assertions
- Extract references to code files, data files, output artifacts, and success metrics
- Build validation checklist from documented achievements and deliverables

### Step 2: Implementation Verification
- **Code Files**: Confirm existence, check line numbers, verify implementations match descriptions
- **Data Files**: Validate file existence, sizes, modification dates, and content structure
- **Output Artifacts**: Verify tables, figures, and datasets contain expected content and formatting

### Step 3: Success Metric Validation
- Check that claimed sample sizes, match rates, and performance metrics are achieved
- Verify statistical results match documented findings
- Confirm data quality metrics and integration success rates

### Step 4: Error Detection & Reporting
- Identify discrepancies between documentation and actual implementation
- Flag missing files, incorrect claims, or incomplete implementations
- Provide actionable recommendations for any issues found

## Output Format

### Validation Report Structure
```
# Project Progress Validation Report

## 📋 Summary Assessment
[OVERALL ACCURACY RATING] - Brief assessment of documentation accuracy

## ✅ Verified Implementations
- Phase 1: [STATUS] - [Key findings]
- Phase 2: [STATUS] - [Key findings]
- Phase N: [STATUS] - [Key findings]

## 🔍 Detailed Validation Results
### Phase 1: [Phase Name]
**Code Implementation:**
- ✅ [Specific verification]
- ✅ [Specific verification]

**Output Artifacts:**
- ✅ [File verification]
- ✅ [Content verification]

**Success Metrics:**
- ✅ [Metric validation]

### Issues Identified
[If any issues found, document with specific details and recommendations]

## 🎯 Recommendations
[Actionable next steps based on validation findings]
```

## Usage Examples

### Basic Progress Verification
```
/verify-progress "Plan.md"
```
Validates all claims in the main project plan.

### Phase-Specific Validation
```
/verify-progress "Results/Phase_3_Implementation.md"
```
Validates specific phase documentation.

### Multi-Document Validation
```
/verify-progress "Plan.md"
```
/verify-progress "Results/Implementation_Details.md"
```
Sequential validation of multiple documentation files.

## Quality Standards

### Academic Rigor
- Systematic, reproducible validation methodology
- Evidence-based findings with specific file and line references
- Quantitative assessment of claim accuracy rates

### Documentation Standards
- Clear validation criteria and success metrics
- Comprehensive artifact inventory with file sizes and modification dates
- Actionable recommendations for any discrepancies found

### Error Handling
- Graceful handling of missing files or incomplete implementations
- Clear distinction between documentation errors and implementation issues
- Specific guidance for resolving identified problems

## Integration Notes

This command integrates with existing Cursor AI workflow by:
- Reading progress documentation files in the current workspace
- Automatically validating against actual project structure and files
- Providing validation reports suitable for academic documentation
- Supporting iterative development and quality assurance processes
