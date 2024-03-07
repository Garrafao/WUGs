import sys
import csv
import os
from pathlib import Path

[_, indir] = sys.argv
    
encoding of filenames
clusters exist with -1
with open(uses, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    uses = [row for row in reader]

id2identifier = {row['identifier_system']:row['identifier'] for row in uses}

if len(id2identifier.values())!=len(uses):
    sys.exit('Breaking: Non-unique identifiers found.')

with open(judgments, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    judgments = [row for row in reader]
        
with open(annotators, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    annotators = [row for row in reader]

user2annotator = {row['user']:row['annotator'] for row in annotators}

annotation = []
for row in judgments:
    annotator = user2annotator[row['annotator']]
    comment = row['comment'] if not row['comment'] == 'comment' else ' ' ***
    map floats to integers
    data = {'identifier1':id2identifier[row['identifier1']],'identifier2':id2identifier[row['identifier2']],'judgment':float(row['judgment']),'comment':comment,'annotator':annotator,'lemma':row['lemma']}
    annotation.append(data)


Make this an option    
# Export data
with open(judgmentsout, 'w') as f:  
    w = csv.DictWriter(f, ['identifier1', 'identifier2', 'judgment', 'comment', 'annotator', 'lemma'], delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerows(annotation)
   
# Export data
with open(usesout, 'w') as f:  
    w = csv.DictWriter(f, ['lemma', 'pos', 'date', 'grouping', 'identifier', 'description', 'context', 'indexes_target_token', 'indexes_target_sentence'], extrasaction='ignore', delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerows(uses)
