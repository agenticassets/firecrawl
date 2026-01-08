#!/usr/bin/env python3
"""Sync .cursor/rules/**/*.mdc -> .windsurf/rules/**/*.md and .github/instructions/*.instructions.md.

Default behavior:
- Recursively syncs Cursor rules into the same subdirectory structure in Windsurf.
- Converts Cursor rules to VS Code .instructions.md format in .github/instructions/.
- Applies a minimal rewrite so Cursor cross-references keep working in each target:
  - @.cursor/rules/subfolder/<name>.mdc  -> @.windsurf/rules/subfolder/<name>.md
  - @.cursor/rules/subfolder/<name>.mdc  -> @.github/instructions/subfolder/<name>.instructions.md
"""

from __future__ import annotations

import argparse
import re
from enum import Enum
from pathlib import Path


# updated regex to handle subdirectories
CURSOR_REF_RE = re.compile(r"@\.cursor/rules/([A-Za-z0-9_/.-]+)\.mdc\b")


class SyncTarget(str, Enum):
    """Target IDE for rule syncing."""

    WINDSURF = "windsurf"
    VSCODE = "vscode"
    ANTIGRAVITY = "antigravity"
    BOTH = "both"


def parse_frontmatter(content: str) -> tuple[dict[str, str | bool], str]:
    """Parse YAML frontmatter from Cursor rule file.

    Returns:
        Tuple of (frontmatter_dict, body_content)
    """
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    frontmatter_text = parts[1].strip()
    body = parts[2].strip()

    # Simple YAML parsing (basic key: value pairs)
    frontmatter: dict[str, str | bool] = {}
    for line in frontmatter_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            # Handle boolean values
            if value.lower() == "true":
                frontmatter[key] = True
            elif value.lower() == "false":
                frontmatter[key] = False
            else:
                frontmatter[key] = value

    return frontmatter, body


def convert_to_vscode_instructions(
    cursor_content: str, filename: str
) -> str:
    """Convert Cursor rule content to VS Code .instructions.md format.

    Args:
        cursor_content: Full content of Cursor rule file
        filename: Base filename (without extension) for naming

    Returns:
        VS Code instructions file content
    """
    frontmatter, body = parse_frontmatter(cursor_content)

    # Extract VS Code fields from Cursor frontmatter
    description = frontmatter.get("description", "")
    globs = frontmatter.get("globs", "")
    always_apply = frontmatter.get("alwaysApply", False)

    # Determine applyTo value
    apply_to: str
    if always_apply:
        apply_to = "**"  # Apply to all files
    elif globs:
        apply_to = str(globs)
    else:
        apply_to = ""  # Manual attachment only

    # Build VS Code frontmatter
    vscode_frontmatter_lines = ["---"]
    if description:
        vscode_frontmatter_lines.append(f'description: "{description}"')
    vscode_frontmatter_lines.append(f'name: "{filename}"')
    if apply_to:
        vscode_frontmatter_lines.append(f'applyTo: "{apply_to}"')
    vscode_frontmatter_lines.append("---")

    # Rewrite references in body
    body_rewritten = CURSOR_REF_RE.sub(
        r"@.github/instructions/\1.instructions.md", body
    )

    return "\n".join(vscode_frontmatter_lines) + "\n\n" + body_rewritten


    return "\n".join(vscode_frontmatter_lines) + "\n\n" + body_rewritten


def convert_to_antigravity_rules(cursor_content: str, filename: str) -> str:
    """Convert Cursor rule content to Antigravity .md rules format.

    Args:
        cursor_content: Full content of Cursor rule file
        filename: Base filename (without extension) for naming

    Returns:
        Antigravity rule file content
    """
    frontmatter, body = parse_frontmatter(cursor_content)

    # Extract fields from Cursor frontmatter
    globs = frontmatter.get("globs", "")
    always_apply = frontmatter.get("alwaysApply", False)

    # Build Antigravity frontmatter
    # Trigger logic:
    # 1. always_on
    # 2. glob (with globs)
    # 3. manual (default)
    # 4. model_decision (not strictly inferable from Cursor rules, so we skip for now unless we want to map "auto" or something)

    ag_frontmatter_lines = ["---"]

    if always_apply:
        ag_frontmatter_lines.append("trigger: always_on")
    elif globs:
        ag_frontmatter_lines.append("trigger: glob")
        # Ensure globs is a list or string correctly formatted
        # The user example showed "globs: app/*.tsx"
        # If existing globs is a list, join it? Or just stringify.
        # Cursor usually has globs as string or list of strings.
        ag_frontmatter_lines.append(f'globs: "{globs}"')
    else:
        ag_frontmatter_lines.append("trigger: manual")

    ag_frontmatter_lines.append("---")

    # Rewrite references in body
    # We'll map @.cursor/rules -> @.agent/rules
    # And .mdc -> .md
    body_rewritten = CURSOR_REF_RE.sub(
        r"@.agent/rules/\1.md", body
    )

    return "\n".join(ag_frontmatter_lines) + "\n\n" + body_rewritten


def rewrite_cursor_refs_to_windsurf(content: str) -> str:
    """Rewrite Cursor references to Windsurf references."""
    return CURSOR_REF_RE.sub(r"@.windsurf/rules/\1.md", content)


