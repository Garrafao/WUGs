import sys
import csv


[_, uses, judgments, senses, is_header, output_file] = sys.argv
        
with open(uses, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    uses = [row for row in reader]

if is_header=='True':
    is_header=True
if is_header=='False':
    is_header=False

id2identifier_senses = {}
if senses!='None':
    with open(senses, encoding='utf-8') as csvfile: 
        reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
        senses = [row for row in reader]
        id2identifier_senses = {row['identifier_sense']:row['identifier_sense'] for row in senses}
    
try:
    id2identifier = {row['identifier_system']:row['identifier'] for row in uses}
except KeyError:
    id2identifier = {row['identifier']:row['identifier'] for row in uses}
    id2identifier = id2identifier | id2identifier_senses

if len(id2identifier.values())!=len(uses)+len(id2identifier_senses.values()):
    sys.exit('Breaking: Non-unique identifiers found.')

with open(judgments, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    judgments = [row for row in reader]

annotation = []
for row in judgments:
    annotator = row['annotator']
    comment = row['comment'] if row['comment']!='' else '-'
    comment = ' ' if (row['comment']=='-' or row['comment']=='') else row['comment']
    data = {'identifier1':id2identifier[row['identifier1']],'identifier2':id2identifier[row['identifier2']],'judgment':float(row['judgment']),'comment':comment,'annotator':annotator,'lemma':row['lemma']}
    annotation.append(data)
    
# Export data
with open(output_file, 'a') as f:  
    w = csv.DictWriter(f, ['identifier1', 'identifier2', 'judgment', 'comment', 'annotator', 'lemma'], delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    if is_header:
        w.writeheader()
    w.writerows(annotation)
