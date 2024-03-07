import sys
import csv
import numpy as np

[_, judgments1, judgments2, judgmentsout, roundtag2] = sys.argv

with open(judgments1, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    judgments1 = [row for row in reader]

with open(judgments2, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    judgments2 = [row for row in reader]

for row in judgments2:
    row['round'] = roundtag2
    
judgments_out = judgments1 + judgments2

ids = np.random.randint(low=0, high=len(judgments_out), size=(10,))
sample = np.array(judgments_out)[ids]
#print(sample)
    
# Export data
with open(judgmentsout, 'w', encoding='utf-8') as f:  
    w = csv.DictWriter(f, judgments_out[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE)
    w.writeheader()
    w.writerows(judgments_out)
 
