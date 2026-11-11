#!/usr/bin/env python3
"""Install, upgrade or reversibly uninstall a managed Neckbeard edition."""
import argparse
import json
from pathlib import Path
import shutil
import tempfile
import uuid
from checksums import digest, manifest as file_manifest, verify

CONFIG={'org-profile.yaml','glossary.json'}


def backup(destination):
    parent=destination.parent/'.neckbeard-backups';parent.mkdir(exist_ok=True)
    path=parent/('neckbeard-'+uuid.uuid4().hex)
    destination.rename(path)
    return path


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target',required=True,type=Path,help='Parent directory for the managed neckbeard folder')
    parser.add_argument('--components',help='Comma-separated IDs, or core; upgrades preserve the existing edition by default')
    parser.add_argument('--action',choices=['install','upgrade','uninstall'],default='install')
    parser.add_argument('--agent',choices=['codex','claude','cursor','generic'],default=None)
    parser.add_argument('--adopt-legacy',action='store_true',help='Explicitly upgrade an older manifest-bearing installation without a receipt, preserving a full backup')
    args=parser.parse_args()
    source=Path(__file__).resolve().parents[1];target=args.target.expanduser().resolve();destination=target/'neckbeard'
    try:
        if destination.is_symlink():raise ValueError('Refusing a symlink destination')
        if args.action=='install' and destination.exists():raise ValueError('Destination already exists; use --action upgrade')
        if args.action!='install' and not destination.is_dir():raise ValueError('No installation found')
        old=None;receipt=None
        if destination.exists():
            old=json.loads((destination/'components.json').read_text())
            if old.get('name')!='neckbeard':raise ValueError('Destination is not a Neckbeard installation')
            rp=destination/'.neckbeard-install.json'
            if rp.exists():
                receipt=json.loads(rp.read_text())
                if receipt.get('name')!='neckbeard' or not isinstance(receipt.get('files'),dict):raise ValueError('Invalid managed installation receipt')
            elif not args.adopt_legacy:raise ValueError('Legacy installation requires --adopt-legacy; it will be backed up')
        if args.action=='uninstall':
            if args.components is not None:raise ValueError('Uninstall removes the entire edition; omit --components')
            saved=backup(destination);print('Uninstalled; complete recoverable backup: '+str(saved));return
        verify(source)
        available=json.loads((source/'components.json').read_text())
        if receipt and args.action=='upgrade':
            current=file_manifest(destination)
            expected=receipt['files']
            changed={k for k in set(current)|set(expected) if current.get(k)!=expected.get(k)}-CONFIG
            if changed:raise ValueError('Local changes detected; preserve them before upgrading: '+', '.join(sorted(changed)))
        selected=set(available['components']) if args.components is None and old is None else set(old['components']) if args.components is None else set(x.strip() for x in args.components.split(',') if x.strip())
        if args.components is not None and not args.components.strip():raise ValueError('Use core for a minimal edition')
        selected.discard('core');unknown=selected-set(available['components'])
        if unknown:raise ValueError('Unavailable components: '+', '.join(sorted(unknown)))
        agent=args.agent or (receipt or {}).get('agent','codex')
        target.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.neckbeard-install-',dir=target) as temporary:
            staging=Path(temporary)/'neckbeard';staging.mkdir()
            for directory in ('references','agents','assets','scripts','adapters'):
                shutil.copytree(source/directory,staging/directory,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
            for name in ('SKILL.md','org-profile.yaml','glossary.json','requirements.txt','LICENSE'):
                shutil.copy2(source/name,staging/name)
            for name in CONFIG:
                if old and (destination/name).exists():shutil.copy2(destination/name,staging/name)
            (staging/'components').mkdir()
            for name in sorted(selected):
                path=Path(available['components'][name]['instructions'])
                if path.is_absolute() or '..' in path.parts or path.parent!=Path('components'):raise ValueError('Invalid component path')
                shutil.copy2(source/path,staging/path)
            available['components']={name:available['components'][name] for name in sorted(selected)}
            (staging/'components.json').write_text(json.dumps(available,indent=2)+'\n')
            entry={'claude':'CLAUDE.md','cursor':'neckbeard.mdc','generic':'AGENTS.md'}.get(agent)
            if entry:shutil.copy2(source/'adapters'/entry,staging/entry)
            # Installed editions carry their own checksum manifest and immutable ownership receipt.
            (staging/'CHECKSUMS.json').write_text(json.dumps({'algorithm':'sha256','files':file_manifest(staging)},indent=2,sort_keys=True)+'\n')
            payload={'name':'neckbeard','version':available['version'],'agent':agent,'files':file_manifest(staging)}
            (staging/'.neckbeard-install.json').write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
            saved=backup(destination) if old else None
            try:staging.rename(destination)
            except OSError:
                if saved:saved.rename(destination)
                raise
        print('Installed Neckbeard '+available['version']+' for '+agent+': '+str(destination))
        if saved:print('Previous installation backup: '+str(saved))
        print('Components: core'+(', '+', '.join(sorted(selected)) if selected else ''))
    except (OSError,ValueError,KeyError,TypeError) as exc:parser.error(str(exc))

if __name__=='__main__':main()
