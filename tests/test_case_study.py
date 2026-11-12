from datetime import date
import importlib.util
import hashlib
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('governance', ROOT/'skills/neckbeard/scripts/governance.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


class PlenumCaseStudyTests(unittest.TestCase):
    def test_fractured_order_package_uses_its_own_deployment_and_finished_formats(self):
        package = ROOT/'docs/case-studies/fractured-order'
        profile = g.profile_check(g.load(ROOT/'.neckbeard/org-profile.yaml'))
        record = g.load(package/'governance.json')
        g.record_check(record, profile, ROOT, release=True, today=date(2026, 11, 12))
        self.assertEqual(record['repositories'][0]['url'], 'https://github.com/ssgwm25/Fractured-Order')
        self.assertTrue(all(d['source_revision'] == '10647dd33143fa0ffaea4b4f84c2f2fdbcbb1469' for d in record['documents']))
        self.assertTrue((package/'participant-guide.pdf').read_bytes().startswith(b'%PDF-'))
        self.assertEqual((package/'blue-scribe.mp4').read_bytes()[4:8], b'ftyp')
        self.assertGreater((package/'blue-scribe.mp3').stat().st_size, 10000)
        self.assertTrue((package/'blue-scribe.vtt').read_text(encoding='utf-8').startswith('WEBVTT'))
        self.assertEqual(len((package/'observations.csv').read_text(encoding='utf-8').splitlines()), 1)
        receipt = g.load(package/'blue-scribe.render.json')
        for path, digest in receipt['inputs'].items():
            self.assertNotIn('\\', path, 'Render receipts must use portable repository-relative paths')
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(), digest)
        for suffix, digest in receipt['outputs'].items():
            self.assertEqual(hashlib.sha256((package/('blue-scribe'+suffix)).read_bytes()).hexdigest(), digest)

    def test_recorded_owner_authorized_package(self):
        package = ROOT/'docs/case-studies/plenum'
        profile = g.profile_check(g.load(ROOT/'.neckbeard/org-profile.yaml'))
        record = g.load(package/'governance.json')
        # Historical package integrity is deterministic; the release CLI checks today's deadline.
        g.record_check(record, profile, ROOT, release=True, today=date(2026, 11, 12))
        provenance = g.load(package/'provenance.json')
        expected_paths = {item['path'] for item in provenance['files']}
        for document in record['documents']:
            self.assertEqual(document['owner'], document['reviewer'])
            self.assertEqual(document['evidence_state'], 'source-supported')
            self.assertEqual(document['source_revision'], provenance['revision'])
            self.assertEqual(set(document['sources'][0]['paths']), expected_paths)
            self.assertEqual({review['reviewer'] for review in document['reviews']}, {document['owner']})
        self.assertTrue(all(e['method'] == 'source' for e in record['evidence']))
        self.assertEqual(len((package/'observations.csv').read_text(encoding='utf-8').splitlines()), 1)

    def test_overview_media_matches_recorded_assets(self):
        package = ROOT/'docs/case-studies/plenum'
        provenance = g.load(package/'provenance.json')
        for asset in provenance['media_assets']:
            with self.subTest(path=asset['path']):
                self.assertEqual(hashlib.sha256((ROOT/asset['path']).read_bytes()).hexdigest(), asset['sha256'])
        srt = (ROOT/'docs/assets/neckbeard-overview.srt').read_text(encoding='utf-8')
        vtt = (package/'neckbeard-overview.vtt').read_text(encoding='utf-8')
        self.assertTrue(vtt.startswith('WEBVTT\n\n'))
        expected = re.sub(r'(\d{2}:\d{2}:\d{2}),(\d{3})', r'\1.\2', srt)
        self.assertEqual(vtt, 'WEBVTT\n\n' + expected)
