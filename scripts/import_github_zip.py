#!/usr/bin/env python3
"""Archive source notes and selected reports from github.zip for local editing."""
import argparse
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {'Math-s-interesting-things-main', 'stat.pre-main'}
SOURCE_EXTENSIONS = {'.qmd', '.ipynb', '.csv', '.txt', '.bib', '.rproj', '.md'}

def main(zip_path):
    with ZipFile(zip_path) as archive:
        for member in archive.namelist():
            if member.startswith('__MACOSX/') or member.endswith('/'):
                continue
            path = PurePosixPath(member)
            if path.parts[0] not in SOURCES or len(path.parts) < 2:
                continue
            relative = PurePosixPath(*path.parts[1:])
            if relative.parts[0] in {'docs', 'site_libs', '_freeze'} or any(part.endswith('_files') for part in relative.parts):
                continue
            if relative.suffix.lower() in SOURCE_EXTENSIONS:
                destination = ROOT / '_source_archive/github_zip' / path
            elif relative.suffix.lower() == '.pdf' and relative.name in {'2421874.pdf', 'MTH203_report.pdf'}:
                destination = ROOT / 'assets/pdf/imported' / relative.name
            else:
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(archive.read(member))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('zip_path', type=Path)
    main(parser.parse_args().zip_path)
