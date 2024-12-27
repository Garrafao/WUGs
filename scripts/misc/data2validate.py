import sys
import csv
import os
import unicodedata
from difflib import SequenceMatcher

[_, uses, judgments, usesout, judgmentsout, annotators] = sys.argv
    
# encoding of filenames
assert uses == unicodedata.normalize('NFC', uses)
usesout = unicodedata.normalize('NFC', usesout)
judgmentsout = unicodedata.normalize('NFC', judgmentsout)

with open(uses, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    uses = [row for row in reader]

try:    
    with open(judgments, encoding='utf-8') as csvfile: 
        reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
        judgments = [row for row in reader]
except FileNotFoundError:
    print('No judgments found!')
    judgments = None
    
# Check all judgments are present in uses    

punctuation = [' ', '.', ',', '!', '"', '\'']
error_no = 0
for row in uses:
    #row['lemma'] = row['lemma'].replace('-', '_') # only do this for erroneous English data
    identifier = row['identifier']
    if (identifier == 'vogt_briefe02_1851-7019-783' or identifier == 'vogt_briefe02_1851-7019-780'):
        print(identifier, 'problem: identifier')
        #print(row['context'][-3:])
        row['context'] = row['context'] + '7.'
        #print(row['indexes_target_sentence'])
        row['indexes_target_sentence'] = row['indexes_target_sentence'].split(':')[0]+':'+str(int(row['indexes_target_sentence'].split(':')[1])+2)
        #print(row['indexes_target_sentence']).blah
        error_no += 1    
    context = row['context']
    target_indices = row['indexes_target_token']
    index_target_start = int(target_indices.split(':')[0])
    index_target_end = int(target_indices.split(':')[1])
    target = context[index_target_start:index_target_end]
    #print([target])
    target_sentence_indices = row['indexes_target_sentence']
    index_target_sentence_start = int(target_sentence_indices.split(':')[0])
    index_target_sentence_end = int(target_sentence_indices.split(':')[1])
    target_sentence = context[index_target_sentence_start:index_target_sentence_end]
    #print([target_sentence])
    # map space descriptions to empty descriptions
    row['description'] = row['description'] if not (row['description'] == ' ') else ''

    if 'context_tokenized' in row:
        if (identifier == 'vogt_briefe02_1851-7019-783' or identifier == 'vogt_briefe02_1851-7019-780'):
            print(identifier, 'problem: identifier')
            #print(row['context_tokenized'][-3:])
            row['context_tokenized'] = row['context_tokenized'] + '7.'
            error_no += 1
        context_tokenized = row['context_tokenized']
        context_tokenized_split = context_tokenized.split(' ')
        indexes_target_token_tokenized = int(row['indexes_target_token_tokenized'])
        indexes_target_sentence_tokenized = row['indexes_target_sentence_tokenized']
        index_target_sentence_tokenized_start = int(indexes_target_sentence_tokenized.split(':')[0])
        index_target_sentence_tokenized_end = int(indexes_target_sentence_tokenized.split(':')[1])
        target_token = context_tokenized_split[indexes_target_token_tokenized]
        assert len(target_token) > 0
        if target_token[0] in punctuation:
            print(target_token, 'problem: target_token[0] in punctuation')
            error_no += 1
        if target_token[-1] in punctuation:                   
            print(target_token, 'problem: target_token[-1] in punctuation')
            error_no += 1
        string_similarity = SequenceMatcher(None, target.lower(), target_token.lower()).ratio()
        if string_similarity < 0.5:
            print(target, target_token, 'problem: string_similarity < 0.5')
            error_no += 1
            raise AssertionError            
        assert 0 <= index_target_sentence_tokenized_start <= len(context_tokenized_split)
        assert 0 <= index_target_sentence_tokenized_end <= len(context_tokenized_split)
        
    if 'context_lemmatized' in row:
        is_optimize = False
        if (identifier == 'vogt_briefe02_1851-7019-783' or identifier == 'vogt_briefe02_1851-7019-780'):
            print(identifier, 'problem: identifier')
            row['context_lemmatized'] = ' '.join(row['context_lemmatized'].split(' ')[:1644])
            #raise AssertionError            
            error_no += 1
        context_lemmatized = row['context_lemmatized']
        context_lemmatized_split = context_lemmatized.split(' ')            
        try:
            assert len(context_tokenized_split) == len(context_lemmatized_split)
        except AssertionError:            
            print(context_tokenized_split, '***', context_lemmatized_split, 'problem: len(context_tokenized_split) == len(context_lemmatized_split)')
            #print(len(context_tokenized_split), len(context_lemmatized_split))
            #print(identifier)
            raise AssertionError # For now raise the error as we don't want anything to pass here           
            error_no += 1
            # Try to solve it by removing empty strings
            context_lemmatized_split = [token for token in context_lemmatized_split if not token == '']
            try:
                assert len(context_tokenized_split) == len(context_lemmatized_split)
                row['context_lemmatized'] = ' '.join(context_lemmatized_split)
                print('solved one error by removing empty strings')
                raise AssertionError
            except AssertionError:
                print(context_tokenized_split, '***', context_lemmatized_split, 'problem: len(context_tokenized_split) == len(context_lemmatized_split)')
                is_optimize = True
                error_no += 1
        if is_optimize:    
                # adjust source file
                row['context_lemmatized'] = ''
        if row['context_lemmatized'] != '':       
            target_lemma = context_lemmatized_split[indexes_target_token_tokenized]
            assert len(target_lemma) > 0
            if target_lemma[0] in punctuation:
                print(target_lemma, 'problem: target_lemma[0] in punctuation')
                error_no += 1
            if target_lemma[-1] in punctuation:                   
                print(target_lemma, 'problem: target_lemma[-1] in punctuation')
                error_no += 1
            string_similarity = SequenceMatcher(None, target.lower(), target_lemma.lower()).ratio()
            if string_similarity < 0.5:
                string_similarity = SequenceMatcher(None, target.lower(), target_lemma.lower().replace('ß', 'ss').replace('fack', 'fackafdelning')).ratio()
                if string_similarity < 0.5:
                    print(target, target_lemma, 'problem: string_similarity < 0.5')
                    error_no += 1
                    raise AssertionError
            assert 0 <= index_target_sentence_tokenized_start <= len(context_lemmatized_split)
            assert 0 <= index_target_sentence_tokenized_end <= len(context_lemmatized_split)

    if 'context_pos' in row:
        if (identifier == 'vogt_briefe02_1851-7019-783' or identifier == 'vogt_briefe02_1851-7019-780'):
            print(identifier, 'problem: identifier')
            row['context_pos'] = ' '.join(row['context_pos'].split(' ')[:1644])
            #print(row['context_pos'].split(' ')[1600:1644]).blah
            #raise AssertionError            
            error_no += 1
        context_pos = row['context_pos']
        context_pos_split = context_pos.split(' ')            
        try:
            assert len(context_tokenized_split) == len(context_pos_split)
        except AssertionError:            
            print(context_tokenized_split, '***', context_pos_split, 'problem: len(context_tokenized_split) == len(context_pos_split)')
            #print(len(context_tokenized_split), len(context_pos_split))
            print(identifier)
            raise AssertionError # For now raise the error as we don't want anything to pass here           
            error_no += 1
        assert 0 <= index_target_sentence_tokenized_start <= len(context_pos_split)
        assert 0 <= index_target_sentence_tokenized_end <= len(context_pos_split)
    
    # Catch normalization errors
    if 'context_normalized' in row and not row['context_normalized'] == '':
        is_optimize = False
        if (identifier == 'vogt_briefe02_1851-7019-783' or identifier == 'vogt_briefe02_1851-7019-780'):
            print(identifier, 'problem: identifier')
            row['context_normalized'] = ' '.join(row['context_normalized'].split(' ')[:1644])
            error_no += 1
        if identifier == 'brehm_thierleben03_1866-10964-18':
            row['context_normalized'] = row['context_normalized'].replace('7 2/3', '7_2/3')
            error_no += 1
        if identifier == 'gerstner_mechanik03_1834-10703-3':
            row['context_normalized'] = row['context_normalized'].replace('5 2/3', '5_2/3')
            error_no += 1
        context_normalized = row['context_normalized']
        context_normalized_split = context_normalized.split(' ')
        if identifier == 'beyer_poetik01_1882-7284-11' or identifier == 'beyer_poetik01_1882-17923-12':
            print(context_tokenized_split, '***', context_normalized_split, 'problem: identifier')
            is_optimize = True
            error_no += 1
        try:
            assert len(context_tokenized_split) == len(context_normalized_split)
        except AssertionError:            
            print(context_tokenized_split, '***', context_normalized_split, 'problem: len(context_tokenized_split) == len(context_normalized_split)')
            error_no += 1
            # Try to solve it by removing empty strings
            context_normalized_split = [token for token in context_normalized_split if not token == '']
            try:
                print(identifier)
                assert len(context_tokenized_split) == len(context_normalized_split)
                row['context_normalized'] = ' '.join(context_normalized_split)
                print('solved one error by removing empty strings')
            except AssertionError:
                print(context_tokenized_split, '***', context_normalized_split, 'problem: len(context_tokenized_split) == len(context_normalized_split)')
                is_optimize = True
                error_no += 1
        if is_optimize:    
                # adjust source file
                row['context_normalized'] = ''
        if row['context_normalized'] != '':       
            try:
                target_normalized = context_normalized_split[indexes_target_token_tokenized]
            except AssertionError:
                print('problem: context_normalized_split[indexes_target_token_tokenized]')
                error_no += 1        
            assert len(target_normalized) > 0
            if target_normalized[0] in punctuation:
                print(target_normalized, 'problem: target_normalized[0] in punctuation')
                error_no += 1
            if target_normalized[-1] in punctuation:                   
                print(target_normalized, 'problem: target_normalized[-1] in punctuation')
                error_no += 1
            string_similarity = SequenceMatcher(None, target.lower(), target_normalized.lower()).ratio()
            if string_similarity < 0.5:                   
                print(target, target_normalized, 'problem: string_similarity < 0.5')
                error_no += 1
            assert 0 <= index_target_sentence_tokenized_start <= len(context_normalized_split)
            assert 0 <= index_target_sentence_tokenized_end <= len(context_normalized_split)       
            assert len(target_normalized) > 0

        
    # Check that constructed target tokens have desired properties
    assert 0 <= index_target_start <= len(context)
    assert 0 <= index_target_end <= len(context)
    assert 0 <= index_target_sentence_start <= len(context)
    assert 0 <= index_target_sentence_end <= len(context)
    assert len(target) > 0
    if target[0] in punctuation:
        print(target, 'problem: target[0] in punctuation')
        error_no += 1
    if target[-1] in punctuation:                   
        print(target, 'problem: target[-1] in punctuation')
        error_no += 1
    if index_target_start > 3:
        #print('test', [context[index_target_start-1]])
        if context[index_target_start-1].isalpha():
            print(context, 'problem: context[index_target_start-1].isalpha()')
            error_no += 1
    if len(context)-index_target_end > 3:
        if context[index_target_end].isalpha():
            print(context, 'problem: context[index_target_end+1].isalpha()')
            error_no += 1

print('error_no', error_no)
#assert error_no == 0 # strict condition
#assert error_no < 4 # relaxed condition
#assert error_no < 13 # loose condition

        
with open(annotators, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    annotators = [row for row in reader]
    
# Check all anonymized annotators our present in judgments and vice versa


if judgments != None:
    user2annotator = {row['user']:row['annotator'] for row in annotators}
    for row in judgments:
       #row['lemma'] = row['lemma'].replace('-', '_') # only do this for erroneous English data
       # map space comments to empty comments
       row['comment'] = row['comment'] if not (row['comment'] == ' ' or row['comment'] == 'comment') else ''
       if len(row['comment'].split(' ')[0].split('-'))==3:
           print(row['comment'], 'problem: comment is daytime')
           row['comment'] = ''
           error_no += 1
       # map floats to integers
       assert int(float(row['judgment'])) == float(row['judgment'])
       row['judgment'] = str(int(float(row['judgment'])))
       # check annotator in anonymized annotators
       assert row['annotator'] in user2annotator.values()


    # Optionally export data
    if judgmentsout != 'None':       
        # Export data
        with open(judgmentsout, 'w') as f:  
            # write header
            header = '\t'.join(judgments[0].keys())
            f.write(header)
            f.write('\n')
            for row in judgments:
                line = '\t'.join(row.values())
                f.write(line)
                f.write('\n')

    '''
    # Export data
    with open(judgmentsout, 'w') as f:  
        w = csv.DictWriter(f, judgments[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE)
        w.writeheader()
        w.writerows(judgments)
    '''
       
if  usesout != 'None':       
    # Export data
    with open(usesout, 'w') as f:  
        # write header
        header = '\t'.join(uses[0].keys())
        f.write(header)
        f.write('\n')
        for row in uses:
            line = '\t'.join(row.values())
            f.write(line)
            f.write('\n')
    
    '''
    with open(usesout, 'w') as f:  
        w = csv.DictWriter(f, uses[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE)
        w.writeheader()
        for line in uses:
            #line = {'context':line['context'].replace('"', '')} # 4 testing
            print(line)
            w.writerow(line)
        #w.writerows(uses)
    '''    

# clusters exist with -1
