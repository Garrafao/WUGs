

import sys
import csv
from collections import defaultdict
import os
import json
import numpy as np

def data2context(tweet,grouping):
    date = tweet['date']
    context_tokenized = ' '.join(tweet['tokens'])
    indexes_target_token_tokenized = tweet['token_idx']
    text = tweet['text']
    context = {'lemma':lemma, 'pos':'-', 'date':date, 'grouping':grouping, 'identifier':identifier+'-tweet'+grouping, 'description':'-', 'context':text, 'indexes_target_token':'-', 'indexes_target_sentence':'-', 'context_tokenized':context_tokenized, 'indexes_target_token_tokenized':indexes_target_token_tokenized, 'indexes_target_sentence_tokenized':'-'}
    return(context)

[_, data, annotations, datadir, label] = sys.argv

# parse an JSON file by name
with open(data) as jsonfile:
    data_instances = [json.loads(line) for line in jsonfile.readlines()]

lemma2group2context = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))
for data_instance in data_instances:
    identifier = data_instance['id']
    lemma = data_instance['word'] # this should be lematized
    tweet1 = data_instance['tweet1']
    context = data2context(tweet1,'1')
    lemma2group2context[lemma][identifier]['1'] = context
    tweet2 = data_instance['tweet2']
    context = data2context(tweet2,'2')
    lemma2group2context[lemma][identifier]['2'] = context


with open(annotations, encoding='utf-8') as csvfile:
    table = [row for row in csv.reader(csvfile,delimiter='\t')]


lemma2data = defaultdict(lambda: [])
for row in table:
    lemma = row[0].split('-')[1]
    id1 = row[0]
    id2 = row[0]
    comment = ' '
    judgment = row[1]
    annotator = np.nan
    data = {'identifier1':id1+'-tweet1','identifier2':id2+'-tweet2','annotator':annotator,'judgment':float(judgment),'comment':comment,'lemma':lemma}
    lemma2data[lemma].append(data)

all_output_folder = datadir +'/tempowic_'+label+ '_all/data/all/'
if not os.path.exists(all_output_folder):
    os.makedirs(all_output_folder)

# contents for 'all'
with open(all_output_folder +'judgments.csv', 'w') as f:
    w = csv.DictWriter(f, [lemma2data[lemma] for lemma in lemma2data][0][0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    for lemma in lemma2data:
        w.writerows(lemma2data[lemma])

with open(all_output_folder +'uses.csv', 'w') as f:
    w = csv.DictWriter(f, [list(lemma2group2context[lemma].values()) for lemma in lemma2data][0][0]['1'].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    for lemma in lemma2data:
        contexts = list(lemma2group2context[lemma].values())
        rows = [r['1'] for r in contexts] + [r['2'] for r in contexts]
        w.writerows(rows)

for lemma in lemma2data:
    output_folder = datadir + '/tempowic_'+label+ '/data/' +lemma+'/'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Export data
    with open(output_folder +'judgments.csv', 'w') as f:
        w = csv.DictWriter(f, lemma2data[lemma][0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
        w.writeheader()
        w.writerows(lemma2data[lemma])

    contexts = list(lemma2group2context[lemma].values())

    # Export data
    with open(output_folder +'uses.csv', 'w') as f:
        w = csv.DictWriter(f, contexts[0]['1'].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
        w.writeheader()
        rows = [r['1'] for r in contexts] + [r['2'] for r in contexts]
        w.writerows(rows)
