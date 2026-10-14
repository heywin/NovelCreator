#!/usr/bin/env python3
"""Validate collaborative state and measurable release gates; never write approval."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from project_checks import CONTROL_FILES, body_text, inspect, sha256

ROLES = ('supervisor','planner','writer','continuity_editor','literary_editor')
EDITORS = ROLES[-2:]
STATUSES = ('planned','writing','in_review','needs_revision','accepted')
CARD_SECTIONS = ('Purpose','Entry State','Required Beats','Character Constraints',
                 'Relationship Pressure','Timeline And Setting Constraints','Plot Line Movement',
                 'Foreshadowing And Payoff','Narrative Boundary','Forbidden Drift','Exit State',
                 'Post-Draft Update Targets')


def nonempty(value):
    return isinstance(value,str) and bool(value.strip())


def positive(value):
    return type(value) is int and value > 0


def unique_json(pairs):
    result = {}
    for key,value in pairs:
        if key in result: raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def validate(root: Path, stage='release') -> dict:
    errors, warnings = [], []
    result = {'stage':stage,'errors':errors,'warnings':warnings,'metrics':None}
    def fail(message): errors.append(message)
    def finish():
        result['ok'] = not errors
        return result
    if not root.is_dir():
        fail(f'project directory does not exist: {root}'); return finish()
    try:
        workflow = json.loads((root/'workflow.json').read_text(encoding='utf-8'),object_pairs_hook=unique_json)
    except (OSError,UnicodeError,ValueError) as exc:
        fail(f'workflow.json: {exc}. Legacy projects require explicit migration; inspect_project.py is read-only.')
        return finish()
    if not isinstance(workflow,dict) or type(workflow.get('schema_version')) is not int or workflow['schema_version'] != 1:
        fail('workflow schema_version must be 1'); return finish()
    contract = workflow.get('contract')
    if not isinstance(contract,dict):
        fail('contract must be an object'); return finish()
    for key in ('chapters','chapter_min','chapter_max','total_min','total_max'):
        if not positive(contract.get(key)): fail(f'contract.{key} must be a positive integer')
    if contract.get('count_mode') not in ('han','nonspace'): fail('contract.count_mode must be han or nonspace')
    if errors: return finish()
    n = contract['chapters']
    if n > 10000: fail('chapter count exceeds supported 10000')
    if contract['chapter_min'] > contract['chapter_max'] or contract['total_min'] > contract['total_max']:
        fail('length ranges are reversed')
    if max(contract['total_min'],n*contract['chapter_min']) > min(contract['total_max'],n*contract['chapter_max']):
        fail('chapter and total length ranges cannot be satisfied together')
    actors = workflow.get('actors')
    actor_ids = {}
    if not isinstance(actors,dict):
        fail('actors must assign session/person IDs to each of the five roles')
    else:
        for role in ROLES:
            value = actors.get(role)
            ids = [value] if isinstance(value,str) else value
            if not isinstance(ids,list) or not ids or any(not nonempty(x) for x in ids):
                fail(f'actors.{role} needs a nonempty ID or array of IDs')
            else: actor_ids[role] = ids
        all_ids = [actor for ids in actor_ids.values() for actor in ids]
        if len(set(all_ids)) != len(all_ids):
            fail('role session/person IDs must be distinct; writer cannot self-approve')
    for key in ('tasks','reviews','issues','repetition_exceptions'):
        if not isinstance(workflow.get(key),list) or any(not isinstance(x,dict) for x in workflow[key]):
            fail(f'{key} must be an array of objects')
    if errors: return finish()
    tasks, reviews, issues = (workflow[k] for k in ('tasks','reviews','issues'))
    for label,items in (('task',tasks),('review',reviews),('issue',issues)):
        ids = [x.get('id') for x in items]
        if any(not nonempty(x) for x in ids) or len(set(x for x in ids if isinstance(x,str))) != len(ids):
            fail(f'{label} IDs must be unique nonempty strings')
    for task in tasks:
        label = str(task.get('id'))
        if not positive(task.get('chapter')) or task.get('chapter',n+1)>n: fail(f'{label}: invalid chapter')
        if task.get('status') not in STATUSES: fail(f'{label}: invalid status')
        if task.get('writer') not in actor_ids['writer']: fail(f'{label}: writer must match assigned writer actor')
        if not isinstance(task.get('depends_on'),list) or any(not nonempty(x) for x in task['depends_on']):
            fail(f'{label}: depends_on must be a list of task IDs')
        if not isinstance(task.get('scenes'),list) or any(not isinstance(x,dict) for x in task['scenes']):
            fail(f'{label}: scenes must be an array of objects'); continue
        scenes = task['scenes']
        if task.get('status') != 'planned' and not scenes: fail(f'{label}: active task needs scene plans')
        ids = [s.get('id') for s in scenes]
        if any(not nonempty(x) for x in ids) or len(set(x for x in ids if isinstance(x,str))) != len(ids):
            fail(f'{label}: scene IDs must be unique nonempty strings')
        for scene in scenes:
            for key in ('goal','entry_state','conflict','exit_state'):
                if not nonempty(scene.get(key)): fail(f'{label}: scene needs {key}')
            if not positive(scene.get('min')) or not positive(scene.get('max')) or scene.get('min',0)>scene.get('max',0):
                fail(f'{label}: invalid scene length range')
        if scenes and all(positive(s.get('min')) and positive(s.get('max')) for s in scenes):
            if max(sum(s['min'] for s in scenes),contract['chapter_min']) > min(sum(s['max'] for s in scenes),contract['chapter_max']):
                fail(f'{label}: scene budgets cannot satisfy chapter range')
    chapter_numbers = [t.get('chapter') for t in tasks if positive(t.get('chapter'))]
    if sorted(chapter_numbers) != list(range(1,n+1)): fail('tasks must cover each contracted chapter exactly once')
    for review in reviews:
        label = str(review.get('id'))
        if review.get('role') not in EDITORS: fail(f'{label}: invalid review role')
        elif review.get('reviewer') not in actor_ids[review['role']]: fail(f'{label}: reviewer does not match assigned editor')
        scope = review.get('scope')
        if scope != 'book' and (not positive(scope) or scope>n): fail(f'{label}: scope must be chapter number or book')
        if review.get('verdict') not in ('pass','changes_requested'): fail(f'{label}: invalid review verdict')
        if not isinstance(review.get('issues'),list) or any(not nonempty(x) for x in review['issues']): fail(f'{label}: issues must be ID array')
        for key in ('sha256','report'):
            if not nonempty(review.get(key)): fail(f'{label}: missing {key}')
    for issue in issues:
        label = str(issue.get('id'))
        if issue.get('scope') != 'book' and (not positive(issue.get('scope')) or issue.get('scope',n+1)>n): fail(f'{label}: invalid scope')
        if issue.get('severity') not in ('low','medium','high','critical'): fail(f'{label}: invalid severity')
        if issue.get('status') not in ('open','done','deferred'): fail(f'{label}: invalid status')
        for key in ('evidence','repair','raised_by'):
            if not nonempty(issue.get(key)): fail(f'{label}: missing {key}')
        if issue.get('status') == 'done' and not nonempty(issue.get('verified_by')): fail(f'{label}: done issue needs verified_by review ID')
        if issue.get('status') == 'deferred' and not nonempty(issue.get('reason')): fail(f'{label}: deferral needs a reason')
    for item in workflow['repetition_exceptions']:
        if any(not nonempty(item.get(k)) for k in ('sha256','reason','review_id')): fail('repetition exception needs sha256, reason, review_id')
    if errors: return finish()
    task_map = {t['id']:t for t in tasks}
    review_map = {r['id']:r for r in reviews}
    issue_map = {i['id']:i for i in issues}
    for task in tasks:
        for dependency in task['depends_on']:
            if dependency not in task_map: fail(f"{task['id']}: unknown dependency {dependency}")
            elif task['status'] != 'planned' and task_map[dependency]['status'] != 'accepted':
                fail(f"{task['id']}: dependency {dependency} is not accepted")
    # Iterative topological check avoids recursion failure on long serials.
    pending = {t['id']:set(t['depends_on']) for t in tasks}
    while pending:
        ready = {key for key,deps in pending.items() if not deps}
        if not ready:
            fail('task dependencies contain a cycle or unknown task'); break
        pending = {key:deps-ready for key,deps in pending.items() if key not in ready}
    required = list(CONTROL_FILES) + (['QUALITY_REPORT.md'] if stage=='release' else [])
    for name in required:
        path=root/name
        if not path.is_file() or not nonempty(path.read_text(encoding='utf-8')): fail(f'missing or empty required file: {name}')
    metrics = inspect(root)
    result['metrics'] = metrics
    manuscripts = {}
    for c in metrics['chapters']:
        stem = Path(c['file']).stem
        if not re.fullmatch(r'\d+',stem) or int(stem)<1 or int(stem)>n:
            fail(f"unexpected manuscript: {c['file']}"); continue
        number = int(stem)
        if number in manuscripts: fail(f'duplicate manuscript chapter number: {number}')
        manuscripts[number] = c
    cards = {}
    for path in (root/'chapter-cards').glob('*.md'):
        match = re.fullmatch(r'(\d+)-card\.md',path.name)
        if not match or not 1<=int(match[1])<=n:
            fail(f'unexpected chapter card: {path.name}'); continue
        number=int(match[1])
        if number in cards: fail(f'duplicate chapter card number: {number}')
        cards[number]=path
    checked_chapters = {t['chapter'] for t in tasks if t['status'] in ('accepted','in_review')}
    normalized_chapters = {}
    for number, chapter in manuscripts.items():
        normalized = re.sub(r'\s+', '', body_text((root/chapter['file']).read_text(encoding='utf-8')))
        if normalized and normalized in normalized_chapters:
            previous = normalized_chapters[normalized]
            target = errors if stage=='release' or number in checked_chapters or previous in checked_chapters else warnings
            target.append(f'identical chapter bodies: {previous} and {number}')
        normalized_chapters[normalized] = number
    for task in tasks:
        number,status=task['chapter'],task['status']
        check = stage=='release' or status in ('in_review','accepted')
        if status!='planned' or stage=='release':
            if number not in cards: fail(f'chapter {number}: missing chapter card')
            else:
                card=cards[number].read_text(encoding='utf-8')
                for section in CARD_SECTIONS:
                    match=re.search(rf'(?m)^## {re.escape(section)}\s*\n(.*?)(?=^## |\Z)',card,re.S)
                    if not match or not nonempty(match[1]): fail(f'chapter {number}: missing/empty card section {section}')
        if number not in manuscripts:
            if check: fail(f'chapter {number}: missing manuscript')
            continue
        c=manuscripts[number]
        raw=(root/c['file']).read_text(encoding='utf-8')
        problems=[]
        length=c[contract['count_mode']]
        if not contract['chapter_min']<=length<=contract['chapter_max']:
            problems.append(f"length {length} outside {contract['chapter_min']}-{contract['chapter_max']} ({contract['count_mode']})")
        if not any(ch.isalnum() for ch in body_text(raw)): problems.append('manuscript contains no letters/numbers')
        if re.search(r'```|~~~|<!--|<[^>]+>|!?\[[^\]]*\]\([^)]*\)|(?m:^\s*\|)|\*\*|__|`',raw): problems.append('manuscript must be plain paragraphs, not code/HTML/links/tables')
        if re.search(r'作者说明[:：]|本章任务|接下来按章节卡|continuity ledger|line heat|chapter card',raw,re.I): problems.append('possible writing-process leak')
        for message in problems:
            (errors if check else warnings).append(f"chapter {number}: {message}")
        if stage=='release' and status!='accepted': fail(f'chapter {number}: not accepted by supervisor')
        if status=='accepted':
            if task.get('manuscript_sha256')!=c['sha256']: fail(f'chapter {number}: accepted manuscript hash is stale')
            if task.get('accepted_by') not in actor_ids['supervisor']: fail(f'chapter {number}: supervisor acceptance is missing')
    def current_hash(scope):
        return metrics['book_sha256'] if scope=='book' else manuscripts.get(scope,{}).get('sha256')
    def fresh_pass(review):
        return review['verdict']=='pass' and review['sha256']==current_hash(review['scope'])
    def latest(scope,role):
        return next((r for r in reversed(reviews) if r['scope']==scope and r['role']==role),None)
    for review in reviews:
        path=(root/review['report']).resolve()
        if not path.is_relative_to(root.resolve()): fail(f"{review['id']}: review report must stay within project"); continue
        if not path.is_file() or not nonempty(path.read_text(encoding='utf-8')): fail(f"{review['id']}: missing/empty review report")
        for issue_id in review['issues']:
            if issue_id not in issue_map: fail(f"{review['id']}: unknown issue {issue_id}")
        if review['verdict']=='changes_requested' and not review['issues']: fail(f"{review['id']}: requested changes need issue records")
    for issue in issues:
        raised=review_map.get(issue['raised_by'])
        if raised is None or issue['id'] not in raised['issues']: fail(f"{issue['id']}: raising review must reference this issue")
        if issue['status']=='done':
            verified=review_map.get(issue.get('verified_by'))
            if not verified or not fresh_pass(verified) or verified['scope']!=issue['scope'] or (raised and verified['role']!=raised['role']):
                fail(f"{issue['id']}: repair needs a fresh pass from the responsible editor")
            elif reviews.index(verified)<=reviews.index(raised): fail(f"{issue['id']}: verification must follow the finding")
        relevant = stage=='release' or any(t['status']=='accepted' and issue['scope'] in ('book',t['chapter']) for t in tasks)
        if relevant and (issue['status']=='open' or (issue['severity'] in ('high','critical') and issue['status']!='done')):
            fail(f"{issue['id']}: unresolved issue blocks acceptance")
        if issue['status']=='deferred' and issue.get('approved_by') not in actor_ids['supervisor']:
            fail(f"{issue['id']}: deferral requires supervisor record")
    for task in tasks:
        if task['status']=='accepted':
            for role in EDITORS:
                review=latest(task['chapter'],role)
                if not review or not fresh_pass(review): fail(f"chapter {task['chapter']}: missing fresh {role} pass")
    if stage=='release':
        for role in EDITORS:
            review=latest('book',role)
            if not review or not fresh_pass(review): fail(f'missing fresh whole-book {role} pass')
        total=metrics['totals'][contract['count_mode']]
        if not contract['total_min']<=total<=contract['total_max']: fail(f'total length {total} outside contracted range')
    exemptions=set()
    duplicate_hashes={d['sha256'] for d in metrics['duplicates']}
    for item in workflow['repetition_exceptions']:
        review=review_map.get(item['review_id'])
        if item['sha256'] not in duplicate_hashes: fail('repetition exception does not match a current repeated paragraph')
        if not review or review['scope']!='book' or review['role']!='literary_editor' or not fresh_pass(review):
            fail('repetition exception needs a fresh whole-book literary review')
        else: exemptions.add(item['sha256'])
    for duplicate in metrics['duplicates']:
        if duplicate['sha256'] in exemptions: continue
        locations=duplicate['occurrences']
        accepted_paths={manuscripts[t['chapter']]['file'] for t in tasks if t['status'] in ('accepted','in_review') and t['chapter'] in manuscripts}
        target=errors if stage=='release' or any(p['file'] in accepted_paths for p in locations) else warnings
        target.append(f"repeated paragraph ({len(locations)} occurrences): {locations[0]['file']}:{locations[0]['line']} sha256={duplicate['sha256']}")
    if stage=='progress': warnings.append('Progress validation is not release approval; unfinished tasks and drafts may remain.')
    return finish()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project_root',type=Path)
    parser.add_argument('--stage',choices=('progress','release'),default='release')
    parser.add_argument('--json',action='store_true')
    args=parser.parse_args()
    try:
        result=validate(args.project_root.resolve(),args.stage)
    except (OSError,UnicodeError,ValueError) as exc:
        result={'ok':False,'stage':args.stage,'errors':[str(exc)],'warnings':[],'metrics':None}
    if args.json: print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        for level in ('warnings','errors'):
            for message in result[level]: print(f'{level[:-1].upper()}: {message}')
        if result['metrics']: print('Measured totals:',result['metrics']['totals'])
        print(f"{'PASS' if result['ok'] else 'FAILED'} ({args.stage}): {len(result['errors'])} error(s), {len(result['warnings'])} warning(s). Mechanical checks do not certify literary quality.")
    return 0 if result['ok'] else 1

if __name__=='__main__': raise SystemExit(main())
