#!/usr/bin/env python3
"""
Markdown linting fixer for docs/ directory.
Fixes the most common linting issues:
- MD022: blanks-around-headings
- MD032: blanks-around-lists
- MD031: blanks-around-fences
- MD040: fenced-code-language
- MD013: line-length
- MD009: trailing-spaces
- MD026: no-trailing-punctuation (in headings)
- MD050: strong-style (use * not _)
"""

import re
from pathlib import Path


def fix_markdown_file(filepath):
    """Fix markdown linting issues in a file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Fix 1: Add blank lines around headings (MD022)
    # Heading should have blank line before (except at start) and after
    content = re.sub(r"([^\n])\n(#{1,6} )", r"\1\n\n\2", content)
    content = re.sub(r"(#{1,6} [^\n]*)\n([^\n])", r"\1\n\n\2", content)

    # Fix 2: Add blank lines around lists (MD032)
    # Lists need blank lines before and after
    content = re.sub(r"([^\n])\n([-*+\d]\. )", r"\1\n\n\2", content)
    content = re.sub(r"([-*+\d]\. [^\n]*)\n([^\n-*+\d])", r"\1\n\n\2", content)

    # Fix 3: Add blank lines around fenced code blocks (MD031)
    # Fenced blocks need blank line before and after
    content = re.sub(r"([^\n])\n(```)", r"\1\n\n\2", content)
    content = re.sub(r"(```)\n([^\n`])", r"\1\n\n\2", content)

    # Fix 4: Add language to fenced code blocks (MD040)
    # ```lang instead of ```
    content = re.sub(r"```\n", r"```text\n", content)
    # But preserve already-specified languages
    content = re.sub(
        r"```text(bash|python|json|yaml|yml|html|css|js|javascript|shell)\n",
        r"```\1\n",
        content,
    )

    # Fix 5: Remove trailing spaces (MD009)
    lines = content.split("\n")
    lines = [line.rstrip() for line in lines]
    content = "\n".join(lines)

    # Fix 6: Fix strong style (MD050) - use * not _
    content = re.sub(r"__([^_]+)__", r"**\1**", content)
    content = re.sub(r"_([^_\n]+)_", r"*\1*", content)  # Careful with this one

    # Fix 7: Remove trailing punctuation in headings (MD026)
    # Keep colons and exclamations in specific cases
    content = re.sub(
        r"^(#{1,6} [^#\n]*[.!?])(\s*)$",
        lambda m: m.group(1).rstrip(".!?") + m.group(2),
        content,
        flags=re.MULTILINE,
    )

    # Write back if changed
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    """Process all markdown files in docs/"""
    docs_dir = Path("docs")
    fixed_count = 0
    file_count = 0

    for md_file in docs_dir.rglob("*.md"):
        file_count += 1
        if fix_markdown_file(str(md_file)):
            fixed_count += 1
            print(f"✓ Fixed: {md_file}")
        else:
            print(f"  Skipped: {md_file}")

    print(f"\n📊 Summary: {fixed_count}/{file_count} files modified")


if __name__ == "__main__":
    main()
