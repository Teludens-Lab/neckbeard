#!/usr/bin/env python3
"""Validate learning governance, export audit records, check drift and preflight media."""
import argparse
import csv
from datetime import date
import fnmatch
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
import subprocess
import sys

STATES = {'runtime-verified', 'source-supported', 'documentation-only', 'unverified'}


def load(path):
    text = Path(path).read_text(encoding='utf-8')
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml
        except ImportError:
            # Bundled profile uses a YAML comment followed by JSON.
            return json.loads('\n'.join(x for x in text.splitlines() if not x.startswith('#')))
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as exc:
            raise ValueError("Invalid YAML input") from exc


def require(ok, message):
    if not ok:
        raise ValueError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip()) and not any(x in value.upper() for x in ('REPLACE_WITH', 'YYYY-MM-DD'))


def safe_path(value, glob=False):
    require(isinstance(value, str) and value and '\\' not in value, 'Expected nonempty POSIX path')
    p = PurePosixPath(value)
    require(not p.is_absolute() and '..' not in p.parts and not value.startswith('-'), 'Unsafe relative path: ' + value)
    require(glob or not any(c in value for c in '*?['), 'Unexpected glob: ' + value)
    return value


def profile_check(p):
    require(isinstance(p, dict) and p.get('schema_version') == 1, 'Unsupported profile schema')
    for key in ('organization', 'house_style', 'glossary', 'documentation_platform', 'required_templates', 'approved_tools', 'data_classification', 'mandatory_reviewers'):
        require(key in p, 'Missing profile field: ' + key)
    require(nonempty(p['organization']), 'Organization is required')
    require(isinstance(p.get('configured'), bool), 'Configured flag must be boolean')
    require(isinstance(p['house_style'], dict) and nonempty(p['house_style'].get('language')), 'House language required')
    require(isinstance(p['glossary'], dict), 'Glossary must be an object')
    safe_path(p['glossary'].get('path'))
    require(nonempty(p['glossary'].get('source_locale')) and isinstance(p['glossary'].get('target_locales'), list), 'Glossary locales required')
    require(isinstance(p['documentation_platform'], dict) and nonempty(p['documentation_platform'].get('name')), 'Documentation platform required')
    safe_path(p['documentation_platform'].get('root'))
    require(isinstance(p['required_templates'], list) and p['required_templates'], 'At least one required template is required')
    for x in p['required_templates']: safe_path(x)
    require(isinstance(p['mandatory_reviewers'], list) and p['mandatory_reviewers'] and all(nonempty(x) for x in p['mandatory_reviewers']), 'Mandatory reviewers required')
    policy = p['data_classification']
    require(isinstance(policy, dict), 'Classification policy required')
    classes = policy.get('classes')
    require(isinstance(classes, list) and classes and all(nonempty(x) for x in classes), 'Classification classes required')
    require(policy.get('default') in classes, 'Invalid default classification')
    for key in ('external_denied', 'offline_only'):
        require(isinstance(policy.get(key), list) and set(policy[key]) <= set(classes), 'Invalid ' + key)
    require(isinstance(policy.get('require_asset_review'), bool), 'Asset review policy must be boolean')
    require(isinstance(p['approved_tools'], list), 'Approved tools must be a list')
    ids = set()
    for t in p['approved_tools']:
        require(isinstance(t, dict) and nonempty(t.get('id')) and t['id'] not in ids, 'Invalid or duplicate tool')
        ids.add(t['id'])
        require(isinstance(t.get('external'), bool) and isinstance(t.get('personal_data_allowed'), bool), 'Tool mode and personal-data policy must be boolean')
        require(isinstance(t.get('operations'), list) and t['operations'] and set(t['operations']) <= {'capture', 'voice', 'render'}, 'Invalid tool operations')
        require(isinstance(t.get('allowed_classifications'), list) and set(t['allowed_classifications']) <= set(classes), 'Invalid tool classifications')
    require(type(p.get('review_interval_days')) is int and p['review_interval_days'] > 0, 'Positive review interval required')
    return p


