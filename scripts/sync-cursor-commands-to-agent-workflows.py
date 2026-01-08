#!/usr/bin/env python3
"""Sync .cursor/commands/*.md -> .agent/workflows/*.md and .github/prompts/*.prompt.md.

Default behavior:
- Reads Cursor commands.
- Extracts description from the first non-empty line after the title.
- Adds Antigravity frontmatter for .agent/workflows.
- Adds VS Code prompt frontmatter for .github/prompts.
"""

from __future__ import annotations

import argparse
from enum import Enum
from pathlib import Path


class SyncTarget(str, Enum):
    """Target for command syncing."""

    AGENT = "agent"
    VSCODE = "vscode"


def extract_description(content: str) -> tuple[str, str]:
    """Extract description and body from Cursor command content.

    Args:
        content: Full content of Cursor command file

    Returns:
        Tuple of (description, body)
    """
    lines = content.splitlines()
    body_lines = []
    description = ""
    found_title = False
    found_description_line = False

    for line in lines:
        stripped = line.strip()
        
        # Skip title line usually starting with #
        if not found_title and stripped.startswith("#"):
            found_title = True
            # We assume the content also starts with this header, so we keep it in body? 
            # The user example showed:
            # ---
            # description: test
            # ---
            # 
            # test
            #
            # The original "test" might have been the content.
            # Usually workflows are markdown files.
            # Let's keep the title in the body to be safe, or should we?
            # If I look at the user request:
            # "write another code... that willl sync my cursor commands... to this fodler... they eed this header format"
            #
            # Let's include everything in the body, but parse the description separately.
            body_lines.append(line)
            continue

        if not found_description_line and stripped:
            # First non-empty line after title is description
            # Clean up bolding markdown if present at start
            desc_text = stripped
            # Heuristic: if it looks like "**Title** - Description", try to get the whole thing or clean it.
            # For now, just take the raw text but maybe strip wrapping ** if it's the whole line.
            
            # Remove leading/trailing quotes if any
            desc_text = desc_text.strip("'").strip('"')
            
            # Attempt to clean up common markdown bolding at start of line
            # e.g. "**Inject AI chat system context** — Understand..."
            # We keep it as is, or strip markers?
            # YAML description usually shouldn't have markdown, strictly.
            # But "test" example is simple.
            # Let's try to remove simple formatting chars from the start/end if they are just bolding.
            # But the line `**Inject...** - ...` is mixed.
            # Let's just escape quotes for YAML and use the string.
            description = desc_text
            found_description_line = True
        
        body_lines.append(line)

    # Join body back
    body = "\n".join(body_lines)
    
    # If no description found (empty file or just title), default
    if not description:
        description = "No description provided"

    # Escape double quotes for YAML
    description = description.replace('"', '\\"')
    
    return description, body


def sync_file(
    src: Path,
    dest: Path,
    *,
    dry_run: bool,
    target: SyncTarget,
) -> bool:
    """Sync a single file."""
    src_text = src.read_text(encoding="utf-8")
    
    description, body = extract_description(src_text)
    
    if target == SyncTarget.AGENT:
        new_content = f"""---
description: "{description}"
---

{body}
"""
    elif target == SyncTarget.VSCODE:
        prompt_name = src.stem
        new_content = f"""---
agent: 'agent'
description: "{description}"
name: "{prompt_name}"
---

{body}
"""
    else:
        return False

    if not dest.exists():
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(new_content, encoding="utf-8")
        return True

    old_text = dest.read_text(encoding="utf-8")

    if new_content == old_text:
        return False

    if not dry_run:
        dest.write_text(new_content, encoding="utf-8")

    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync Cursor commands (.md) to Agent Workflows (.md) and VS Code Prompts (.prompt.md).",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Path to repo root",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would change without writing files",
    )
    
    args = parser.parse_args()
    
    repo_root: Path = args.repo_root
    cursor_dir = repo_root / ".cursor" / "commands"
    agent_dir = repo_root / ".agent" / "workflows"
    vscode_dir = repo_root / ".github" / "prompts"
    
    if not cursor_dir.is_dir():
        print(f"Cursor commands dir not found: {cursor_dir}")
        return 1
        
    src_files = sorted(cursor_dir.glob("*.md"))
    
    if not src_files:
        print(f"No .md files found in {cursor_dir}")
        return 0

    all_updated = {Target: [] for Target in SyncTarget}
    
    for src in src_files:
        # Sync to AGENT
        dest_agent = agent_dir / src.name
        if sync_file(src, dest_agent, dry_run=args.dry_run, target=SyncTarget.AGENT):
            all_updated[SyncTarget.AGENT].append(dest_agent)

        # Sync to VSCODE
        dest_vscode = vscode_dir / f"{src.stem}.prompt.md"
        if sync_file(src, dest_vscode, dry_run=args.dry_run, target=SyncTarget.VSCODE):
            all_updated[SyncTarget.VSCODE].append(dest_vscode)

    print(f"Processed {len(src_files)} Cursor commands")
    for Target in SyncTarget:
        print(f"{Target.value.upper()}: Updated {len(all_updated[Target])} files")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
