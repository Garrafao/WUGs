import sys
import csv
import unicodedata
import numpy as np
import pandas as pd
from pathlib import Path
from itertools import combinations

[_, input1, input2, output, lemma] = sys.argv

print(input1, input2, output, lemma)
   
lemma = unicodedata.normalize('NFC', lemma)

df_input = pd.DataFrame()
for p in Path(input1).glob('*.tsv'):
    df = pd.read_csv(p, delimiter='\t', na_filter=False)
    group = str(p).split('/')[-1].split('_')[-1].replace('.tsv', '')          
    df['group'] = group.lower()
    print(group)
    if 'Earlier' == group:
        df['usage1_grouping'] = 'SHC'
        df['usage2_grouping'] = 'SHC'
    elif 'Later' == group:
        df['usage1_grouping'] = 'BCCWJ'
        df['usage2_grouping'] = 'BCCWJ'
    elif 'Compare' == group:
        df['usage1_grouping'] = 'SHC'
        df['usage2_grouping'] = 'BCCWJ'
    else:
        assert 1 == 0
    # there's potential time point information for the first corpus to be extracted
    df_input = pd.concat([df_input, df]) 
for p in Path(input2).glob('*.tsv'):
    df = pd.read_csv(p, delimiter='\t', na_filter=False)
    group = str(p).split('/')[-1].split('_')[-1].replace('.tsv', '')          
    df['group'] = group.lower()
    if 'Earlier' == group:
        df['usage1_grouping'] = 'CHJ'
        df['usage2_grouping'] = 'CHJ'
    elif 'Later' == group:
        df['usage1_grouping'] = 'BCCWJ'
        df['usage2_grouping'] = 'BCCWJ'
    elif 'Compare' == group:
        df['usage1_grouping'] = 'CHJ'
        df['usage2_grouping'] = 'BCCWJ'
    else:
        assert 1 == 0
    df_input = pd.concat([df_input, df]) 
print(df_input.columns)  

def isnumber(x):
    try:
        float(x)
        return True
    except:
        return False

def isnotnumber(x):
    try:
        float(x)
        return False
    except:
        return True
        
workers = sorted([c for c in df_input.columns if 'worker' in c])      
assert set(workers) <= set(['worker1','worker2','worker3','worker4'])
        
for worker in workers:
    n = worker[-1]               
    df_input['comment'+str(n)] = df_input[['worker'+str(n)]] 
    df_input['comment'+str(n)] = df_input[['comment'+str(n)]][df_input[['comment'+str(n)]].applymap(isnotnumber)] 
    df_input['worker'+str(n)] = df_input['worker'+str(n)].fillna(-1) # distinguishing these not confuse them below with explicit zero judgments which are temporarily mapped to nan
    df_input['worker'+str(n)] = df_input[['worker'+str(n)]][df_input[['worker'+str(n)]].applymap(isnumber)] # some judgment fields contain comments instead of judgments, we assume these are judgments of zero (cannot decide)
    df_input['worker'+str(n)] = df_input['worker'+str(n)].fillna(0)
    df_input['comment'+str(n)] = df_input['comment'+str(n)].fillna('')
    df_input['worker'+str(n)].replace({-1:np.nan}, inplace=True) # map missing values back to nan
    df_input['worker'+str(n)] = df_input['worker'+str(n)].astype(float) # make them all floats
   
df_uses = df_input[['usage1', 'usage1_CharacterStartingPosition', 'usage1_SampleID', 'usage1_SequenceNumber', 'usage1_grouping']].rename(columns={'usage1': 'context', 'usage1_CharacterStartingPosition': 'usage_CharacterStartingPosition', 'usage1_SampleID': 'usage_SampleID', 'usage1_SequenceNumber': 'usage_SequenceNumber', 'usage1_grouping': 'grouping'})
df_uses = pd.concat([df_uses, df_input[['usage2', 'usage2_CharacterStartingPosition', 'usage2_SampleID', 'usage2_SequenceNumber', 'usage2_grouping']].rename(columns={'usage2': 'context', 'usage2_CharacterStartingPosition': 'usage_CharacterStartingPosition', 'usage2_SampleID': 'usage_SampleID', 'usage2_SequenceNumber': 'usage_SequenceNumber', 'usage2_grouping': 'grouping'})]) 
df_uses['identifier'] = df_uses['usage_SampleID'].astype(str) + '-' + df_uses['usage_SequenceNumber'].astype(str)
print(len(df_uses))

df_uses = df_uses.drop_duplicates(keep='first')
print(len(df_uses))

assert len(df_uses['identifier'].to_list()) == len(set(df_uses['identifier'].to_list())) # important for below

contexts = df_uses['context'].to_list()
identifiers = df_uses['identifier'].to_list()
uses_reconstructed = []
for i, context in enumerate(contexts):
    context = contexts[i]
    identifier = identifiers[i]
    indices = [
    index for index in range(len(context))
    if context.startswith('**', index)
    ]
    try:
        assert len(indices) == 2
    except AssertionError:
        print(context, indices).black # happens for one usage, but it was fixed in source
        #indices = [0, 2]
        #context = '****' + context
    
    index1 = indices[0]+2
    index2 = indices[1]
    target = context[index1:index2]
    assert not '*' in target
    #print(target)
    assert context[index1-1] == '*'
    assert context[index2] == '*'
    assert context[index1-2] == '*'
    assert context[index2+1] == '*'
    context_cleaned = context.replace("**", "")
    assert len(context_cleaned) == len(context)-4
    index1_cleaned = index1-2
    index2_cleaned = index2-2
    target_cleaned = context_cleaned[index1_cleaned:index2_cleaned]
    assert target_cleaned == target    
    uses_reconstructed.append((identifier, context_cleaned, index1_cleaned, index2_cleaned, 0, len(context_cleaned)))
            
