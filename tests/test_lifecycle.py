from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest
SOURCE=Path(__file__).resolve().parents[1]/'skills/neckbeard'
class LifecycleTests(unittest.TestCase):
 def run_install(self,target,*args):return subprocess.run([sys.executable,str(SOURCE/'scripts/install.py'),'--target',str(target),*args],capture_output=True,text=True)
 def test_upgrade_preserves_config_uninstall_and_backups(self):
  with tempfile.TemporaryDirectory() as tmp:
   target=Path(tmp);self.assertEqual(self.run_install(target,'--components','support','--agent','claude').returncode,0)
   dest=target/'neckbeard';self.assertTrue((dest/'CLAUDE.md').exists());(dest/'org-profile.yaml').write_text('organization: My organization\n')
   result=self.run_install(target,'--action','upgrade');self.assertEqual(result.returncode,0,result.stderr);self.assertEqual((dest/'org-profile.yaml').read_text(),'organization: My organization\n');self.assertEqual(list(json.loads((dest/'components.json').read_text())['components']),['support'])
   result=self.run_install(target,'--action','uninstall');self.assertEqual(result.returncode,0,result.stderr);self.assertFalse(dest.exists());self.assertEqual(len(list((target/'.neckbeard-backups').iterdir())),2)
 def test_upgrade_refuses_local_code_changes(self):
  with tempfile.TemporaryDirectory() as tmp:
   self.assertEqual(self.run_install(tmp).returncode,0);(Path(tmp)/'neckbeard/SKILL.md').write_text('locally modified')
   result=self.run_install(tmp,'--action','upgrade');self.assertNotEqual(result.returncode,0);self.assertIn('Local changes',result.stderr)
 def test_adapters(self):
  for agent,entry in [('claude','CLAUDE.md'),('cursor','neckbeard.mdc'),('generic','AGENTS.md')]:
   with tempfile.TemporaryDirectory() as tmp:
    p=self.run_install(tmp,'--agent',agent,'--components','core');self.assertEqual(p.returncode,0,p.stderr);self.assertTrue((Path(tmp)/'neckbeard'/entry).exists())
 def test_checksum_tamper_is_rejected(self):
  import shutil
  with tempfile.TemporaryDirectory() as tmp:
   copy=Path(tmp)/'source';shutil.copytree(SOURCE,copy);(copy/'SKILL.md').write_text('tampered')
   p=subprocess.run([sys.executable,str(copy/'scripts/install.py'),'--target',str(Path(tmp)/'target')],capture_output=True,text=True);self.assertNotEqual(p.returncode,0);self.assertIn('checksum mismatch',p.stderr)
