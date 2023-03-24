

import sys
import csv
from collections import defaultdict
import os
import json
import numpy as np
import spacy
import re


nlp = spacy.load("en_core_web_sm")


def data2context(tweet,grouping):
    date = tweet['date']
    text = tweet['text']
    text_start = tweet['text_start']
    text_end = tweet['text_end']
    indexes_target_token = str(text_start)+':'+str(text_end)
    annotated = annotate_text_word(text,text[text_start:text_end])

    context = {'lemma':lemma, 'pos':nlp(lemma)[0].pos_, 'date':date, 'grouping':grouping, 'identifier':identifier+'-tweet'+grouping, 'description':'-', 'context':text, 'indexes_target_token':indexes_target_token, 'context_tokenized':' '.join(annotated['context_tokenized']), 'indexes_target_token_tokenized':annotated['indexes_target_token_tokenized'],'indexes_target_sentence':annotated['indexes_target_sentence'],'indexes_target_sentence_tokenized':annotated['indexes_target_sentence_tokenized'],'context_lemmatized':' '.join(annotated['context_lemmatized']),'context_pos':' '.join(annotated['context_pos'])}

    return(context)

def annotate_text_word(text,word):
    annotations = nlp(text)
    indexes_target_sentence = '-'
    indexes_target_sentence_tokenized = '-'
    indexes_target_sentence_tokenized_s = 0
    indexes_target_sentence_tokenized_e = 0
    word=word.replace('\'s','')
    for n,sent in enumerate(annotations.sents):
        if word in [t.text for t in sent]:
            indexes_target_sentence_tokenized_e = indexes_target_sentence_tokenized_s + len([t.text for t in sent])
            s = text.find(str(sent))
            if s != -1:
                e = s + len(str(sent))
                indexes_target_sentence = str(s)+':'+str(e)
                break
        else:
            indexes_target_sentence_tokenized_s += len([t.text for t in sent])


    context_tokenized = [str(token) for token in annotations]
    indexes_target_sentence_tokenized = str(indexes_target_sentence_tokenized_s)+':'+str(indexes_target_sentence_tokenized_e)
    #print(n,indexes_target_sentence_tokenized_s,indexes_target_sentence_tokenized_e,word,context_tokenized)
    assert context_tokenized[indexes_target_sentence_tokenized_s:indexes_target_sentence_tokenized_e] == [t.text for t in [sen for sen in annotations.sents][n]]

    context_lemmatized = [str(token.lemma_.lower()) for token in annotations]
    context_pos = [str(token.pos_) for token in annotations]

    assert len(context_tokenized) == len (context_lemmatized) and len(context_tokenized) == len(context_pos)

    indexes_target_token_tokenized = context_tokenized.index(word)


    return {'context_lemmatized':context_lemmatized,'indexes_target_sentence':indexes_target_sentence,'context_pos':context_pos,'indexes_target_sentence_tokenized':indexes_target_sentence_tokenized,'context_lemmatized':context_lemmatized,'context_tokenized':context_tokenized,'indexes_target_token_tokenized':indexes_target_token_tokenized}


[_, data, annotations, datadir, label] = sys.argv
#print('Processing: '+label)
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
    annotator = "gold"
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
