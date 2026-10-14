#!/usr/bin/env python3
"""Create an unapproved workflow scaffold without changing existing manuscripts."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project_root',type=Path)
    for name in ('chapters','chapter-min','chapter-max','total-min','total-max'):
        parser.add_argument('--'+name,type=int,required=True)
    parser.add_argument('--count-mode',choices=('han','nonspace'),required=True)
    args=parser.parse_args()
    if not args.project_root.is_dir(): parser.error('project directory must already exist')
    if not (0 < args.chapters <= 10000 and 0 < args.chapter_min <= args.chapter_max and 0 < args.total_min <= args.total_max):
        parser.error('positive, ordered ranges and 1-10000 chapters required')
    if max(args.total_min,args.chapters*args.chapter_min)>min(args.total_max,args.chapters*args.chapter_max):
        parser.error('total and chapter ranges cannot be satisfied together')
    data={'schema_version':1,'contract':{'chapters':args.chapters,'count_mode':args.count_mode,
          'chapter_min':args.chapter_min,'chapter_max':args.chapter_max,'total_min':args.total_min,'total_max':args.total_max},
          'actors':{'supervisor':'','planner':'','writer':'','continuity_editor':'','literary_editor':''},
          'tasks':[{'id':f'chapter-{n:02d}','chapter':n,'status':'planned','writer':'',
                    'depends_on':[f'chapter-{n-1:02d}'] if n>1 else [],'scenes':[],
                    'manuscript_sha256':'','accepted_by':''} for n in range(1,args.chapters+1)],
          'reviews':[],'issues':[],'repetition_exceptions':[]}
    try:
        with (args.project_root/'workflow.json').open('x',encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False,indent=2); f.write('\n')
    except FileExistsError:
        parser.error('workflow.json already exists; refusing to overwrite')
    print('Created workflow.json. Assign distinct role session IDs and plan scenes before validation; no manuscript was accepted.')

if __name__ == '__main__': main()
