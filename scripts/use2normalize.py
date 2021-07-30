import sys
import csv
import numpy as np

[_, uses, dataset, output_file] = sys.argv
    
with open(uses, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    uses = [row for row in reader]

    
if dataset=='dwug_de' or dataset=='discowug' or dataset=='refwug':    
    trans_table = {'aͤ' : 'ä', 'oͤ' : 'ö', 'uͤ' : 'ü', 'Aͤ' : 'Ä', 
               'Oͤ' : 'Ö', 'Uͤ' : 'Ü', 'ſ' : 's', '\ua75b' : 'r', 
               'm̃' : 'mm', 'æ' : 'ae', 'Æ' : 'Ae', ' ,': ',',
               ' .': '.', ' ;': ';', ' ?': '?', ' !': '!',
               '„ ': '„', ' “': '“', ' "': '"', ' :': ':', ' )': ')',
               '( ': '(', ' \'s' : '\'s', '- ' : '-', '  ' : ' '}   
if dataset=='dwug_en' or dataset=='usim' or dataset=='dups':    
    trans_table = {' ,': ',',
               ' .': '.', ' ;': ';', ' ?': '?', ' !': '!',
               '„ ': '„', ' “': '“', ' :': ':', ' )': ')',
               '( ': '(', ' \'s' : '\'s', '  ' : ' ',
               ' n\'t' : 'n\'t', ' \'ve' : '\'ve', ' \'d' : '\'d',
               ' \'re' : '\'re', ' \'ll' : '\'ll'}           
if dataset=='dwug_sv':    
    trans_table = {' ,': ',',
               ' .': '.', ' ;': ';', ' ?': '?', ' !': '!',
               '„ ': '„', ' “': '“', ' "': '"', ' :': ':', ' )': ')',
               '( ': '(', ' \'s' : '\'s', '  ' : ' '}
if dataset=='generic':    
    trans_table = {' ,': ',',
               ' .': '.', ' ;': ';', ' ?': '?', ' !': '!',
               '„ ': '„', ' “': '“', ' "': '"', ' :': ':', ' )': ')',
               '( ': '(', '  ' : ' '}

data_out = []
for row in uses:
    identifier = row['identifier']
    indexes = row['indexes_target_sentence_tokenized'].split(':')
    index_start_sentence, index_end_sentence = int(indexes[0]), int(indexes[1])
    context = row['context_tokenized']
    tokens = context.split(' ')
    index_start = np.sum([len(t)+1 for t in tokens[:index_start_sentence]]) if index_start_sentence!=0 else 0
    index_end = np.sum([len(t)+1 for t in tokens[:index_end_sentence]]) if index_end_sentence!=0 else 0
    preceding_data = context[:index_start]
    sentence = context[index_start:index_end]
    following_data = context[index_end:]
    index_target = int(row['indexes_target_token_tokenized'])
    tokens_sentence = sentence.split(' ')
    tokens_preceding = preceding_data.split(' ')
    index_target_start = int(np.sum([len(t)+1 for t in tokens_sentence[:index_target-index_start_sentence]])) if index_target!=0 else 0
    index_target_end = index_target_start + len(tokens_sentence[index_target-index_start_sentence])
    sentence1 = sentence[:index_target_start]
    sentence2 = sentence[index_target_start:index_target_end]
    sentence3 = sentence[index_target_end:]
    for (s, sr) in trans_table.items():
        preceding_data = preceding_data.replace(s, sr)
        sentence1 = sentence1.replace(s, sr)
        sentence2 = sentence2.replace(s, sr)
        sentence3 = sentence3.replace(s, sr)
        following_data = following_data.replace(s, sr)
    context = preceding_data + sentence1 + sentence2 + sentence3 + following_data
    index_start = len(preceding_data)
    index_end = index_start + len(sentence1) + len(sentence2) + len(sentence3)
    index_target_start = index_start + len(sentence1)
    index_target_end = index_target_start + len(sentence2) 
    print('target: ',context[index_target_start:index_target_end])
    data_row = {'identifier': identifier, 'context': context, 'indexes_target_token':str(index_target_start)+':'+str(index_target_end), 'indexes_target_sentence':str(index_start)+':'+str(index_end)}
    data_out.append(data_row)
        
# Export data
with open(output_file, 'w') as f:  
    w = csv.DictWriter(f, data_out[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerows(data_out)

    
