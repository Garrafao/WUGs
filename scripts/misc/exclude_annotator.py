import sys
import csv
import numpy as np
import pandas as pd
import os
from collections import defaultdict


[_, judgments, judgmentsout] = sys.argv

with open(judgments, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    judgments = [row for row in reader]
        


data = []
for row in judgments:
    ident1 = row['identifier1']
    ident2 = row['identifier2']
    annotator = row['annotator']
    judgment = row['judgment']
    comment = ' '
    lemma = row['lemma']
    data_row = {'identifier1' : ident1, 'identifier2': ident2, 'annotator': annotator, 'judgment': judgment, 'comment': comment, 'lemma' : lemma}
    data.append(data_row)

unique_annotators = list(set(d['annotator'] for d in data))

res = [i for i in data if not (i['annotator'] == 'JoshuaC99')] #give annotator to exclude name here
    
with open(judgmentsout, 'w') as f:  
    w = csv.DictWriter(f, res[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerows(res)