def sync_file(
    src: Path,
    dest: Path,
    *,
    dry_run: bool,
    target: SyncTarget,
) -> bool:
    """Sync a single file from Cursor rules to target IDE rules."""
    src_text = src.read_text(encoding="utf-8")

    # Rewrite references based on target
    if target == SyncTarget.WINDSURF:
        new_text = rewrite_cursor_refs_to_windsurf(src_text)
    elif target == SyncTarget.VSCODE:
        # Convert to VS Code instructions format
        filename = src.stem
        new_text = convert_to_vscode_instructions(src_text, filename)
    elif target == SyncTarget.ANTIGRAVITY:
        filename = src.stem
        new_text = convert_to_antigravity_rules(src_text, filename)
    else:
        # Should not happen, but fallback to Windsurf
        new_text = rewrite_cursor_refs_to_windsurf(src_text)

    if not dest.exists():
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(new_text, encoding="utf-8")
        return True

    old_text = dest.read_text(encoding="utf-8")

    if new_text == old_text:
        return False

    if not dry_run:
        dest.write_text(new_text, encoding="utf-8")

    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync Cursor rule files (.mdc) to Windsurf and/or VS Code rule files (.md).",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Path to repo root (defaults to parent of scripts/)",
    )
    parser.add_argument(
        "--target",
        type=SyncTarget,
        choices=list(SyncTarget),
        default=SyncTarget.BOTH,
        help="Target IDE(s) to sync to: windsurf, vscode, or both (default: both)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would change without writing files",
    )
    parser.add_argument(
        "--stems",
        type=str,
        default=None,
        help=(
            "Comma-separated list of Cursor rule stems to sync (e.g. '001-ai_integration_rules_concise,001b-ai-integration-tools'). "
            "If omitted, all Cursor .mdc rules are considered."
        ),
    )
    create_missing_group = parser.add_mutually_exclusive_group()
    create_missing_group.add_argument(
        "--create-missing",
        action="store_true",
        help="Create target rule files if missing (default behavior)",
    )
    create_missing_group.add_argument(
        "--no-create-missing",
        action="store_true",
        help="Do not create target rule files if missing",
    )

    args = parser.parse_args()

    create_missing = bool(args.create_missing) or not bool(args.no_create_missing)
    targets = (
        [SyncTarget.WINDSURF, SyncTarget.VSCODE, SyncTarget.ANTIGRAVITY]
        if args.target == SyncTarget.BOTH
        else [args.target]
    )

    repo_root: Path = args.repo_root
    cursor_dir = repo_root / ".cursor" / "rules"

    if not cursor_dir.is_dir():
        raise SystemExit(f"Cursor rules dir not found: {cursor_dir}")

    # Check target directories exist (or will be created)
    target_dirs = {}
    for target in targets:
        if target == SyncTarget.WINDSURF:
            target_dir = repo_root / ".windsurf" / "rules"
            if not target_dir.is_dir() and not create_missing:
                raise SystemExit(f"Windsurf rules dir not found: {target_dir}")
            target_dirs[target] = target_dir
        elif target == SyncTarget.VSCODE:
            target_dir = repo_root / ".github" / "instructions"
            # VS Code instructions dir may not exist yet - that's okay, we'll create it
            target_dirs[target] = target_dir
        elif target == SyncTarget.ANTIGRAVITY:
            target_dir = repo_root / ".agent" / "rules"
            target_dirs[target] = target_dir

    src_files = sorted(cursor_dir.rglob("*.mdc"))
    if args.stems:
        stems = {s.strip() for s in args.stems.split(",") if s.strip()}
        src_files = [p for p in src_files if p.stem in stems]
    if not src_files:
        print(f"No Cursor .mdc rules found in {cursor_dir}")
        return 0

    # Track updates per target
    all_updated: dict[SyncTarget, list[Path]] = {target: [] for target in targets}
    all_skipped_missing: dict[SyncTarget, list[Path]] = {target: [] for target in targets}

    for src in src_files:
        rel_path = src.relative_to(cursor_dir)

        for target in targets:
            target_dir = target_dirs[target]
            # VS Code uses .instructions.md extension, Windsurf uses .md
            if target == SyncTarget.VSCODE:
                dest = target_dir / rel_path.with_suffix(".instructions.md")
            else:
                dest = target_dir / rel_path.with_suffix(".md")

            if not dest.exists():
                if create_missing:
                    if args.dry_run:
                        print(f"[dry-run] create {dest} ({target.value})")
                    else:
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        # Rewrite references based on target
                        src_text = src.read_text(encoding="utf-8")
                        if target == SyncTarget.WINDSURF:
                            new_text = rewrite_cursor_refs_to_windsurf(src_text)
                        elif target == SyncTarget.VSCODE:
                            filename = src.stem
                            new_text = convert_to_vscode_instructions(
                                src_text, filename
                            )
                        elif target == SyncTarget.ANTIGRAVITY:
                            filename = src.stem
                            new_text = convert_to_antigravity_rules(
                                src_text, filename
                            )
                        else: # Fallback
                             new_text = src_text

                        dest.write_text(new_text, encoding="utf-8")
                    all_updated[target].append(dest)
                else:
                    all_skipped_missing[target].append(dest)
                continue

            changed = sync_file(src, dest, dry_run=args.dry_run, target=target)
            if changed:
                all_updated[target].append(dest)

    # Print summary
    print(f"Processed {len(src_files)} Cursor rules")
    for target in targets:
        updated = all_updated[target]
        skipped = all_skipped_missing[target]
        target_name = target.value.upper()
        print(f"\n{target_name}:")
        print(f"  Updated {len(updated)} rule files{' (dry-run)' if args.dry_run else ''}")
        if updated:
            for p in updated:
                print(f"  - {p.as_posix()}")

        if skipped:
            print(f"  Skipped {len(skipped)} missing targets (use --create-missing to create):")
            for p in skipped:
                print(f"  - {p.as_posix()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
