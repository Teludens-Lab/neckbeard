import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
class BehaviorTests(unittest.TestCase):
 def test_supported_task_and_recovery(self):
  fixture=ROOT/'evals/fixtures/approval-product/app.py'
  p=subprocess.run([sys.executable,str(fixture),'submit','--role','participant','--text','Repair the bridge'],capture_output=True,text=True);self.assertEqual(p.returncode,0);self.assertEqual(json.loads(p.stdout)['status'],'submitted')
  p=subprocess.run([sys.executable,str(fixture),'submit','--role','observer','--text','Repair the bridge'],capture_output=True,text=True);self.assertNotEqual(p.returncode,0);self.assertIn('Only participants',p.stderr)
  p=subprocess.run([sys.executable,str(fixture),'submit','--role','participant','--text',''],capture_output=True,text=True);self.assertNotEqual(p.returncode,0);self.assertIn('Proposal text is required',p.stderr)
 def test_roadmap_is_not_executable(self):
  p=subprocess.run([sys.executable,str(ROOT/'evals/fixtures/approval-product/app.py'),'export'],capture_output=True,text=True);self.assertNotEqual(p.returncode,0)
 def test_scoring_critical_failure_overrides_score(self):
  spec=importlib.util.spec_from_file_location('score',ROOT/'evals/score.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  rubric=json.loads((ROOT/'evals/rubric.json').read_text());submission={'case_id':'first-task','reviewer':'test-reviewer','artifact':'fixture-only','criteria':{c['id']:{'score':4,'evidence':'test evidence'} for c in rubric['criteria']},'critical_failures':[]}
  self.assertTrue(m.score(rubric,submission)['passed']);submission['critical_failures']=['false_runtime_verification'];self.assertFalse(m.score(rubric,submission)['passed'])
