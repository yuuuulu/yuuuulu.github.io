#!/usr/bin/env python3
"""Safely stage a full al-folio migration IN the original yuuuulu.github.io repo.

Requires a clean local checkout on 'main'. Publishes a backup branch to origin
BEFORE touching tracked files. Does not push any changes to 'main'.
"""
from pathlib import Path
import argparse
import re
import shutil
import subprocess
import sys
import yaml

PACKAGE = Path(__file__).resolve().parent.parent
EXPECTED = re.compile(r"^(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)(?:yuuuulu/yuuuulu\.github\.io)(?:\.git)?/?$", re.I)


def git(repo, *args, capture=True):
    cmd = ["git", "-C", str(repo), *args]
    return subprocess.run(cmd, check=True, text=True,
                          capture_output=capture).stdout.strip() if capture else subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser(description="Install new al-folio pages into your EXISTING GitHub Pages repository")
    ap.add_argument("--repo", required=True, help="Local path of the cloned yuuuulu.github.io repository")
    ap.add_argument("--apply", action="store_true", help="Actually create/push backup branch and stage replacement files")
    args = ap.parse_args()
    repo = Path(args.repo).expanduser().resolve()
    if not repo.is_dir() or not (repo / '.git').exists():
        raise SystemExit('ERROR: --repo must point to your existing CLONED Git repository, with its .git metadata.')
    actual = Path(git(repo, 'rev-parse','--show-toplevel')).resolve()
    if actual != repo:
        raise SystemExit(f'ERROR: repo path must be repository root, not {repo}. Actual root is {actual}.')
    branch = git(repo, 'branch', '--show-current')
    if branch != 'main':
        raise SystemExit(f'ERROR: Switch to main first (current branch: {branch}).')
    remote = git(repo, 'remote', 'get-url', 'origin')
    if not EXPECTED.fullmatch(remote):
        raise SystemExit(f'ERROR: Remote origin is not the expected original repository: {remote}')
    if git(repo, 'status','--porcelain','--untracked-files=normal'):
        raise SystemExit('ERROR: Your local repository has uncommitted/untracked changes. Commit or store them first.')
    if not (PACKAGE / '_pages' / 'about.md').exists():
        raise SystemExit('ERROR: Missing packaged about page.')
    if not (PACKAGE / '_source_archive' / 'teaching.Rmd').exists():
        raise SystemExit('ERROR: Missing original note archive.')
    config = yaml.safe_load((PACKAGE / '_config.yml').read_text(encoding='utf8'))
    if config.get('url') != 'https://yuuuulu.github.io' or config.get('baseurl') not in (None, ''):
        raise SystemExit('ERROR: The config is not configured for the original root site.')
    subprocess.run([sys.executable, str(PACKAGE/'scripts'/'audit_content.py')], check=True)
    sha = git(repo, 'rev-parse', '--short=8', 'HEAD')
    backup = f'backup-before-al-folio-{sha}'
    print('Original repository:', repo)
    print('Remote:', remote)
    print('Current branch:', branch)
    print('Backup branch to publish:', backup)
    print('Plan: publish BACKUP branch; replace tracked files, stage changes; never push main automatically.')
    if not args.apply:
        print('DRY RUN only. To stage the migration, repeat with --apply.')
        return
    # Save the old branch to GitHub before replacing a single tracked file.
    known = git(repo, 'branch', '--list', backup)
    if not known:
        git(repo, 'branch', backup)
    print('Publishing backup branch to GitHub...')
    git(repo, 'push','-u','origin', backup, capture=False)
    print('Backup published. Replacing tracked website files locally...')
    git(repo, 'rm', '-r', '-q', '--', '.', capture=False)
    for item in PACKAGE.iterdir():
        if item.name in {'.git','.DS_Store'}: continue
        dst = repo/item.name
        if item.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(item, dst)
        else:
            shutil.copy2(item, dst)
    git(repo, 'add', '-A', capture=False)
    print('\nDONE: New website is STAGED in your original repo, but NOT committed or published.')
    print('Check changes: git -C "'+str(repo)+'" diff --cached --stat')
    print('When satisfied, execute:')
    print('  git -C "'+str(repo)+'" commit -m "Migrate to al-folio and reorganize notes"')
    print('  git -C "'+str(repo)+'" push origin main')
    print('Then open GitHub Actions, followed by Settings > Pages > gh-pages / (root).')


if __name__ == '__main__':
    main()
