"""Shared, dependency-free manuscript measurements. No project writes."""
from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from pathlib import Path

CONTROL_FILES = (
    'PROJECT_ENTRY.md', '00-project-overview.md', '01-cast-bible.md',
    '02-relationship-map.md', '03-timeline.md', '04-plot-lines.md',
    '05-chapter-roadmap.md', '06-continuity-ledger.md', '07-style-and-voice.md',
    '08-active-state.md', '09-literary-revision.md',
)
# Review bookkeeping is excluded so recording a review does not invalidate itself.
TRUTH_FILES = CONTROL_FILES[1:10]
HAN_RANGES = ((0x3400,0x4DBF),(0x4E00,0x9FFF),(0xF900,0xFAFF),
              (0x20000,0x2EE5F),(0x2F800,0x2FA1F),(0x30000,0x3347F))


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def body_text(text: str) -> str:
    """Plain manuscript paragraphs only; headings/separators are not prose.

    Code, comments, links and other Markdown are rejected separately, rather
    than silently counted as manuscript. Unicode letters remain unmodified.
    """
    return '\n'.join(line for line in text.splitlines()
                     if not re.match(r'^\s*#{1,6}(?:\s|$)', line)
                     and not re.fullmatch(r'\s*(?:\*\s*){3,}|\s*(?:-\s*){3,}|\s*(?:_\s*){3,}', line))


def count_text(text: str, mode: str) -> int:
    body = body_text(text)
    if mode == 'han':
        return sum(any(lo <= ord(c) <= hi for lo,hi in HAN_RANGES) for c in body)
    if mode == 'nonspace':
        return sum(not c.isspace() for c in body)
    raise ValueError('count_mode must be han or nonspace')


def chapter_files(root: Path) -> list[Path]:
    return sorted((root/'chapters').glob('*.md'), key=lambda p: p.name)


def snapshot(root: Path) -> str:
    """Hash paths + exact bytes of all chapters and canonical story truth."""
    digest = hashlib.sha256()
    paths = [root/name for name in TRUTH_FILES] + chapter_files(root) + list((root/'chapter-cards').glob('*.md'))
    for path in sorted(paths):
        name = str(path.relative_to(root)).encode('utf-8')
        data = path.read_bytes() if path.is_file() else b'<missing>'
        digest.update(len(name).to_bytes(8,'big') + name)
        digest.update(len(data).to_bytes(8,'big') + data)
    return digest.hexdigest()


def inspect(root: Path) -> dict:
    chapters = []
    paragraphs = defaultdict(list)
    total_paragraph_chars = 0
    for path in chapter_files(root):
        raw = path.read_text(encoding='utf-8')
        body = body_text(raw)
        chapters.append({'file': str(path.relative_to(root)), 'sha256': sha256(raw),
                         'raw': len(raw), 'han': count_text(raw,'han'),
                         'nonspace': count_text(raw,'nonspace')})
        offset = 0
        for paragraph in re.split(r'\n\s*\n', raw):
            start = raw.find(paragraph, offset)
            offset = start + len(paragraph)
            normalized = re.sub(r'\s+', '', body_text(paragraph))
            total_paragraph_chars += len(normalized)
            if len(normalized) >= 40:
                paragraphs[normalized].append({'file': str(path.relative_to(root)),
                                               'line': raw[:start].count('\n')+1})
    duplicates = [{'sha256': sha256(p), 'characters': len(p), 'preview': p[:80],
                   'occurrences': locations} for p,locations in paragraphs.items() if len(locations)>1]
    redundant = sum(d['characters']*(len(d['occurrences'])-1) for d in duplicates)
    return {'chapters': chapters, 'totals': {m: sum(c[m] for c in chapters) for m in ('raw','han','nonspace')},
            'book_sha256': snapshot(root), 'duplicates': duplicates,
            'repeated_characters_after_first': redundant,
            'repetition_ratio': redundant/total_paragraph_chars if total_paragraph_chars else 0}
