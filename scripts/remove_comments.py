#!/usr/bin/env python3
"""Remove Python comments from files while keeping comments that match a pattern.

This script uses the `tokenize` module to remove COMMENT tokens unless they
contain the keep pattern (default: '마이:'). It creates backups of edited
files under `backups/comments-<timestamp>/`.

Usage:
  python3 scripts/remove_comments.py --path src --keep '마이:'
"""

import argparse
import os
import shutil
import sys
import time
import tokenize
from io import BytesIO


def process_file(path: str, keep_pattern: str) -> bool:
    with open(path, 'rb') as f:
        src = f.read()

    changed = False
    tokens = list(tokenize.tokenize(BytesIO(src).readline))
    new_tokens = []

    for tok in tokens:
        if tok.type == tokenize.COMMENT:
            if keep_pattern in tok.string:
                new_tokens.append(tok)
            else:
                # drop comment
                changed = True
                continue
        else:
            new_tokens.append(tok)

    new_src = tokenize.untokenize(new_tokens)
    # ensure bytes
    if isinstance(new_src, str):
        new_bytes = new_src.encode('utf-8')
    else:
        new_bytes = new_src

    if new_bytes != src:
        with open(path, 'wb') as f:
            f.write(new_bytes)
        return True
    return False


def find_py_files(base_path: str):
    for root, dirs, files in os.walk(base_path):
        # skip __pycache__ dirs
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for fn in files:
            if fn.endswith('.py'):
                yield os.path.join(root, fn)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default='src', help='Path to scan for .py files')
    parser.add_argument('--keep', default='마이:', help='Keep comments containing this pattern')
    args = parser.parse_args()

    base = args.path
    if not os.path.exists(base):
        print('Path does not exist:', base, file=sys.stderr)
        sys.exit(2)

    stamp = time.strftime('%Y%m%d-%H%M%S')
    backup_dir = os.path.join('backups', f'comments-{stamp}')
    os.makedirs(backup_dir, exist_ok=True)

    changed_files = []
    for p in find_py_files(base):
        rel = os.path.relpath(p)
        # backup
        dest = os.path.join(backup_dir, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(p, dest)
        if process_file(p, args.keep):
            changed_files.append(p)

    print('Backup saved to', backup_dir)
    if changed_files:
        print('Modified files:')
        for f in changed_files:
            print(' -', f)
    else:
        print('No files changed.')


if __name__ == '__main__':
    main()
