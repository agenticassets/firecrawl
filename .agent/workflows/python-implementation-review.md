---
description: "Review Python code for implementation completeness, ensuring no placeholder code, hard-coded data points, or incomplete implementations remain."
---

# python-implementation-review

Review Python code for implementation completeness, ensuring no placeholder code, hard-coded data points, or incomplete implementations remain.

## Overview

This command performs a targeted review of Python code to verify complete implementation without placeholders, stubs, or hard-coded values that should be dynamic or configurable.

## Step 1: Placeholder Code Detection

Identify and catalog placeholder implementations:

- **TODO comments**: Search for `TODO`, `FIXME`, `HACK`, or similar markers
- **Pass statements**: Find `pass` statements used as temporary fillers
- **Stub functions**: Identify functions with minimal or dummy implementations
- **Empty methods**: Locate methods with no implementation body
- **NotImplementedError**: Find intentional placeholders for future implementation

## Step 2: Hard-Coded Data Identification

Locate and document hard-coded values that should be dynamic:

- **Magic numbers**: Numeric literals that should be constants or configuration
- **Hard-coded strings**: String literals used for configuration or data paths
- **Fixed file paths**: Absolute paths that should be configurable
- **Static variables**: Variables with hard-coded values instead of dynamic assignment
- **Configuration values**: Settings embedded directly in code instead of external config

## Step 3: Implementation Completeness Verification

Ensure all code components are fully implemented:

- **Function completeness**: Verify all functions have complete logic implementation
- **Class method coverage**: Check that all class methods are implemented
- **Error handling**: Confirm proper exception handling and edge cases
- **Return values**: Ensure functions return appropriate values or None when expected
- **Documentation**: Verify docstrings and comments reflect actual implementation
- **Code quality standards**: Never include emojis in Python code - they can cause execution errors across different environments and platforms

## Step 4: Dynamic Configuration Assessment

Review code for proper configuration management:

- **Configuration imports**: Check for proper config file usage
- **Environment variables**: Verify environment-based configuration
- **Parameter validation**: Ensure input parameters are validated and used
- **Settings management**: Confirm configuration is centralized and accessible

## Focus Areas

- **Production readiness**: Eliminate all placeholder and stub code
- **Configuration flexibility**: Remove hard-coded values that limit adaptability
- **Code maintainability**: Ensure implementations are complete and functional
- **Documentation accuracy**: Verify documentation matches actual implementation

## Quick Wins

1. **Critical placeholders**: Remove `pass` statements and `TODO` comments in active code paths
2. **Hard-coded paths**: Extract file paths and URLs to configuration variables
3. **Magic numbers**: Replace numeric literals with named constants
4. **Incomplete functions**: Implement missing function logic or mark for removal

## Deliverables

- **Placeholder inventory**: Complete list of all placeholder code found
- **Hard-coded values report**: Catalog of all hard-coded data points identified
- **Completeness assessment**: Evaluation of overall implementation completeness
- **Refactoring recommendations**: Specific suggestions for addressing identified issues

Review Python code implementation completeness to ensure production-ready, maintainable code without placeholders or hard-coded values.
