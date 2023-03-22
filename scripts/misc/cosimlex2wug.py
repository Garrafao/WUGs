

import sys
import csv
from collections import defaultdict
from itertools import groupby
import os
import json
import numpy as np
import random
import spacy
import re

[_, data, datadir, lang] = sys.argv
if lang=='fi':
    nlp = spacy.load("fi_core_news_sm")
elif lang == 'en':
    nlp = spacy.load("en_core_web_sm")
elif lang == 'hr':
    nlp = spacy.load("hr_core_news_sm")

#print('Processing:'+lang)
def data2context(data_instance,text,grouping,word):
    date = data_instance['date']

    text = clean_text(text)

    word_in_text = [m.span() for m in re.finditer(word, text)]
    if word_in_text != []:
        (s,e)=word_in_text[0]
    else:
        (s,e) = ('-','-')
    indexes_target_token = str(s)+':'+str(e)
    if (s,e) != ('-','-'):
        assert text[int(s):int(e)]==word
    processed = annotate_text_word(text,word)
    context = {'lemma':lemma, 'pos':processed['leamma_pos'], 'date':date, 'grouping':grouping, 'identifier':identifier+'-text'+grouping, 'description':'-', 'context':text, 'indexes_target_token':indexes_target_token, 'indexes_target_sentence':processed['indexes_target_sentence'], 'context_tokenized':' '.join(processed['context_tokenized']), 'indexes_target_token_tokenized':processed['indexes_target_token_tokenized'], 'indexes_target_sentence_tokenized':processed['indexes_target_sentence_tokenized'],'context_lemmatized':' '.join(processed['context_lemmatized']),'context_pos':' '.join(processed['context_pos']),'word_in_context':word}
    return(context)


def clean_text(t):
    return(t.replace('<strong>','').replace('</strong>',''))
def annotate_text(text,lemma):
    annotations = nlp(text)
    indexes_target_sentence = '-'
    indexes_target_sentence_tokenized = '-'
    for n,sent in enumerate(annotations.sents):
        if lemma in sent.lemma_:
            #print(str(sent))
            indexes_target_sentence_tokenized = n
            s = text.find(str(sent))
            if s != -1:
                e = s + len(str(sent))
                indexes_target_sentence = str(s)+':'+str(e)
                break


    context_tokenized = [str(token) for token in annotations]
    context_lemmatized = [str(token.lemma_.lower()) for token in annotations]
    context_pos = [str(token.pos_) for token in annotations]

    assert len(context_tokenized) == len (context_lemmatized) and len(context_tokenized) == len(context_pos)
    #print(lemma,indexes_target_sentence,text)
    if lemma in context_lemmatized: # there are some lemmatization error, so this check
        indexes_target_token_tokenized = context_lemmatized.index(lemma)
    else:
        indexes_target_token_tokenized = '-'

    return {'leamma_pos':nlp(lemma)[0].pos_,'context_lemmatized':context_lemmatized,'context_tokenized':context_tokenized,'indexes_target_token_tokenized':indexes_target_token_tokenized,'indexes_target_sentence':indexes_target_sentence,'context_pos':context_pos,'indexes_target_sentence_tokenized':indexes_target_sentence_tokenized}

def annotate_text_word(text,word):
    annotations = nlp(text)
    indexes_target_sentence = '-'
    indexes_target_sentence_tokenized = '-'
    sent_lengths = []
    indexes_target_sentence_tokenized_s = 0
    indexes_target_sentence_tokenized_e = 0
    for n,sent in enumerate(annotations.sents):

        if word in [t.text for t in sent]:
            indexes_target_sentence_tokenized_e = indexes_target_sentence_tokenized_s + len([t.text for t in sent])
            #print(str(sent))
            index_target_sentence = n
            s = text.find(str(sent))
            if s != -1:
                e = s + len(str(sent))
                indexes_target_sentence = str(s)+':'+str(e)
                break
        else:
            indexes_target_sentence_tokenized_s += len([t.text for t in sent])


    context_tokenized = [str(token) for token in annotations]
    indexes_target_sentence_tokenized = str(indexes_target_sentence_tokenized_s)+':'+str(indexes_target_sentence_tokenized_e)
    assert context_tokenized[indexes_target_sentence_tokenized_s:indexes_target_sentence_tokenized_e] == [t.text for t in [sen for sen in annotations.sents][n]]
    #print(indexes_target_sentence_tokenized)
    context_lemmatized = [str(token.lemma_.lower()) for token in annotations]
    context_pos = [str(token.pos_) for token in annotations]

    assert len(context_tokenized) == len (context_lemmatized) and len(context_tokenized) == len(context_pos)
    #print(lemma,indexes_target_sentence,text)
    indexes_target_token_tokenized = context_tokenized.index(word)


    return {'leamma_pos':nlp(lemma)[0].pos_,'context_lemmatized':context_lemmatized,'context_tokenized':context_tokenized,'indexes_target_token_tokenized':indexes_target_token_tokenized,'indexes_target_sentence':indexes_target_sentence,'context_pos':context_pos,'indexes_target_sentence_tokenized':indexes_target_sentence_tokenized}

