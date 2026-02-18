#!/usr/bin/env python3
"""
Markdown fixer for remaining issues.
Focus on MD036 (emphasis as heading) and MD032 edge cases.
"""

import re
from pathlib import Path


def fix_emphasis_headings(content):
    """Convert **Text:** to ### Text heading."""
    # **Text:** → ### Text
    pattern = r'^\*\*([^*]+):\*\*\s*$'
    result = []
    lines = content.split('\n')

    for i, line in enumerate(lines):
        if re.match(pattern, line):
            match = re.match(pattern, line)
            text = match.group(1)
            # Add blank line before if needed
            if result and result[-1].strip():
                result.append('')
            result.append(f'### {text}')
        else:
            result.append(line)

    return '\n'.join(result)


def fix_markdown_file(filepath):
    """Fix markdown issues in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Apply fixes
    content = fix_emphasis_headings(content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    """Process all markdown files in docs/"""
    docs_dir = Path('docs')
    fixed_count = 0
    file_count = 0

    for md_file in sorted(docs_dir.rglob('*.md')):
        file_count += 1
        if fix_markdown_file(str(md_file)):
            fixed_count += 1
            print(f"✓ {md_file.relative_to('.')}")

    print(f"\n✅ Fixed {fixed_count}/{file_count} files")


if __name__ == '__main__':
    main()
