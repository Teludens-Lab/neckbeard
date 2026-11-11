import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / 'skills' / 'neckbeard'

class InstallerTests(unittest.TestCase):
    def test_editions_and_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            for edition, count in [('core', 0), ('end-user,practice', 2), ('media', 1), (None, 8)]:
                target = Path(tmp) / str(count)
                command = [sys.executable, str(SOURCE/'scripts/install.py'), '--target', str(target)]
                if edition is not None:
                    command += ['--components', edition]
                result = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                dest = target/'neckbeard'
                manifest = json.loads((dest/'components.json').read_text())
                self.assertEqual(len(manifest['components']), count)
                self.assertEqual(len(list((dest/'components').glob('*.md'))), count)
                for item in manifest['components'].values():
                    self.assertTrue((dest/item['instructions']).is_file())
                self.assertTrue((dest/'assets/neckbeard.svg').is_file())
                self.assertTrue((dest/'references/production-standards.md').is_file())
                if 'media' in manifest['components']:
                    self.assertTrue((dest/'references/production-brief-template.yaml').is_file())
                    self.assertTrue((dest/'references/storyboard-template.csv').is_file())
                self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)

    def test_invalid_component(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(SOURCE/'scripts/install.py'), '--target', tmp, '--components', 'missing'], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((Path(tmp)/'neckbeard').exists())
