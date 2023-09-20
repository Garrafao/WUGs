import argparse
from pathlib import Path
import csv

parser = argparse.ArgumentParser()
parser.add_argument("out_dir", type=Path)
parser.add_argument("in_dirs", nargs='+', type=Path)
parser.add_argument('--require-full-word-overlap', action=argparse.BooleanOptionalAction, default=True)
args = parser.parse_args()

args.out_dir.mkdir(parents=True, exist_ok=False)
data_dir = args.out_dir/'data'
data_dir.mkdir()

def get_word(word_dir):
    with open(word_dir/'uses.csv', encoding='utf-8') as csvfile: 
        reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
        row = next(reader)
        return row['lemma']

# write annotators_excluded.csv
excluded_annotators = ['random', 'xlmr+mlp+binary', 'tuozhang', 'garrafao', 'Frida', 'JoshuaC99', 'Tegehall', 'Maria Rumar']
out_data = [{'user':user, 'annotator':user} for i, user in enumerate(excluded_annotators)]
with open(args.out_dir/'annotators_excluded.csv', 'w') as f:
    w = csv.DictWriter(f, ['user', 'annotator'], delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerows(out_data)

# check that it's all the same words
if args.require_full_word_overlap:
    words = [get_word(path) for path in (args.in_dirs[0]/'data').iterdir()]
    for in_dir in args.in_dirs[1:]:
        words_ = [get_word(path) for path in (in_dir/'data').iterdir()]
        for w in words:
            if not w in words_:
                raise ValueError(f"{w} in {args.in_dirs[0]} but not {in_dir}")
        for w_ in words_:
            if not w_ in words:
                raise ValueError(f"{w_} in {in_dir} but not {args.in_dirs[0]}")
else:
    wordss = [[get_word(path) for path in (in_dir/'data').iterdir()] for in_dir in args.in_dirs]
    words = [w for w in wordss[0] if all([w in words_ for words_ in wordss])]

for word in words:

    # collect usages and annotations
    uses, judgments = {}, []
    for in_dir in args.in_dirs:

        word_dir = in_dir/'data'/word
        if not word_dir.exists(): # find the weird unicode dir if its in that format
            for word_dir_ in (in_dir/'data').iterdir():
                if get_word(word_dir_) == word:
                    word_dir = word_dir_
                    break

        with open(word_dir/'judgments.csv', encoding='utf-8') as csvfile: 
            reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
            judgments += [row for row in reader]

        with open(word_dir/'uses.csv', encoding='utf-8') as csvfile: 
            reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
            new_uses = [row for row in reader]    
            for use in new_uses:
                uses[use['identifier']] = uses.get(use['identifier'], {}) | use
    uses = list(uses.values())

    # write {word}/data/judgements.csv and {word}/data/uses.csv
    word_dir = args.out_dir/'data'/word
    word_dir.mkdir(exist_ok=False)
    uses_fields = ['lemma', 'pos', 'date', 'grouping', 'identifier', 'description', 'context']
    with open(args.out_dir/'data'/word/'uses.csv', 'w', encoding='utf-8') as csvfile: 
        writer = csv.DictWriter(csvfile, uses_fields, delimiter='\t',quoting=csv.QUOTE_NONE,quotechar=None,strict=True,extrasaction='ignore')
        writer.writeheader()
        for row in uses:
            try: 
                writer.writerow(row)
            except Exception as e:
                from IPython import embed
                embed(); raise

    # write {word}/data/judgements.csv and {word}/data/uses.csv
    judgment_fields = ['identifier1', 'identifier2', 'annotator', 'judgment', 'lemma']
    with open(args.out_dir/'data'/word/'judgments.csv', 'w', encoding='utf-8') as csvfile: 
        writer = csv.DictWriter(csvfile, judgment_fields, delimiter='\t',quoting=csv.QUOTE_NONE,quotechar=None,strict=True,extrasaction='ignore')
        writer.writeheader()
        writer.writerows(judgments)

