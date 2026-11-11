#!/usr/bin/env python3
"""Copy fixtures into isolated Git repositories for reproducible fresh-agent runs."""
import argparse,json,shutil,subprocess
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True,type=Path);a=p.parse_args();root=a.out.resolve()
 if root.exists():p.error('Output already exists; choose a fresh directory')
 root.mkdir(parents=True)
 sources=Path(__file__).parent/'fixtures';result={}
 for fixture in sorted(sources.iterdir()):
  if not fixture.is_dir():continue
  dest=root/fixture.name;shutil.copytree(fixture,dest,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
  for args in (['init','-q'],['add','.'],['-c','user.name=Neckbeard Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Fixture baseline']):subprocess.run(['git','-C',str(dest),*args],check=True)
  revision=subprocess.check_output(['git','-C',str(dest),'rev-parse','HEAD']).decode().strip();result[fixture.name]={'path':str(dest),'revision':revision}
 (root/'fixtures.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
