#!/usr/bin/env python3
"""Read-only measurements; this command does not accept or release a manuscript."""
import argparse
import json
from pathlib import Path
from project_checks import inspect


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project_root', type=Path)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    if not args.project_root.is_dir():
        parser.error('project directory does not exist')
    try:
        result = inspect(args.project_root)
    except (OSError, UnicodeError) as error:
        parser.error(str(error))
    if args.json:
        print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        for c in result['chapters']:
            print(f"{c['file']}: han={c['han']} nonspace={c['nonspace']} sha256={c['sha256']}")
        print('Totals:',result['totals'])
        print('Repeated paragraph groups:',len(result['duplicates']))
        print(f"Redundant paragraph characters: {result['repeated_characters_after_first']} ({result['repetition_ratio']:.2%})")
        print('Book review snapshot:',result['book_sha256'])
        print('Inspection only; no quality or release verdict.')

if __name__ == '__main__':
    main()
