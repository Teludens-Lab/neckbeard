#!/usr/bin/env python3
"""Create or verify a deterministic source checksum manifest (not a signature)."""
import argparse
import hashlib
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest(root):
    result={}
    for path in sorted(root.rglob('*')):
        if path.is_symlink(): raise ValueError('Symlinks are not permitted in distributions')
        if path.is_file() and path.name not in ('CHECKSUMS.json','.neckbeard-install.json') and '__pycache__' not in path.parts and path.suffix != '.pyc':
            result[path.relative_to(root).as_posix()]=digest(path)
    return result


def verify(root):
    expected=json.loads((root/'CHECKSUMS.json').read_text())
    if expected.get('algorithm')!='sha256' or expected.get('files')!=manifest(root):
        raise ValueError('Distribution checksum mismatch; regenerate only from reviewed source')
    return True


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['create','verify']);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args()
    if a.action=='create':(a.root/'CHECKSUMS.json').write_text(json.dumps({'algorithm':'sha256','files':manifest(a.root)},indent=2,sort_keys=True)+'\n')
    else:verify(a.root)
    print('Checksums '+a.action+' passed')

if __name__=='__main__':main()
