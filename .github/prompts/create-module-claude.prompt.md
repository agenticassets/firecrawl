---
agent: 'agent'
description: "Generate ultra-lean, module-specific CLAUDE.md for designated folder with domain context and local patterns."
name: "create-module-claude"
---

# create-module-claude

Generate ultra-lean, module-specific CLAUDE.md for designated folder with domain context and local patterns.

## Usage

```bash
/create-module-claude "<folder-path>" [domain-context|condense]
```

## Parameters
- `folder-path` (required): Target directory path for module-specific CLAUDE.md generation.
- `mode` (optional): Operation mode - "domain-context" (generate specialized documentation) or "condense" (create compact 20-40 line version). Defaults to "domain-context".

## Procedure
1. **Parse inputs and validate**: Confirm folder exists and determine operation mode.
2. **Analyze module context**: Extract domain purpose, local patterns, and integration points from target folder.
3. **Identify module boundaries**: Determine what the folder owns versus delegates to other modules.
4. **Extract domain-specific elements**:
   - **Domain purpose**: Single most important rule for this module
   - **Local patterns**: Naming conventions unique to this folder
   - **Integration points**: How this connects to other modules
   - **Module boundaries**: Ownership and delegation responsibilities
5. **Apply mode-specific formatting**:
   - **domain-context**: Generate specialized documentation with module essentials
   - **condense**: Create compact version (20-40 lines) preserving critical boundaries
6. **Assemble documentation**: Use standardized template structure with flat bullet lists.
7. **Write to disk**: Save as CLAUDE.md within target folder, avoiding duplication of root content.

## Deliverables

- **Module CLAUDE.md**: Ultra-lean documentation file (20-40 lines) with folder-specific essentials only.
- **Console summary**: Brief report of folder analyzed, sections generated, and line count.
- **Mode-specific outputs**: Domain analysis report or condensed version as appropriate.

## Validation
- **Length control**: Target 20-40 lines maximum (ultra-lean, avoid diluting context).
- **Content scope**: Include only essentials unique to this folder - never repeat root content.
- **Structure compliance**: Verify sections follow module-specific sequencing and naming conventions.
- **Inheritance awareness**: Ensure root rules are referenced but not duplicated.
- **Freshness validation**: Confirm documentation reflects current folder state and patterns.
- **Integration verification**: Validate module boundaries and connection points are accurately documented.
