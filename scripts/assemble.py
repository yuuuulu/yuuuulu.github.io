#!/usr/bin/env python3
"""Overlay this migration onto an official al-folio starter checkout.

The upstream Jekyll layouts/styles/plugins are real al-folio. This repository
only replaces personal pages and website configuration; no fake reimplementation.
"""
import argparse
from pathlib import Path
import shutil
import yaml

p=argparse.ArgumentParser()
p.add_argument('--upstream',required=True)
p.add_argument('--out',required=True)
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
upstream=Path(a.upstream).resolve()
out=Path(a.out).resolve()
if not (upstream/'Gemfile').is_file() or not (upstream/'_config.yml').is_file():
 raise SystemExit('The upstream directory must be a genuine al-folio checkout.')
if out==upstream or out==root or root in out.parents and out.name=='_source_archive':
 raise SystemExit('Unsafe output directory.')
if out.exists():shutil.rmtree(out)
shutil.copytree(upstream,out,ignore=shutil.ignore_patterns('.git','.github','_site','vendor','.bundle'))

# Suppress upstream demonstration publications, projects, feeds, people and posts.
for dirname in ['_pages','_posts','_news','_projects','_books','_teachings','_bibliography']:
 target=out/dirname
 if target.exists():shutil.rmtree(target)
 target.mkdir(exist_ok=True)

# Use official full config so plugin expectations stay satisfied, then merge personal settings.
def merge(orig, overrides):
 for k,v in overrides.items():
  if isinstance(v,dict) and isinstance(orig.get(k),dict):merge(orig[k],v)
  else:orig[k]=v
 return orig

base=yaml.safe_load((out/'_config.yml').read_text(encoding='utf8'))
overrides=yaml.safe_load((root/'_config.yml').read_text(encoding='utf8'))
merged=merge(base,overrides)
merged['exclude']=list(dict.fromkeys((merged.get('exclude') or [])+['_source_archive','scripts','MIGRATION_MANIFEST.json','README_部署说明.md','README.md','tests']))
(out/'_config.yml').write_text(yaml.safe_dump(merged,allow_unicode=True,sort_keys=False,width=120),encoding='utf8')

for dirname in ['_pages','_bibliography','_data','_includes','assets']:
 overlay=root/dirname
 if overlay.exists():
  shutil.copytree(overlay,out/dirname,dirs_exist_ok=True)

# The local starter may contain assets from an earlier preview. Keep removed
# page media out of the newly assembled site as well.
for obsolete in ['assets/img/proabout.webp', 'assets/pdf/imported/APH103_Final_Report.pdf']:
 (out/obsolete).unlink(missing_ok=True)
shutil.rmtree(out/'assets/img/imported', ignore_errors=True)

# Remove al-folio author's social data and replace with Yu Lu's.
if not (out/'_data/socials.yml').exists():
 raise SystemExit('socials.yml was not copied')
# Avoid accidental default profile contact or example content from the starter.
# All intended pages, posts and bibliography are supplied by this migration.
print('Prepared genuine al-folio source at',out)