# add indices
identifiers = [identifier for identifier, context, index_target_start, index_target_end, index_sentence_start, index_sentence_end in uses_reconstructed]
contexts = [context for identifier, context, index_target_start, index_target_end, index_sentence_start, index_sentence_end in uses_reconstructed]
indices = [str(index_target_start)+':'+str(index_target_end) for identifier, context, index_target_start, index_target_end, index_sentence_start, index_sentence_end in uses_reconstructed]
indices_sentence = [str(index_sentence_start)+':'+str(index_sentence_end) for identifier, context, index_target_start, index_target_end, index_sentence_start, index_sentence_end in uses_reconstructed]
df_uses['indexes_target_token'] = ''
df_uses.loc[df_uses['identifier'].isin(identifiers), 'indexes_target_token'] = indices   
df_uses['indexes_target_sentence'] = ''
df_uses.loc[df_uses['identifier'].isin(identifiers), 'indexes_target_sentence'] = indices_sentence   
df_uses.loc[df_uses['identifier'].isin(identifiers), 'context'] = contexts   
print(len(df_uses))

df_uses['lemma'] = lemma
df_uses['pos'] = ''
df_uses['date'] = ''
df_uses['description'] = ''

print(df_uses.columns)   
df_uses = df_uses[['lemma','pos','date','grouping', 'identifier','description','context','indexes_target_token', 'indexes_target_sentence']]

# Export data
df_uses.to_csv(output + '/uses.csv', sep='\t', encoding='utf-8', quoting = 3, index=False)
#contexts.append({'lemma':lemma, 'pos':pos, 'date':date, 'grouping':grouping, 'identifier':identifier, 'description':description, 'context':c, 'indexes_target_token':str(index_target_start)+':'+str(index_target_end), 'indexes_target_sentence':str(index_sentence_start)+':'+str(index_sentence_end)})



df_judgments_list = []
for worker in workers:
    df_judgments = df_input.copy()
    n = worker[-1]               
    df_judgments['judgment'] = df_judgments['worker'+str(n)]
    df_judgments['annotator'] = 'worker'+str(n)
    df_judgments['comment'] = df_judgments['comment'+str(n)]
    df_judgments_list.append(df_judgments)

df_judgments = pd.concat(df_judgments_list) 
df_judgments['identifier1'] = df_judgments['usage1_SampleID'].astype(str) + '-' + df_judgments['usage1_SequenceNumber'].astype(str)
df_judgments['identifier2'] = df_judgments['usage2_SampleID'].astype(str) + '-' + df_judgments['usage2_SequenceNumber'].astype(str)
df_judgments['lemma'] = lemma
df_judgments.dropna(subset=['judgment'], inplace=True)
print(df_judgments.columns)   


df_judgments = df_judgments[['identifier1','identifier2','annotator','judgment','comment','lemma','group']]
df_judgments.to_csv(output + '/judgments.csv', sep='\t', encoding='utf-8', quoting = 3, index=False)



# Rename for simplicity
df_labels = df_input.copy()
df_labels['identifier1'] = df_labels['usage1_SampleID'].astype(str) + '-' + df_labels['usage1_SequenceNumber'].astype(str)
df_labels['identifier2'] = df_labels['usage2_SampleID'].astype(str) + '-' + df_labels['usage2_SequenceNumber'].astype(str)
    
annotators = workers
# extract median over annotators
def extract_median(judgments):
    #print(judgments)
    judgments = [j for j in judgments if ~np.isnan(j)] # drop all nan
    judgments = [j for j in judgments if j != 0.0] # drop all 0.0
    median = np.median(judgments)
    return median
    
def extract_median_cleaned(judgments):
    #print(judgments)
    judgments = [j for j in judgments if ~np.isnan(j)] # drop all nan
    median = np.median(judgments)
    if len(judgments) < 2: # filter out pairs with less than two judgments
        return np.nan
    elif 0.0 in judgments: # filter out any use pairs with 0.0 (cannot decide) judgment
        return np.nan
    elif any(abs(j1-j2) > 1 for (j1,j2) in combinations(judgments, 2)): # filter out pairs with at least one annotator pair diverging by more than 1 point on the scale
        return np.nan
    elif median != int(median): # filter out medians which are no integers
        return np.nan
    else:
        return median
        
def extract_judgments_as_int(judgments):
    #print(judgments)
    judgments = [int(j) for j in judgments if ~np.isnan(j)] # drop all nan
    return judgments                        
       
def extract_annotators(judgments):
    annotators = judgments.index.to_list()
    judgments = list(judgments)
    annotators = [annotators[i] for i, j in enumerate(judgments) if ~np.isnan(j)] # drop all nan
    return annotators         
        
df_labels['median'] = df_labels[annotators].apply(lambda x: extract_median(list(x)), axis=1) # add label column
df_labels['median_cleaned'] = df_labels[annotators].apply(lambda x: extract_median_cleaned(list(x)), axis=1) # add label column
df_labels['judgments'] = df_labels[annotators].apply(lambda x: extract_judgments_as_int(list(x)), axis=1) # add judgment column
df_labels['annotators'] = df_labels[annotators].apply(lambda x: extract_annotators(x), axis=1) # add annotator column
df_labels['lemma'] = lemma
print(df_labels.columns)   

df_labels = df_labels[['identifier1','identifier2','median','median_cleaned','judgments','annotators','lemma','group']]
df_labels.to_csv(output + '/labels.csv', sep='\t', encoding='utf-8', quoting = 3, index=False, na_rep='nan')


