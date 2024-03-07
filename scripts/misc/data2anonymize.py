import sys
import csv
import numpy as np
import unicodedata
import os

[_, judgments, judgmentsout, lemma, annotators] = sys.argv

lemma = unicodedata.normalize('NFC', lemma)

with open(judgments, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    judgments = [row for row in reader]
        
with open(annotators, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    annotators = [row for row in reader]

user2annotator = {row['user']:row['annotator'] for row in annotators}

judgments_out = []
for row in judgments:
    row_out = row
    #row_out['comment'] = row_out['comment'] if not row_out['comment'] == ' ' else ''
    row_out['annotator'] = user2annotator[row['annotator']]
    judgments_out.append(row_out)
    
assert len(judgments) == len(judgments_out)    

ids = np.random.randint(low=0, high=len(judgments), size=(10,))
sample = np.array(judgments_out)[ids]
print(sample)
    
# Export data
if not os.path.isdir(judgmentsout + '/' + lemma):
    os.makedirs(judgmentsout + '/' + lemma)
with open(judgmentsout + '/' + lemma + '/judgments.csv', 'w', encoding='utf-8') as f:  
    w = csv.DictWriter(f, judgments_out[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE)
    w.writeheader()
    w.writerows(judgments_out)
 
