import copy
from datetime import date, timedelta
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SOURCE=Path(__file__).resolve().parents[1]/'skills/neckbeard'
spec=importlib.util.spec_from_file_location('governance',SOURCE/'scripts/governance.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def profile():
    p=g.load(SOURCE/'org-profile.yaml');p['configured']=True;p['organization']='Fixture organization';return p

def record(revision='a'*40):
    return {'schema_version':1,'repositories':[{'id':'product'},{'id':'api'}], 'documents':[{'id':'first-task','path':'guide.md','owner':'learning-team','source_revision':revision,'evidence_state':'source-supported','reviewer':'documentation-owner','review_by':'2099-01-01','locale':'en','sources':[{'repository':'product','revision':revision,'paths':['app.py']}],'evidence_ids':['e1'],'reviews':[],'templates':['references/governed-document.md']}], 'evidence':[{'id':'e1','repository':'product','revision':revision,'path':'app.py','claim':'Only participants submit','method':'source','result':'passed','limitations':'No runtime verification'}],'media_assets':[]}

def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.STDOUT).decode().strip()
def init(root):
    git(root,'init','-q');git(root,'config','user.name','Fixture');git(root,'config','user.email','fixture@example.invalid')
def commit(root):git(root,'add','.');git(root,'commit','-qm','fixture');return git(root,'rev-parse','HEAD')

TODAY = date(2026, 11, 12)