with open(data) as data_file:
    data_instances = []
    reader = csv.reader(data_file,delimiter='\t')
    header = next(reader)
    data = [tuple(l) for l in reader]
    sorted_data = sorted(data, key=lambda x: x[0])
    for k, g in groupby(sorted_data, key=lambda x: x[0]):

        for n,item in enumerate(g):
            data_instance = {}
            #data_instance['id'] = ''.join(random.choice('0123456789abcdef') for i in range(8))+'-'+item[0]
            data_instance['id'] = '2-'+str(n)+'-'+item[0]
            data_instance['other_id'] = '1-'+str(n)+'-'+item[1]
            data_instance['word'] = item[0]
            data_instance['other_word'] = item[1]
            data_instance['pos'] = '-'
            data_instance['date'] = '-'
            data_instance['text1'] = item[2]
            data_instance['text2'] = item[3]
            data_instance['sim1'] = item[4]
            data_instance['sim2'] = item[5]
            data_instance['tokens'] = item[2].split(' ') # this should be properly tokenized_text
            data_instance['token_idx'] = 0 # need to get the token of word in text
            data_instance['word_in_context1'] = item[9]
            data_instance['word_in_context2'] = item[11]
            # cosmilex
            data_instance['other_lemma'] = item[1]
            data_instances.append(data_instance)
    sorted_data2 = sorted(data, key=lambda x: x[1]) # for the second item in the pair of words
    for k, g in groupby(sorted_data2, key=lambda x: x[1]):
        for n,item in enumerate(g):
            data_instance = {}
            #data_instance['id'] = ''.join(random.choice('0123456789abcdef') for i in range(8))+'-'+item[1]
            data_instance['id'] = '1-'+str(n)+'-'+item[1]
            data_instance['other_id'] = '2-'+str(n)+'-'+item[0]
            data_instance['word'] = item[1]
            data_instance['other_word'] = item[0]
            data_instance['pos'] = '-'
            data_instance['date'] = '-'
            data_instance['text1'] = item[2]
            data_instance['text2'] = item[3]
            data_instance['sim1'] = item[4]
            data_instance['sim2'] = item[5]
            data_instance['tokens'] = item[2].split(' ') # this should be properly tokenized_text
            data_instance['token_idx'] = 0 # need to get the token of word in text
            data_instance['word_in_context1'] = item[10]
            data_instance['word_in_context2'] = item[12]
            # cosmilex
            data_instance['other_lemma'] = item[0]
            data_instances.append(data_instance)



lemma2group2context = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))
table = []
for data_instance in data_instances:
    identifier = data_instance['id']
    #print(identifier)
    lemma = data_instance['word'] # this should be lematized
    other_word = data_instance['other_word']
    #tweet1 = data_instance['text1']
    text1 = data_instance['text1']
    context = data2context(data_instance,text1,'1',data_instance['word_in_context1'])
    identifier1 = context['identifier']
    identifier2 = data_instance['other_id']+'-text1'
    #print(identifier1,identifier2,data_instance['sim1'])

    table.append([data_instance['id'],identifier1,identifier2,data_instance['sim1']])

    lemma2group2context[lemma+'_'+other_word][identifier]['1'] = context

    #tweet2 = data_instance['tweet2']
    text2 = data_instance['text2']
    context = data2context(data_instance,text2,'2',data_instance['word_in_context2'])
    identifier1 = context['identifier']
    identifier2 = data_instance['other_id']+'-text2'

    lemma2group2context[lemma+'_'+other_word][identifier]['2'] = context

    table.append([data_instance['id'],identifier1,identifier2,data_instance['sim2']])




lemma2data = defaultdict(lambda: [])

# In cosmilex, we do not have judgemnts between usage pairs but between two different context wrods
for row in table:
    # below is for cosmilex formation
    #lemma = row[0].split('-')[2]
    id1 = row[1]
    id2 = row[2]
    lemma1= id1.split('-')[2]
    lemma2= id2.split('-')[2]
    key = lemma1+'_'+lemma2
    comment = '-'
    sim = str(row[3])
    #print(judgment)
    annotator = np.nan
    data = {'identifier1':id1,'identifier2':id2,'annotator':annotator,'judgment':float(sim),'comment':comment,'lemma':key}
    lemma2data[key].append(data)
    #lemma2data[lemma].append(data)



all_output_folder = datadir +'/wug_all/data/all/'
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
'''
for lemma in lemma2data:
    output_folder = datadir + '/wug'+ '/data/' +lemma+'/'
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
'''
