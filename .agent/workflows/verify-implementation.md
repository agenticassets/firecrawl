---
description: "Comprehensive verification command for validating newly implemented features or fixes. Systematically understands the codebase architecture, dependencies, and patterns before verifying that implementations match documentation and function correctly without errors."
---

# verify-implementation

Comprehensive verification command for validating newly implemented features or fixes. Systematically understands the codebase architecture, dependencies, and patterns before verifying that implementations match documentation and function correctly without errors.

## Purpose & Methodology

This command performs rigorous validation of implementations by:
1. **Codebase Understanding**: Deep analysis of project structure, dependencies, code types, and architectural patterns
2. **Documentation Analysis**: Parsing provided documentation to extract implementation requirements and expected behaviors
3. **Implementation Verification**: Confirming code matches documentation and follows established patterns
4. **Error Detection**: Identifying linting errors, type errors, runtime issues, and architectural inconsistencies
5. **Quality Assurance**: Validating code quality, performance, and integration with existing systems

## Critical Prerequisites

**BEFORE beginning verification, you MUST:**

### Step 1: Understand Codebase Architecture
- **Project Structure**: Analyze directory organization, file naming conventions, and module boundaries
- **Technology Stack**: Identify all frameworks, libraries, and tools in use (Next.js version, React version, database systems, etc.)
- **Dependencies**: Review `package.json` to understand all dependencies and their versions
- **Code Types**: Identify what types of code exist (Server Components, Client Components, API routes, Server Actions, database queries, etc.)
- **Architectural Patterns**: Understand established patterns (routing, data fetching, state management, authentication, etc.)
- **Integration Points**: Map how different systems connect (database → API → UI, auth flows, etc.)

### Step 2: Understand Domain Context
- **Business Logic**: Understand what the feature/fix is supposed to accomplish
- **User Flows**: Identify how users interact with the implementation
- **Data Models**: Understand relevant database schemas and data structures
- **API Contracts**: Review API endpoints, request/response formats, and error handling

### Step 3: Review Related Documentation
- **CLAUDE.md files**: Check domain-specific documentation in relevant directories
- **Cursor Rules**: Review relevant `.cursor/rules/` files for coding standards
- **Existing Patterns**: Find similar implementations to understand conventions

## Verification Process

### Phase 1: Codebase Analysis (MANDATORY FIRST STEP)
- **Project Structure Discovery**: Map all relevant directories and their purposes
- **Dependency Analysis**: Identify all packages, versions, and their roles
- **Pattern Recognition**: Document established coding patterns and conventions
- **Architecture Mapping**: Understand how components, routes, and services interact
- **Configuration Review**: Check build configs, environment variables, and tooling setup

### Phase 2: Documentation Parsing
- **Requirement Extraction**: Parse provided documentation to identify what was implemented
- **Expected Behavior**: Extract functional requirements and success criteria
- **Scope Definition**: Identify which files, components, or systems should be affected
- **Integration Points**: Note any dependencies on other features or systems

### Phase 3: Implementation Verification
- **File Existence**: Confirm all mentioned files exist at specified locations
- **Code Structure**: Verify code organization matches project conventions
- **Pattern Compliance**: Ensure implementation follows established patterns
- **Functionality Match**: Confirm code behavior matches documentation claims
- **Integration Validation**: Verify proper integration with existing systems

### Phase 4: Error Detection & Quality Checks
- **Type Errors**: Run TypeScript type checking and identify any type mismatches
- **Linting Issues**: Check for ESLint errors, warnings, and code quality issues
- **Runtime Errors**: Identify potential runtime issues, null checks, error handling gaps
- **Performance Issues**: Flag potential performance problems (N+1 queries, missing memoization, etc.)
- **Security Concerns**: Check for common security issues (XSS, injection, auth bypass, etc.)

### Phase 5: Integration Testing
- **Import Validation**: Verify all imports resolve correctly
- **Dependency Check**: Confirm all required dependencies are installed
- **Build Verification**: Check if code compiles without errors
- **Route Testing**: Verify API routes and pages load correctly
- **Database Validation**: Check migrations, queries, and schema changes

## Output Format

### Verification Report Structure
```
# Implementation Verification Report

## 📋 Codebase Understanding Summary
**Project Structure**: [Brief overview of architecture]
**Key Dependencies**: [Critical packages and versions]
**Code Types Identified**: [Server Components, Client Components, API routes, etc.]
**Architectural Patterns**: [Established patterns found]

## 📖 Documentation Analysis
**Implementation Scope**: [What was documented to be implemented/fixed]
**Expected Behavior**: [Key functional requirements]
**Affected Systems**: [Components, routes, databases touched]

## ✅ Verification Results

### Implementation Verification
- ✅ [Specific verification point]
- ✅ [File/component verified]
- ⚠️ [Warning or concern]
- ❌ [Issue found]

### Code Quality Checks
- ✅ [Type checking results]
- ✅ [Linting results]
- ⚠️ [Code quality warnings]
- ❌ [Errors found]

### Integration Validation
- ✅ [Integration point verified]
- ✅ [Dependencies resolved]
- ❌ [Integration issue]

## 🔍 Issues Identified
[Detailed list of any problems found with specific file references and line numbers]

## 🎯 Recommendations
[Actionable steps to resolve issues or improve implementation]
```

## Usage Examples

### Basic Implementation Verification
```
/verify-implementation "Fixed iOS chat submission issue by adding ID generation fallback in chat.tsx"
```
Verifies the iOS fix matches the description and works correctly.

### Feature Implementation Verification
```
/verify-implementation "Added new Projects feature with database migrations, API routes, and UI components"
```
Comprehensive verification of a complete feature implementation.

### Post-Plan Verification
```
/verify-implementation [paste plan.md content or summary]
```
Validates that implementation matches the plan documentation.

## Quality Standards

### Understanding First
- **Never skip codebase analysis**: Always understand architecture before verification
- **Pattern recognition**: Identify and follow established patterns, don't introduce new ones
- **Dependency awareness**: Know what packages are available and their capabilities
- **Context matters**: Understand the "why" behind implementations, not just the "what"

### Verification Rigor
- **Evidence-based**: All findings must reference specific files and line numbers
- **Comprehensive**: Check all aspects (types, linting, runtime, integration)
- **Actionable**: Provide clear, specific recommendations for any issues found
- **Honest assessment**: Report what works, what doesn't, and what needs investigation

### Error Handling
- **Graceful degradation**: Handle missing files or incomplete implementations gracefully
- **Clear reporting**: Distinguish between critical errors and minor warnings
- **Prioritization**: Focus on blocking issues first, then code quality improvements

## Integration Notes

This command integrates with existing Cursor AI workflow by:
- **Post-Implementation**: Use after completing features or fixes to validate correctness
- **Post-Plan**: Use after plan.md execution to verify all plan items were implemented correctly
- **Quality Gate**: Acts as a quality checkpoint before committing or deploying
- **Documentation Validation**: Ensures implementations match their documentation

## Critical Success Factors

1. **Codebase Understanding**: Deep knowledge of project structure prevents false positives
2. **Pattern Recognition**: Understanding conventions ensures proper validation
3. **Comprehensive Checking**: Multiple verification layers catch different types of issues
4. **Clear Reporting**: Actionable feedback enables quick resolution of problems
