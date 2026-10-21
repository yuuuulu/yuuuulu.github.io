#!/usr/bin/env python3
"""Verify archived source files and the reading pages."""
from pathlib import Path
import hashlib, json
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'MIGRATION_MANIFEST.json').read_text(encoding='utf8'))
source=(root/'_source_archive/teaching.Rmd').read_text(encoding='utf8').splitlines(keepends=True)
assembled=[]
for entry in manifest['reading_slices']:
    content=''.join(source[entry['start_line']-1:entry['end_line']])
    if hashlib.sha256(content.encode()).hexdigest()!=entry['sha256']:
        raise SystemExit('Source slice changed: '+entry['destination'])
    if not (root/entry['destination']).is_file():
        raise SystemExit('Reading page missing: '+entry['destination'])
    assembled.append(content)
if ''.join(assembled)!=''.join(source[10:]):
    raise SystemExit('Reading source incomplete')
for filename, sha in manifest['archived_files_sha256'].items():
    if hashlib.sha256((root/'_source_archive'/filename).read_bytes()).hexdigest()!=sha:
        raise SystemExit('Archived file changed: '+filename)
print('PASS: Archived sources verified; reading pages present.')
