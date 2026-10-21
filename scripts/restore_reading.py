#!/usr/bin/env python3
"""Restore the full prose and formulas from the archived reading manuscript."""
from pathlib import Path
import json

root=Path(__file__).resolve().parents[1]
source=(root/'_source_archive/teaching.Rmd').read_text(encoding='utf8').splitlines(keepends=True)
manifest=json.loads((root/'MIGRATION_MANIFEST.json').read_text(encoding='utf8'))
titles={
 'statistics-history.md':('History of Statistics and Probability','/reading/history/'),
 'estimation.md':('Estimation','/reading/estimation/'),
 'kl-divergence.md':('KL Divergence and Modern Statistics','/reading/kl-divergence/'),
 'reading-books.md':('Book Notes','/reading/books/'),
 'philosophy.md':('Philosophy and Quotes','/reading/philosophy/'),
}
for entry in manifest['reading_slices']:
    destination=root/entry['destination']
    title,url=titles[destination.name]
    body=''.join(source[entry['start_line']-1:entry['end_line']]).strip()
    if destination.name=='philosophy.md':
        body=body.replace('## reference list','')
    header='---\nlayout: page\ntitle: '+json.dumps(title)+'\npermalink: '+url+'\nnav: false\nmath: true\ntoc:\n  sidebar: left\n---\n\n[← Reading]({{ \'/reading/\' | relative_url }})\n\n'
    destination.write_text(header+body+'\n',encoding='utf8')