def record_check(r, p=None, root=None, release=False, today=None):
    today = today or date.today()
    if release:
        require(p and p.get('configured'), 'A configured organization profile is required for release')
        profile_check(p)
        require(root is not None, 'Release requires an artifact root to verify approved bytes')
    require(isinstance(r, dict) and r.get('schema_version') == 1, 'Unsupported governance schema')
    for k in ('repositories', 'documents', 'evidence', 'media_assets'):
        require(isinstance(r.get(k), list), k + ' must be a list')
    if release: require(r['documents'], 'Release requires at least one document')
    repo_ids = set()
    for repo in r['repositories']:
        require(isinstance(repo, dict) and nonempty(repo.get('id')) and repo['id'] not in repo_ids, 'Invalid or duplicate repository')
        repo_ids.add(repo['id'])
    evidence = {}
    for e in r['evidence']:
        require(isinstance(e, dict), 'Evidence must be an object')
        for k in ('id', 'repository', 'revision', 'path', 'claim', 'method', 'result'):
            require(nonempty(e.get(k)), 'Missing evidence ' + k)
        require(e['id'] not in evidence, 'Duplicate evidence ID')
        require(e['repository'] in repo_ids, 'Unknown evidence repository')
        require(e['result'] in {'passed', 'failed', 'not-run'}, 'Invalid evidence result')
        require(e['method'] in {'runtime', 'source', 'documentation', 'none'}, 'Invalid evidence method')
        require(isinstance(e.get('limitations'), str), 'Evidence limitations must be explicit')
        safe_path(e['path']); evidence[e['id']] = e
    docs = {}
    for d in r['documents']:
        require(isinstance(d, dict), 'Document must be an object')
        for k in ('id', 'path', 'owner', 'source_revision', 'evidence_state', 'reviewer', 'review_by', 'locale'):
            require(nonempty(d.get(k)), 'Missing document ' + k)
        require(d['id'] not in docs, 'Duplicate document ID'); docs[d['id']] = d
        safe_path(d['path'])
        require(d['evidence_state'] in STATES, 'Invalid evidence state')
        review_by = date.fromisoformat(d['review_by'])
        require(isinstance(d.get('sources'), list) and d['sources'], 'Document sources required')
        for source in d['sources']:
            require(source.get('repository') in repo_ids and nonempty(source.get('revision')), 'Unknown source repository or missing revision')
            require(isinstance(source.get('paths'), list) and source['paths'], 'Source paths required')
            for path in source['paths']: safe_path(path, glob=True)
        require(d['source_revision'] == d['sources'][0]['revision'], 'Primary source revision mismatch')
        require(isinstance(d.get('evidence_ids'), list) and d['evidence_ids'] and all(x in evidence for x in d['evidence_ids']), 'Missing or unknown document evidence')
        entries = [evidence[x] for x in d['evidence_ids']]
        for source in d['sources']:
            for pattern in source['paths']:
                require(any(e['repository'] == source['repository'] and e['revision'] == source['revision'] and matches(e['path'], pattern) for e in entries), 'Source mapping lacks matching evidence: ' + pattern)
        for e in entries:
            require(any(e['repository'] == src['repository'] and e['revision'] == src['revision'] and any(matches(e['path'], pat) for pat in src['paths']) for src in d['sources']), 'Evidence is outside document mapping')
        if d['evidence_state'] == 'runtime-verified':
            require(any(e['method'] == 'runtime' and e['result'] == 'passed' for e in entries) and all(e['result'] == 'passed' for e in entries), 'Runtime verification requires passing runtime evidence and no unresolved evidence')
        if d['evidence_state'] == 'source-supported':
            require(any(e['method'] in {'source', 'runtime'} and e['result'] == 'passed' for e in entries), 'Source-supported document lacks passing source evidence')
        if root is not None:
            doc = (Path(root) / d['path']).resolve()
            require(doc.is_relative_to(Path(root).resolve()), 'Document escapes root')
            require(doc.is_file(), 'Document missing: ' + d['path'])
            meta_path = Path(str(doc) + '.metadata.json')
            if doc.suffix.lower() in ('.md', '.markdown'):
                text = doc.read_text(encoding='utf-8')
                require(text.startswith('---\n') and '\n---\n' in text[4:], 'Document YAML metadata missing: ' + d['path'])
                front = text.split('\n---\n', 1)[0][4:]
                try:
                    meta = json.loads(front)
                except json.JSONDecodeError:
                    try:
                        import yaml
                    except ImportError:
                        raise ValueError('Install requirements.txt to read YAML document metadata')
                    meta = yaml.safe_load(front)
            else:
                require(meta_path.is_file(), 'Metadata companion missing: ' + str(meta_path))
                meta = load(meta_path)
            for key in ('owner', 'source_revision', 'evidence_state', 'reviewer', 'review_by', 'locale'):
                require(str(meta.get(key)) == str(d[key]), 'Artifact metadata mismatch: ' + key)
            require(meta.get('document_id') == d['id'], 'Artifact document ID mismatch')
        require(isinstance(d.get('reviews'), list), 'Document reviews list required')
        if release:
            require(all(re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', src['revision']) for src in d['sources']), 'Release requires exact committed source hashes')
            require(not any(x in d['owner'].lower() or x in d['reviewer'].lower() for x in ('unassigned', 'unknown', 'pending')), 'Release requires assigned owner and reviewer')
            require(review_by >= today, 'Review overdue: ' + d['id'])
            require(d['evidence_state'] != 'unverified', 'Unverified document cannot be released')
            require(all(e['result'] != 'failed' for e in entries), 'Failed evidence must be resolved before release: ' + d['id'])
            artifact_sha256 = hashlib.sha256(doc.read_bytes()).hexdigest()
            required = set(p['mandatory_reviewers'] if p else []) | {d['reviewer']}
            decisions = {}
            for rev in d['reviews']:
                require(isinstance(rev, dict) and nonempty(rev.get('reviewer')), 'Invalid review')
                require(rev.get('decision') in {'approved', 'rejected', 'pending'}, 'Invalid review decision')
                review_date = date.fromisoformat(rev['date'])
                require(review_date <= today, 'Review date is in future')
                previous = decisions.get(rev['reviewer'])
                if previous is None or review_date >= previous[0]:
                    decisions[rev['reviewer']] = (review_date, rev)
            approved = {reviewer for reviewer, (_, rev) in decisions.items() if rev['decision'] == 'approved'}
            require(required <= approved, 'Mandatory reviewer approval missing: ' + d['id'])
            for reviewer in required:
                review_date, rev = decisions[reviewer]
                require(rev.get('source_revision') == d['source_revision'], 'Review applies to an old revision')
                require(rev.get('sources') == d['sources'], 'Review must cover all source dependencies')
                require(rev.get('artifact_sha256') == artifact_sha256, 'Artifact changed or approval hash missing: ' + d['id'])
                require(0 <= (review_by - review_date).days <= p['review_interval_days'], 'Review deadline exceeds the policy interval or precedes approval: ' + d['id'])
    for d in docs.values():
        if d.get('translation_of'):
            require(d['translation_of'] in docs and d['translation_of'] != d['id'], 'Unknown translation source')
            original = docs[d['translation_of']]
            require(original['sources'] == d['sources'] and d['locale'] != original['locale'], 'Translation mappings/locale mismatch')
        if p:
            require(isinstance(d.get('templates'), list) and set(p['required_templates']) <= set(d['templates']), 'Required document templates missing')
            locales = [p['glossary']['source_locale']] + p['glossary']['target_locales']
            require(d['locale'] in locales, 'Unconfigured output locale')
    asset_ids = set()
    for a in r['media_assets']:
        require(isinstance(a, dict) and nonempty(a.get('id')) and a['id'] not in asset_ids, 'Invalid or duplicate media asset')
        asset_ids.add(a['id']); safe_path(a.get('path'))
        require(isinstance(a.get('sha256'), str) and len(a['sha256']) == 64 and all(c in '0123456789abcdef' for c in a['sha256']), 'Asset SHA256 required')
        require(nonempty(a.get('classification')), 'Asset classification required')
        for key in ('contains_personal_data', 'sanitized', 'reviewed'):
            require(isinstance(a.get(key), bool), 'Asset ' + key + ' must be boolean')
        require(nonempty(a.get('reviewer')), 'Asset reviewer required')
        if p: require(a['classification'] in p['data_classification']['classes'], 'Unknown asset classification')
    return r


def matches(path, pattern):
    return fnmatch.fnmatchcase(path, pattern) or (pattern.startswith('**/') and fnmatch.fnmatchcase(path, pattern[3:]))


def gate(p, r, tool_id, operation, mode, asset_ids, root):
    profile_check(p); record_check(r, p)
    require(p['configured'], 'Organization profile is still an unconfigured template')
    root = Path(root).resolve()
    tools = [t for t in p['approved_tools'] if t['id'] == tool_id]
    require(len(tools) == 1, 'Tool is not approved')
    tool = tools[0]; policy = p['data_classification']
    require(tool['external'] == (mode == 'external'), 'Tool execution mode mismatch')
    require(operation in tool['operations'], 'Operation is not approved')
    require(asset_ids and len(set(asset_ids)) == len(asset_ids), 'Explicit unique asset IDs required')
    assets = {a['id']: a for a in r['media_assets']}
    for aid in asset_ids:
        require(aid in assets, 'Unknown asset: ' + aid)
        a = assets[aid]; cls = a['classification']
        path = (root / a['path']).resolve()
        require(path.is_relative_to(root) and path.is_file(), 'Asset missing or outside approved root')
        require(hashlib.sha256(path.read_bytes()).hexdigest() == a['sha256'], 'Asset bytes changed since review')
        require(cls in tool['allowed_classifications'], 'Classification not approved for tool')
        if policy['require_asset_review']: require(a['reviewed'], 'Asset review incomplete')
        require(not a['contains_personal_data'] or tool['personal_data_allowed'], 'Personal data not approved for tool')
        if mode == 'external':
            require(cls not in policy['external_denied'] and cls not in policy['offline_only'], 'Classification cannot leave offline environment')
    digest = hashlib.sha256(json.dumps({'profile':p,'assets':[assets[i] for i in asset_ids]}, sort_keys=True).encode()).hexdigest()
    return {'allowed':True,'tool':tool_id,'operation':operation,'mode':mode,'asset_ids':asset_ids,'policy_and_inventory_sha256':digest,'note':'Preflight only; does not sandbox tools or authenticate asset review.'}


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE).decode('utf-8', errors='replace').rstrip('\r\n')


def stale(r, repos, today=None):
    record_check(r); today = today or date.today(); findings = []
    for d in r['documents']:
        if date.fromisoformat(d['review_by']) < today: findings.append({'document':d['id'],'reason':'review-overdue'})
        for src in d['sources']:
            repo = src['repository']
            if repo not in repos:
                findings.append({'document':d['id'],'repository':repo,'reason':'checkout-missing'}); continue
            try:
                root = repos[repo]
                rev = git(root, 'rev-parse', '--verify', src['revision'] + '^{commit}')
                head = git(root, 'rev-parse', 'HEAD')
                git(root, 'merge-base', '--is-ancestor', rev, head)
                changed = git(root, 'diff', '--name-only', '--no-renames', '-z', rev, head).split('\0')
                # Include worktree/index/untracked changes conservatively.
                if git(root, 'status', '--porcelain'):
                    findings.append({'document':d['id'],'repository':repo,'reason':'dirty-checkout'})
                affected = [path for path in changed if path and any(matches(path, pat) for pat in src['paths'])]
                if affected: findings.append({'document':d['id'],'repository':repo,'reason':'source-changed','paths':affected})
            except (subprocess.CalledProcessError, OSError) as exc:
                findings.append({'document':d['id'],'repository':repo,'reason':'revision-unavailable','detail':type(exc).__name__})
    return {'stale':bool(findings),'findings':findings,'coverage':'Only explicitly mapped dependencies are checked.'}


def export(r, out):
    record_check(r); out = Path(out); out.mkdir(parents=True, exist_ok=True)
    (out/'governance.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    tables = {
        'documents':[{k:d[k] for k in ('id','path','owner','source_revision','evidence_state','reviewer','review_by','locale')} for d in r['documents']],
        'evidence':r['evidence'],
        'mapping':[{'document_id':d['id'],'document_path':d['path'],'repository':s['repository'],'revision':s['revision'],'source_path':p,'workflow':d.get('workflow',''),'translation_of':d.get('translation_of','')} for d in r['documents'] for s in d['sources'] for p in s['paths']],
        'media-gate':r.get('gate_receipts',[])
    }
    for name, rows in tables.items():
        keys = sorted(set().union(*(x.keys() for x in rows))) if rows else ['id']
        with (out/(name+'.csv')).open('w',newline='',encoding='utf-8') as f:
            w = csv.DictWriter(f,fieldnames=keys);w.writeheader()
            for row in rows:
                # Neutralize spreadsheet formula interpretation while preserving raw JSON.
                values = {k:json.dumps(v,sort_keys=True) if isinstance(v,(dict,list)) else v for k,v in row.items()}
                w.writerow({k:"'"+v if isinstance(v,str) and v.startswith(('=','+','-','@','\t','\r')) else v for k,v in values.items()})
    lines = ['# Learning governance audit','',f"Documents: {len(r['documents'])}. Evidence records: {len(r['evidence'])}.",'']
    for d in r['documents']:
        lines += [f"- {d['id']}: owner {d['owner']}; {d['evidence_state']}; reviewer {d['reviewer']}; review by {d['review_by']}."]
        for src in d['sources']: lines += [f"  - Source {src['repository']} at {src['revision']}: {', '.join(src['paths'])}."]
        for eid in d['evidence_ids']:
            e = next(e for e in r['evidence'] if e['id']==eid)
            lines += [f"  - Evidence {eid}: {e['claim']} — {e['method']}, {e['result']}. Limits: {e['limitations'] or 'none recorded'}."]
    (out/'audit.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command',choices=['profile','validate','export','stale','gate'])
    ap.add_argument('--profile',type=Path);ap.add_argument('--record',type=Path);ap.add_argument('--root',type=Path)
    ap.add_argument('--release',action='store_true');ap.add_argument('--out',type=Path)
    ap.add_argument('--repo',action='append',default=[]);ap.add_argument('--tool');ap.add_argument('--operation',choices=['capture','voice','render'])
    ap.add_argument('--mode',choices=['offline','external'],default='offline');ap.add_argument('--assets',nargs='+')
    args=ap.parse_args()
    try:
        p=profile_check(load(args.profile)) if args.profile else None
        if args.command=='profile':require(p is not None,'--profile required');result={'valid':True}
        else:
            require(args.record is not None,'--record required');r=load(args.record)
            if args.command=='validate':
                require(p is not None and args.root is not None,'--profile and --root required')
                record_check(r,p,args.root,args.release)
                glossary_path=(args.profile.parent/p['glossary']['path']).resolve()
                require(glossary_path.is_relative_to(args.profile.parent.resolve()),'Glossary escapes profile directory')
                glossary=load(glossary_path);require(isinstance(glossary,dict) and glossary.get('schema_version')==1 and isinstance(glossary.get('terms'),list),'Invalid glossary')
                ids=set()
                for term in glossary['terms']:
                    require(nonempty(term.get('id')) and term['id'] not in ids and nonempty(term.get('source')) and nonempty(term.get('definition')),'Invalid glossary term');ids.add(term['id'])
                    require(isinstance(term.get('translations'),dict) and isinstance(term.get('do_not_translate'),bool),'Invalid glossary translations')
                    if args.release and not term['do_not_translate']:
                        used={d['locale'] for d in r['documents']} - {p['glossary']['source_locale']}
                        require(all(nonempty(term['translations'].get(locale)) for locale in used),'Missing approved glossary translation')
                result={'valid':True,'release':args.release}
            elif args.command=='export':require(args.out is not None,'--out required');export(r,args.out);result={'exported':str(args.out)}
            elif args.command=='stale':
                repos={}
                for item in args.repo:
                    key,sep,path=item.partition('=');require(sep and key and path and key not in repos,'Use unique --repo ID=CHECKOUT');repos[key]=Path(path)
                result=stale(r,repos)
            else:
                require(p is not None and args.tool and args.operation and args.root is not None,'--profile, --tool, --operation and --root required')
                result=gate(p,r,args.tool,args.operation,args.mode,args.assets,args.root)
        print(json.dumps(result,indent=2));return 1 if result.get('stale') else 0
    except (ValueError,KeyError,TypeError,OSError,AttributeError) as exc:
        print(json.dumps({'error':str(exc),'allowed':False}));return 2

if __name__=='__main__':sys.exit(main())
