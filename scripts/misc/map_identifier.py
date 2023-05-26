import sys
import csv
import numpy as np
import pandas as pd
import os
from collections import defaultdict


[_, uses, judgments, usesout, judgmentsout] = sys.argv


with open(uses, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    uses = [row for row in reader]

data_out = []
for row in uses:
    identifier = row['identifier']
    identifier_system = row['identifier_system']
    data_row = {identifier_system: identifier}
    data_out.append(data_row)

mapdict = {}
for d in data_out:
    mapdict.update(d)

outdata = []
for row in uses:
    lemma = row['lemma']
    date = row['date']
    grouping = row['grouping']
    identifier = row['identifier']
    description = row['description']
    context = row['context']
    indexes_target_token = row['indexes_target_token']
    indexes_target_sentence = row['indexes_target_sentence']
    dat_row = {'lemma' : lemma, 'date':date, 'grouping': grouping, 'identifier':identifier, 'description': description, 'context': context, 'indexes_target_token': indexes_target_token, 'indexes_target_sentence': indexes_target_sentence}
    outdata.append(dat_row)

with open(judgments, encoding='utf-8') as csvfile: 
     reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
     judgments = [row for row in reader]


data = []
for row in judgments:
    ident1 = row['identifier1']
    ident2 = row['identifier2']
    for k,v in mapdict.items():
        if ident1 == k:
            row['identifier1'] == v
            identifier1 = v
        if ident2 == k:
            row['identifier2'] == v
            identifier2 = v
    annotator = row['annotator']
    judgment = row['judgment']
    comment = ' '
    lemma = row['lemma']
    data_row = {'identifier1' : identifier1, 'identifier2': identifier2, 'annotator': annotator, 'judgment': judgment, 'comment': comment, 'lemma' : lemma}
    data.append(data_row)



with open(judgmentsout, 'w') as f:  
        w = csv.DictWriter(f, data[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
        w.writeheader()
        w.writerows(data)

with open(usesout, 'w') as f:  
        w = csv.DictWriter(f, outdata[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
        w.writeheader()
        w.writerows(outdata)

