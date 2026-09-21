#!/usr/bin/env python3
"""Update one or more git repositories to the latest remote state.

Usage:
  python scripts/update_to_latest.py [--path PATH] [--stash]

Options:
  --path PATH   Path to a git repo or directory containing repos (default: current directory)
  --stash       Auto-stash uncommitted changes before pulling and pop after

This script:
 - detects git repos at the provided path (or the path itself if it's a repo)
 - optionally stashes local changes
 - runs `git fetch --all --prune` and `git pull --rebase origin <branch>`
 - updates submodules recursively
"""

import argparse
import os
import subprocess
import sys


def run(cmd, cwd=None, check=True):
    print(f"$ {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    print(res.stdout)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)} (cwd={cwd})")
    return res


def is_git_repo(path):
    return os.path.isdir(os.path.join(path, '.git'))


def has_uncommitted_changes(path):
    r = subprocess.run(['git', 'status', '--porcelain'], cwd=path, stdout=subprocess.PIPE, text=True)
    return bool(r.stdout.strip())


def current_branch(path):
    r = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=path, stdout=subprocess.PIPE, text=True)
    return r.stdout.strip()


def update_repo(path, stash=False):
    print(f"== Updating {path}")
    if not is_git_repo(path):
        print("Not a git repository — skipping")
        return

    stashed = False
    if has_uncommitted_changes(path):
        if not stash:
            print("Uncommitted changes present. Use --stash to auto-stash, or commit/clean first. Skipping.")
            return
        else:
            print("Stashing local changes...")
            run(['git', 'stash', 'push', '-u', '-m', 'autostash-before-update'], cwd=path)
            stashed = True

    try:
        run(['git', 'fetch', '--all', '--prune'], cwd=path)
        branch = current_branch(path)
        if branch == 'HEAD' or branch == 'detached':
            print('Detached HEAD; skipping pull')
        else:
            # try pull --rebase; allow non-zero return but continue
            try:
                run(['git', 'pull', '--rebase', 'origin', branch], cwd=path, check=False)
            except Exception as e:
                print(f'Pull failed: {e}')

        run(['git', 'submodule', 'update', '--init', '--recursive'], cwd=path)
        print(f"Updated {path} successfully")
    finally:
        if stashed:
            print('Popping stash...')
            # try to pop; if conflict, leave as-is
            try:
                run(['git', 'stash', 'pop'], cwd=path, check=False)
            except Exception as e:
                print(f'Failed to pop stash automatically: {e}')


def find_and_update(base_path, stash=False):
    base_path = os.path.abspath(base_path)
    if is_git_repo(base_path):
        update_repo(base_path, stash=stash)
        return

    # otherwise, scan immediate children for git repos
    for name in sorted(os.listdir(base_path)):
        full = os.path.join(base_path, name)
        if os.path.isdir(full) and is_git_repo(full):
            update_repo(full, stash=stash)


def main():
    parser = argparse.ArgumentParser(description='Update git repo(s) to latest from origin')
    parser.add_argument('--path', '-p', default='.', help='Path to repo or directory')
    parser.add_argument('--stash', action='store_true', help='Auto-stash uncommitted changes')
    args = parser.parse_args()

    try:
        find_and_update(args.path, stash=args.stash)
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
