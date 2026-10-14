"""Regression checks for collaboration gates; all manuscripts are disposable.

Run: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s verification -v
"""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/longform-fiction-studio/scripts'
sys.path.insert(0, str(SCRIPTS))
from project_checks import CONTROL_FILES, count_text, inspect, sha256, snapshot
from validate_project import CARD_SECTIONS, EDITORS, ROLES, validate


CHAPTERS = (
    '雨停的时候，林青终于走到了旧邮局门前。门上的铜锁已经换过，玻璃后面却还贴着父亲写下的营业时间。她把信封从衣袋里拿出来，沿着封口摸了一遍，决定先去找那位退休的投递员。\n\n'
    '老人正在院子里收晒干的豆子，听见名字便停住了手。他没有接信，只让她到屋里坐下。桌上的茶已经凉了，林青等到街口最后一声车铃消失，才问起那场没有人肯说清的夜雨。',
    '码头的货船迟迟没有靠岸，许远站在售票窗外，看着水面浮起的木片。他认出了木片上蓝色的油漆，那是仓库侧门独有的颜色。守门人说昨天没人来过，他却在台阶边看见了一串新鲜的泥脚印。\n\n'
    '许远没有立刻揭穿对方。他绕到屋后，将湿透的账页摊在石头上，等风吹开粘连的纸角。数字下面露出一个陌生的签名。他原本准备交给警方的证据，现在牵连到了一个曾经救过自己的人。',
    '天亮之前，陈默把最后一箱旧书搬上卡车。母亲留在门边，手里攥着一枚已经生锈的钥匙。谁也没有提起搬走以后是否还会回来，只有厨房的水龙头不停滴水，把漫长的沉默分成细小的间隔。\n\n'
    '车子发动时，他忽然看见邻家的女孩从巷口追来。她递进车窗的并非告别礼物，而是一张写着地址的纸条。陈默读完后叫司机停下，转身望向母亲。她慢慢松开了手，那枚钥匙落在了门槛上。',
)


class ProjectValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory(prefix='novel-validation-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for directory in ('chapters', 'chapter-cards', 'reviews'):
            (self.root / directory).mkdir()
        for filename in (*CONTROL_FILES, 'QUALITY_REPORT.md'):
            (self.root / filename).write_text('# 项目记录\n\n已核对的故事事实与编辑结论。\n', encoding='utf-8')
        for number, prose in enumerate(CHAPTERS, 1):
            (self.root / f'chapters/{number:02d}.md').write_text(f'# 第{number}章\n\n{prose}\n', encoding='utf-8')
            (self.root / f'chapter-cards/{number:02d}-card.md').write_text(
                '\n\n'.join(f'## {heading}\n\n本章必须兑现的具体情节和边界。' for heading in CARD_SECTIONS),
                encoding='utf-8')
        lengths = [count_text(p, 'han') for p in CHAPTERS]
        self.workflow = {
            'schema_version': 1,
            'contract': {'chapters': 3, 'count_mode': 'han', 'chapter_min': min(lengths)-5,
                         'chapter_max': max(lengths)+30, 'total_min': sum(lengths)-5,
                         'total_max': sum(lengths)+90},
            'actors': {role: f'session-{role}' for role in ROLES},
            'tasks': [], 'reviews': [], 'issues': [], 'repetition_exceptions': [],
        }
        for number in range(1, 4):
            self.workflow['tasks'].append({
                'id': f'chapter-{number:02d}', 'chapter': number, 'status': 'accepted',
                'writer': self.workflow['actors']['writer'],
                'depends_on': [f'chapter-{number-1:02d}'] if number > 1 else [],
                'accepted_by': self.workflow['actors']['supervisor'],
                'scenes': [{'id': f'scene-{number}', 'goal': '取得线索', 'entry_state': '尚不知真相',
                            'conflict': '证人与主人公利益冲突', 'exit_state': '获得线索并承担后果',
                            'min': min(lengths)-5, 'max': max(lengths)+30}],
            })
            for role in EDITORS:
                self.add_review(number, role)
        for role in EDITORS:
            self.add_review('book', role)
        self.refresh_hashes()

    def add_review(self, scope, role, *, verdict='pass', issues=None, identifier=None):
        identifier = identifier or f'{scope}-{role}'
        report = f'reviews/{identifier}.md'
        (self.root / report).write_text('# 审读记录\n\n已逐段核对正文、因果与人物状态。\n', encoding='utf-8')
        record = {'id': identifier, 'scope': scope, 'role': role,
                  'reviewer': self.workflow['actors'][role], 'verdict': verdict,
                  'issues': issues or [], 'report': report, 'sha256': ''}
        self.workflow['reviews'].append(record)
        return record

    def refresh_hashes(self):
        for task in self.workflow['tasks']:
            path = self.root / f"chapters/{task['chapter']:02d}.md"
            if path.is_file():
                task['manuscript_sha256'] = sha256(path.read_text(encoding='utf-8'))
        for review in self.workflow['reviews']:
            path = self.root / f"chapters/{review['scope']:02d}.md" if type(review['scope']) is int else None
            review['sha256'] = snapshot(self.root) if path is None else sha256(path.read_text(encoding='utf-8'))

    def save(self):
        (self.root / 'workflow.json').write_text(json.dumps(self.workflow, ensure_ascii=False), encoding='utf-8')

    def check(self, stage='release'):
        self.save()
        return validate(self.root, stage)

    def assert_rejected(self, stage='release'):
        result = self.check(stage)
        self.assertFalse(result['ok'], result)
        self.assertTrue(result['errors'], result)
        return result

    def issue_fixture(self, status='done', severity='high'):
        finding = self.add_review(1, 'continuity_editor', verdict='changes_requested',
                                  issues=['issue-1'], identifier='initial-finding')
        self.workflow['reviews'].remove(finding)
        self.workflow['reviews'].insert(0, finding)
        issue = {'id': 'issue-1', 'scope': 1, 'severity': severity, 'status': status,
                 'evidence': 'chapters/01.md:3 人物知识与时间线不符',
                 'repair': '补足人物取得信息的场景', 'raised_by': finding['id'],
                 'verified_by': '1-continuity_editor'}
        self.workflow['issues'].append(issue)
        self.refresh_hashes()
        return issue

    def repetition_fixture(self):
        repeated = CHAPTERS[0].split('\n\n')[0]
        path = self.root / 'chapters/02.md'
        path.write_text(path.read_text(encoding='utf-8') + '\n\n' + repeated + '\n', encoding='utf-8')
        self.workflow['contract']['chapter_max'] += 200
        self.workflow['contract']['total_max'] += 200
        for task in self.workflow['tasks']:
            task['scenes'][0]['max'] += 200
        self.refresh_hashes()
        duplicate = inspect(self.root)['duplicates'][0]
        exception = {'sha256': duplicate['sha256'], 'reason': '两位人物读到同一封信，保留全文回环。',
                     'review_id': 'book-literary_editor'}
        self.workflow['repetition_exceptions'].append(exception)
        return exception

    def test_count_modes_exclude_headings_and_whitespace(self):
        sample = '# 标题不算字数\n\n汉 字，A1！\n\n---\n\n𠀀。\n'
        self.assertEqual(count_text(sample, 'han'), 3)
        self.assertEqual(count_text(sample, 'nonspace'), 8)

    def test_three_chapter_project_passes_without_mutation(self):
        self.save()
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result = validate(self.root)
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['metrics']['totals']['han'], sum(count_text(p, 'han') for p in CHAPTERS))
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_copied_chapters_fail_even_with_fresh_reviews(self):
        for number in (2, 3):
            (self.root / f'chapters/{number:02d}.md').write_text(CHAPTERS[0], encoding='utf-8')
        self.refresh_hashes()
        result = self.assert_rejected()
        self.assertGreater(result['metrics']['repetition_ratio'], 0.5)

    def test_punctuation_cannot_satisfy_nonspace_contract(self):
        self.workflow['contract'].update(count_mode='nonspace', chapter_min=100, chapter_max=500,
                                         total_min=300, total_max=1500)
        for number in range(1, 4):
            (self.root / f'chapters/{number:02d}.md').write_text('。！？'[number-1] * 150, encoding='utf-8')
        self.refresh_hashes()
        self.assert_rejected()

    def test_changed_text_invalidates_acceptance_and_reviews(self):
        path = self.root / 'chapters/01.md'
        path.write_text(path.read_text(encoding='utf-8').replace('林青', '林清'), encoding='utf-8')
        self.assert_rejected()

    def test_stale_accepted_hash_fails_independently(self):
        self.workflow['tasks'][0]['manuscript_sha256'] = '0' * 64
        self.assert_rejected()

    def test_stale_chapter_review_fails_independently(self):
        self.workflow['reviews'][0]['sha256'] = '0' * 64
        self.assert_rejected()

    def test_truth_change_invalidates_final_book_review(self):
        before = snapshot(self.root)
        (self.root / '03-timeline.md').write_text('新时间线：证人在事件之前已离开城市。', encoding='utf-8')
        self.assertNotEqual(snapshot(self.root), before)
        self.assert_rejected()

    def test_card_change_invalidates_final_book_review(self):
        path = self.root / 'chapter-cards/01-card.md'
        path.write_text(path.read_text(encoding='utf-8') + '\n新的限制：此时不能公开证人姓名。\n', encoding='utf-8')
        self.assert_rejected()

    def test_bookkeeping_does_not_invalidate_book_snapshot(self):
        before = snapshot(self.root)
        (self.root / '09-literary-revision.md').write_text('补充了修订记录。', encoding='utf-8')
        self.assertEqual(snapshot(self.root), before)
        self.assertTrue(self.check()['ok'])

    def test_missing_review_report_fails(self):
        (self.root / self.workflow['reviews'][0]['report']).unlink()
        self.assert_rejected()

    def test_review_report_cannot_escape_project(self):
        self.workflow['reviews'][0]['report'] = '../outside-review.md'
        self.assert_rejected()

    def test_severe_issue_cannot_be_deferred_by_supervisor(self):
        issue = self.issue_fixture(status='deferred')
        issue.update(reason='下次再修', approved_by=self.workflow['actors']['supervisor'])
        self.assert_rejected()

    def test_done_issue_with_later_fresh_responsible_review_passes(self):
        self.issue_fixture()
        result = self.check()
        self.assertTrue(result['ok'], result)

    def test_done_issue_cannot_be_verified_by_writer(self):
        self.issue_fixture()
        self.workflow['reviews'][1]['reviewer'] = self.workflow['actors']['writer']
        self.assert_rejected()

    def test_done_issue_requires_responsible_editor(self):
        self.issue_fixture()['verified_by'] = '1-literary_editor'
        self.assert_rejected()

    def test_done_issue_requires_later_review(self):
        self.issue_fixture()
        self.workflow['reviews'].insert(2, self.workflow['reviews'].pop(0))
        self.assert_rejected()

    def test_done_issue_requires_fresh_review(self):
        self.issue_fixture()
        self.workflow['reviews'][1]['sha256'] = '0' * 64
        self.assert_rejected()

    def test_latest_failed_review_supersedes_old_pass(self):
        issue = self.issue_fixture(status='deferred', severity='low')
        issue.update(reason='保留悬念', approved_by=self.workflow['actors']['supervisor'])
        self.add_review(1, 'continuity_editor', verdict='changes_requested',
                        issues=[issue['id']], identifier='later-failure')
        self.refresh_hashes()
        self.assert_rejected()

    def test_dependency_cycle_fails(self):
        self.workflow['tasks'][0]['depends_on'] = ['chapter-03']
        self.assert_rejected()

    def test_active_task_requires_accepted_dependency(self):
        self.workflow['tasks'][0]['status'] = 'in_review'
        self.assert_rejected('progress')

    def test_missing_whole_book_review_blocks_release(self):
        self.workflow['reviews'] = [r for r in self.workflow['reviews'] if r['scope'] != 'book']
        self.assert_rejected()

    def test_latest_failed_whole_book_review_blocks_release(self):
        self.add_review('book', 'literary_editor', verdict='changes_requested',
                        issues=['book-issue'], identifier='book-latest')
        self.workflow['issues'].append({
            'id': 'book-issue', 'scope': 'book', 'severity': 'low', 'status': 'deferred',
            'evidence': '全书中段节奏尚待优化', 'repair': '调整章节间的转场',
            'raised_by': 'book-latest', 'reason': '暂缓',
            'approved_by': self.workflow['actors']['supervisor'],
        })
        self.refresh_hashes()
        self.assert_rejected()

    def test_infeasible_total_range_fails(self):
        contract = self.workflow['contract']
        contract['total_min'] = contract['chapter_max'] * 3 + 1
        contract['total_max'] = contract['total_min'] + 10
        self.assert_rejected()

    def test_infeasible_scene_budget_fails(self):
        self.workflow['tasks'][0]['scenes'][0].update(min=1, max=2)
        self.assert_rejected()

    def test_duplicate_chapter_number_fails(self):
        (self.root / 'chapters/1.md').write_text(CHAPTERS[0], encoding='utf-8')
        self.refresh_hashes()
        self.assert_rejected()

    def test_uncontracted_extra_chapter_fails(self):
        (self.root / 'chapters/04.md').write_text('额外章节正文。', encoding='utf-8')
        self.refresh_hashes()
        self.assert_rejected()

    def test_missing_chapter_fails(self):
        (self.root / 'chapters/02.md').unlink()
        self.assert_rejected()

    def test_total_minimum_enforced_even_when_chapters_pass(self):
        actual = inspect(self.root)['totals']['han']
        self.workflow['contract']['total_min'] = actual + 1
        self.assert_rejected()

    def test_missing_card_section_fails(self):
        (self.root / 'chapter-cards/01-card.md').write_text('# 空章节卡\n', encoding='utf-8')
        self.assert_rejected()

    def test_empty_canonical_control_fails(self):
        (self.root / '01-cast-bible.md').write_text(' \n', encoding='utf-8')
        self.refresh_hashes()
        self.assert_rejected()

    def test_process_notes_in_manuscript_block_release(self):
        path = self.root / 'chapters/01.md'
        path.write_text(path.read_text(encoding='utf-8') + '\n\n作者说明：接下来按章节卡继续写作。\n', encoding='utf-8')
        self.refresh_hashes()
        self.assert_rejected()

    def test_writer_cannot_share_editor_identity(self):
        self.workflow['actors']['continuity_editor'] = self.workflow['actors']['writer']
        self.assert_rejected()

    def test_session_handoff_preserves_historical_role_attribution(self):
        for role in ROLES:
            self.workflow['actors'][role] = [self.workflow['actors'][role], f'successor-{role}']
        result = self.check()
        self.assertTrue(result['ok'], result)

    def test_registered_successor_can_submit_fresh_review(self):
        review = self.add_review(1, 'continuity_editor', identifier='successor-review')
        review['reviewer'] = 'successor-continuity-editor'
        self.workflow['actors']['continuity_editor'] = [
            self.workflow['actors']['continuity_editor'], review['reviewer']]
        self.refresh_hashes()
        result = self.check()
        self.assertTrue(result['ok'], result)

    def test_handoff_ids_cannot_overlap_between_roles(self):
        self.workflow['actors']['writer'] = [self.workflow['actors']['writer'], 'shared-successor']
        self.workflow['actors']['literary_editor'] = [self.workflow['actors']['literary_editor'], 'shared-successor']
        self.assert_rejected()

    def test_registered_actor_cannot_review_for_another_role(self):
        self.workflow['actors']['writer'] = [self.workflow['actors']['writer'], 'successor-writer']
        self.workflow['reviews'][0]['reviewer'] = 'successor-writer'
        self.assert_rejected()

    def test_identical_short_dialogue_chapters_fail_without_long_paragraphs(self):
        lines = ['“你还回来吗？”', '“等天亮再说。”', '“钥匙留在哪里？”', '“窗台下，别让雨淋湿。”']
        self.workflow['contract'].update(chapter_min=1, chapter_max=300, total_min=3, total_max=900)
        for number, task in enumerate(self.workflow['tasks'], 1):
            task['scenes'][0].update(min=1, max=300)
            (self.root / f'chapters/{number:02d}.md').write_text(
                f'# 不同章标题{number}\n\n' + ('\n' * (number+1)).join(lines), encoding='utf-8')
        self.refresh_hashes()
        result = self.assert_rejected()
        self.assertEqual(result['metrics']['duplicates'], [])
        self.assertTrue(any('identical chapter' in e for e in result['errors']), result)

    def test_duplicate_future_drafts_warn_until_submitted_for_review(self):
        dialogue = '“你还回来吗？”\n\n“等天亮再说。”\n\n“钥匙留在哪里？”'
        for task in self.workflow['tasks'][1:]:
            task.update(status='planned', manuscript_sha256='', accepted_by='')
            (self.root / f"chapters/{task['chapter']:02d}.md").write_text(dialogue, encoding='utf-8')
        self.workflow['reviews'] = [r for r in self.workflow['reviews'] if r['scope'] == 1]
        # Keep draft lengths valid when chapter 2 enters review: its duplicate
        # body, rather than an unrelated length or dependency failure, blocks it.
        self.workflow['contract'].update(chapter_min=1, total_min=3)
        for task in self.workflow['tasks']:
            task['scenes'][0]['min'] = 1
        result = self.check('progress')
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['metrics']['duplicates'], [])
        self.assertTrue(any('identical chapter' in w for w in result['warnings']), result)
        self.assert_rejected('release')
        self.workflow['tasks'][1]['status'] = 'in_review'
        result = self.assert_rejected('progress')
        self.assertTrue(any('identical chapter' in e for e in result['errors']), result)

    def test_repetition_exception_with_current_book_literary_pass_is_valid(self):
        self.repetition_fixture()
        result = self.check()
        self.assertTrue(result['ok'], result)
        self.assertEqual(len(result['metrics']['duplicates']), 1)

    def test_repetition_exception_requires_literary_editor(self):
        self.repetition_fixture()['review_id'] = 'book-continuity_editor'
        self.assert_rejected()

    def test_repetition_exception_requires_whole_book_scope(self):
        self.repetition_fixture()['review_id'] = '1-literary_editor'
        self.assert_rejected()

    def test_repetition_exception_cannot_use_stale_historical_pass(self):
        self.repetition_fixture()
        self.add_review('book', 'literary_editor', identifier='current-book-literary')
        self.refresh_hashes()
        for review in self.workflow['reviews']:
            if review['id'] == 'book-literary_editor':
                review['sha256'] = '0' * 64
        self.assert_rejected()

    def test_malformed_json_returns_diagnostic(self):
        (self.root / 'workflow.json').write_text('{"schema_version":1,', encoding='utf-8')
        result = validate(self.root)
        self.assertFalse(result['ok'])
        self.assertTrue(result['errors'])

    def test_duplicate_json_key_returns_diagnostic(self):
        (self.root / 'workflow.json').write_text('{"schema_version":1,"schema_version":1}', encoding='utf-8')
        self.assertFalse(validate(self.root)['ok'])

    def test_malformed_field_types_return_diagnostics_without_traceback(self):
        original = copy.deepcopy(self.workflow)
        mutations = (
            lambda w: w.update(tasks={}),
            lambda w: w['tasks'][0].update(chapter=[]),
            lambda w: w['reviews'][0].update(scope={}),
            lambda w: w['reviews'][0].update(id=[]),
            lambda w: w['tasks'][0].update(depends_on=[{}]),
        )
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                self.workflow = copy.deepcopy(original)
                mutate(self.workflow)
                self.assert_rejected()

    def test_malformed_issue_verifier_returns_diagnostic_without_traceback(self):
        self.issue_fixture()['verified_by'] = []
        self.assert_rejected()

    def test_valid_partial_progress_is_not_release_approval(self):
        for task in self.workflow['tasks'][1:]:
            task.update(status='planned', scenes=[], manuscript_sha256='', accepted_by='')
            (self.root / f"chapters/{task['chapter']:02d}.md").unlink()
            (self.root / f"chapter-cards/{task['chapter']:02d}-card.md").unlink()
        self.workflow['reviews'] = [r for r in self.workflow['reviews'] if r['scope'] == 1]
        (self.root / 'QUALITY_REPORT.md').unlink()
        result = self.check('progress')
        self.assertTrue(result['ok'], result)
        self.assertTrue(result['warnings'])
        self.assert_rejected('release')

    def test_initializer_refuses_overwrite_and_preserves_manuscripts(self):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        cmd = [sys.executable, str(SCRIPTS / 'init_workflow.py'), str(self.root),
               '--chapters', '3', '--count-mode', 'han', '--chapter-min', '100',
               '--chapter-max', '300', '--total-min', '300', '--total-max', '900']
        before = {p.name: p.read_bytes() for p in (self.root / 'chapters').iterdir()}
        first = subprocess.run(cmd, capture_output=True, text=True, env=env)
        self.assertEqual(first.returncode, 0, first.stderr)
        created = (self.root / 'workflow.json').read_bytes()
        scaffold = json.loads(created)
        self.assertTrue(all(t['status'] == 'planned' for t in scaffold['tasks']))
        self.assertFalse(scaffold['reviews'])
        second = subprocess.run(cmd, capture_output=True, text=True, env=env)
        self.assertNotEqual(second.returncode, 0)
        self.assertNotIn('Traceback', second.stderr)
        self.assertEqual((self.root / 'workflow.json').read_bytes(), created)
        self.assertEqual({p.name: p.read_bytes() for p in (self.root / 'chapters').iterdir()}, before)


if __name__ == '__main__':
    unittest.main()