def approved_record(root, suffix='.md'):
    r=record();d=r['documents'][0];d['path']='guide'+suffix
    d['owner']=d['reviewer']='documentation-owner'
    d['review_by']=(TODAY+timedelta(days=90)).isoformat()
    meta={k:d[k] for k in ('owner','source_revision','evidence_state','reviewer','review_by','locale')};meta['document_id']=d['id']
    path=root/d['path']
    if suffix=='.md':path.write_text('---\n'+json.dumps(meta)+'\n---\n# Approved guide\n',encoding='utf-8')
    else:
        path.write_bytes(b'Approved artifact')
        Path(str(path)+'.metadata.json').write_text(json.dumps(meta),encoding='utf-8')
    d['reviews']=[{'reviewer':d['reviewer'],'decision':'approved','date':TODAY.isoformat(),
        'source_revision':d['source_revision'],'sources':copy.deepcopy(d['sources']),
        'artifact_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}]
    return r

class GovernanceTests(unittest.TestCase):
    def test_profile_and_missing_policy(self):
        g.profile_check(profile());p=profile();del p['approved_tools']
        with self.assertRaises(ValueError):g.profile_check(p)
    def test_evidence_cannot_overclaim_runtime(self):
        r=record();g.record_check(r,profile());r['documents'][0]['evidence_state']='runtime-verified'
        with self.assertRaises(ValueError):g.record_check(r)
        r['evidence'][0].update(method='runtime',limitations='');g.record_check(r)
    def test_release_requires_complete_current_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=profile();r=approved_record(root);d=r['documents'][0]
            g.record_check(r,p,root,release=True,today=TODAY)
            approval=d['reviews'].pop()
            with self.assertRaisesRegex(ValueError,'approval missing'):g.record_check(r,p,root,release=True,today=TODAY)
            d['reviews'].append(approval)
            d['reviews'].append(dict(d['reviews'][0],decision='rejected'))
            with self.assertRaisesRegex(ValueError,'approval missing'):g.record_check(r,p,root,release=True,today=TODAY)
            d['reviews'].pop()
            d['reviews'][0]['sources'][0]['revision']='old'
            with self.assertRaisesRegex(ValueError,'all source dependencies'):g.record_check(r,p,root,release=True,today=TODAY)

    def test_release_binds_approval_to_bytes_and_allows_owner_renewal(self):
        for suffix in ('.md','.html','.pdf'):
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);r=approved_record(root,suffix);d=r['documents'][0];path=root/d['path']
                g.record_check(r,profile(),root,release=True,today=TODAY)
                path.write_bytes(path.read_bytes()+b'\nChanged instructions')
                with self.assertRaisesRegex(ValueError,'Artifact changed'):g.record_check(r,profile(),root,release=True,today=TODAY)
                d['reviews'].append(dict(d['reviews'][0],artifact_sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
                g.record_check(r,profile(),root,release=True,today=TODAY)
                del d['reviews'][-1]['artifact_sha256']
                with self.assertRaisesRegex(ValueError,'approval hash missing'):g.record_check(r,profile(),root,release=True,today=TODAY)

    def test_release_rejects_failed_evidence_in_every_releasable_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for state in ('source-supported','documentation-only','runtime-verified'):
                with self.subTest(state=state):
                    r=approved_record(root);d=r['documents'][0];d['evidence_state']=state
                    path=root/d['path'];path.write_text(path.read_text(encoding='utf-8').replace('source-supported',state),encoding='utf-8')
                    d['reviews'][0]['artifact_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
                    r['evidence'].append(dict(r['evidence'][0],id='failed-command',method='runtime',result='failed'))
                    d['evidence_ids'].append('failed-command')
                    with self.assertRaisesRegex(ValueError,'Failed evidence|Runtime verification'):g.record_check(r,profile(),root,release=True,today=TODAY)

    def test_release_requires_artifact_root_and_nonempty_package(self):
        empty={'schema_version':1,'repositories':[],'documents':[],'evidence':[],'media_assets':[]}
        g.record_check(empty)
        with self.assertRaisesRegex(ValueError,'artifact root'):g.record_check(empty,profile(),release=True,today=TODAY)
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError,'at least one document'):g.record_check(empty,profile(),Path(tmp),release=True,today=TODAY)

    def test_release_enforces_review_interval_and_latest_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);r=approved_record(root);d=r['documents'][0];rev=d['reviews'][0]
            g.record_check(r,profile(),root,release=True,today=TODAY)
            g.record_check(r,profile(),root,release=True,today=TODAY+timedelta(days=90))
            rev['date']=(TODAY-timedelta(days=1)).isoformat()
            with self.assertRaisesRegex(ValueError,'policy interval'):g.record_check(r,profile(),root,release=True,today=TODAY)
            rev['date']='2020-01-01'
            with self.assertRaisesRegex(ValueError,'policy interval'):g.record_check(r,profile(),root,release=True,today=TODAY)
            d['reviews'].append(dict(rev,date=TODAY.isoformat()))
            g.record_check(r,profile(),root,release=True,today=TODAY)
            d['reviews'][-1]['date']=(TODAY+timedelta(days=1)).isoformat()
            with self.assertRaisesRegex(ValueError,'future'):g.record_check(r,profile(),root,release=True,today=TODAY)
            d['reviews'][-1]['date']=TODAY.isoformat()
            with self.assertRaisesRegex(ValueError,'overdue'):g.record_check(r,profile(),root,release=True,today=TODAY+timedelta(days=91))

    def test_release_cli_rejects_empty_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=profile();p['glossary']['path']='glossary.json'
            (root/'profile.json').write_text(json.dumps(p))
            (root/'glossary.json').write_text(json.dumps({'schema_version':1,'terms':[]}))
            (root/'record.json').write_text(json.dumps({'schema_version':1,'repositories':[],'documents':[],'evidence':[],'media_assets':[]}))
            result=subprocess.run([sys.executable,str(SOURCE/'scripts/governance.py'),'validate','--release','--profile',str(root/'profile.json'),'--record',str(root/'record.json'),'--root',str(root)],capture_output=True,text=True)
            self.assertEqual(result.returncode,2,result.stderr)
            self.assertFalse(json.loads(result.stdout)['allowed'])
            self.assertIn('at least one document',json.loads(result.stdout)['error'])
    def test_metadata_and_exports(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);r=record();d=r['documents'][0]
            meta={k:d[k] for k in ('owner','source_revision','evidence_state','reviewer','review_by','locale')};meta['document_id']=d['id']
            (root/'guide.md').write_text('---\n'+json.dumps(meta)+'\n---\n# First task\n')
            g.record_check(r,profile(),root);g.export(r,root/'audit')
            for f in ('governance.json','mapping.csv','evidence.csv','documents.csv','audit.md'):self.assertTrue((root/'audit'/f).is_file())
            (root/'guide.md').write_text('# no metadata')
            with self.assertRaises(ValueError):g.record_check(r,profile(),root)
    def test_missing_repository_is_not_clean(self):
        result=g.stale(record(),{});self.assertTrue(result['stale']);self.assertEqual(result['findings'][0]['reason'],'checkout-missing')
    def test_actual_git_drift_and_multiple_repositories(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=Path(tmp)/'product';b=Path(tmp)/'api';a.mkdir();b.mkdir()
            for root,filename in ((a,'app.py'),(b,'policy.py')):init(root);(root/filename).write_text('initial\n');commit(root)
            r=record(git(a,'rev-parse','HEAD'));rev=git(b,'rev-parse','HEAD');r['documents'][0]['sources'].append({'repository':'api','revision':rev,'paths':['policy.py']});r['evidence'].append(dict(r['evidence'][0],id='e2',repository='api',revision=rev,path='policy.py'));r['documents'][0]['evidence_ids'].append('e2')
            self.assertFalse(g.stale(r,{'product':a,'api':b})['stale'])
            (b/'policy.py').write_text('changed\n');commit(b)
            result=g.stale(r,{'product':a,'api':b});self.assertEqual(result['findings'][0]['repository'],'api');self.assertEqual(result['findings'][0]['paths'],['policy.py'])
            # Deleted mapped files are flagged too.
            (a/'app.py').unlink();commit(a);self.assertTrue(any(x.get('repository')=='product' for x in g.stale(r,{'product':a,'api':b})['findings']))
    def test_review_due_and_unknown_revision(self):
        r=record();r['documents'][0]['review_by']='2000-01-01';self.assertEqual(g.stale(r,{})['findings'][0]['reason'],'review-overdue')
    def test_localization_mapping(self):
        r=record();d=copy.deepcopy(r['documents'][0]);d.update(id='translated',path='translated.md',locale='xh',translation_of='first-task');r['documents'].append(d);p=profile();p['glossary']['target_locales']=['xh'];g.record_check(r,p)
        d['sources'][0]['revision']='other'
        with self.assertRaises(ValueError):g.record_check(r,p)
    def test_media_gate_public_offline_external_and_asset_tamper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'narration.txt').write_text('Synthetic demonstration only.');p=profile();r=record();a={'id':'voice','path':'narration.txt','sha256':hashlib.sha256((root/'narration.txt').read_bytes()).hexdigest(),'classification':'public','contains_personal_data':False,'sanitized':True,'reviewed':True,'reviewer':'documentation-owner'};r['media_assets']=[a]
            self.assertTrue(g.gate(p,r,'local-tools','voice','offline',['voice'],root)['allowed'])
            with self.assertRaises(ValueError):g.gate(p,r,'cloud','voice','external',['voice'],root)
            p['approved_tools'].append({'id':'cloud','external':True,'operations':['voice'],'allowed_classifications':['public','confidential'],'personal_data_allowed':False})
            self.assertTrue(g.gate(p,r,'cloud','voice','external',['voice'],root)['allowed'])
            a['classification']='confidential'
            with self.assertRaises(ValueError):g.gate(p,r,'cloud','voice','external',['voice'],root)
            a['classification']='public';a['contains_personal_data']=True
            with self.assertRaises(ValueError):g.gate(p,r,'cloud','voice','external',['voice'],root)
            a['contains_personal_data']=False;a['reviewed']=False
            with self.assertRaises(ValueError):g.gate(p,r,'local-tools','voice','offline',['voice'],root)
            a['reviewed']=True;(root/'narration.txt').write_text('Changed after review')
            with self.assertRaises(ValueError):g.gate(p,r,'local-tools','voice','offline',['voice'],root)
    def test_unconfigured_profile_cannot_approve_media(self):
        p=profile();p['configured']=False
        with self.assertRaises(ValueError):g.gate(p,record(),'local-tools','voice','offline',['a'],'.')
    def test_unsafe_paths_are_rejected(self):
        r=record();r['documents'][0]['sources'][0]['paths']=['../secret']
        with self.assertRaises(ValueError):g.record_check(r)
    def test_dirty_and_unknown_revision_are_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);init(root);(root/'app.py').write_text('initial');rev=commit(root);r=record(rev)
            (root/'app.py').write_text('local edit');self.assertEqual(g.stale(r,{'product':root})['findings'][0]['reason'],'dirty-checkout')
            r['documents'][0]['sources'][0]['revision']='b'*40;r['documents'][0]['source_revision']='b'*40;r['evidence'][0]['revision']='b'*40
            self.assertEqual(g.stale(r,{'product':root})['findings'][0]['reason'],'revision-unavailable')
    def test_classified_offline_and_tool_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'input.txt').write_text('Synthetic classified example')
            p=profile();p['approved_tools'][0]['allowed_classifications'].append('classified');r=record();r['media_assets']=[{'id':'a','path':'input.txt','sha256':hashlib.sha256((root/'input.txt').read_bytes()).hexdigest(),'classification':'classified','contains_personal_data':False,'sanitized':True,'reviewed':True,'reviewer':'documentation-owner'}]
            self.assertTrue(g.gate(p,r,'local-tools','voice','offline',['a'],root)['allowed'])
            with self.assertRaises(ValueError):g.gate(p,r,'local-tools','voice','external',['a'],root)
    def test_cli_machine_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            f=Path(tmp)/'record.json';f.write_text(json.dumps(record()));p=subprocess.run([sys.executable,str(SOURCE/'scripts/governance.py'),'stale','--record',str(f)],capture_output=True,text=True)
            self.assertEqual(p.returncode,1);self.assertTrue(json.loads(p.stdout)['stale'])
