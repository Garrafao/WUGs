import sys
import csv
import numpy as np

[_, judgments1, judgments2, judgmentsout, roundtag1, roundtag2] = sys.argv

with open(judgments1, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    judgments1 = [row for row in reader]

with open(judgments2, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    judgments2 = [row for row in reader]

if not roundtag1 == 'None':    
    for row in judgments1:
        assert not 'round' in row
        row['round'] = roundtag1

if not roundtag2 == 'None':    
    for row in judgments2:
        assert not 'round' in row
        row['round'] = roundtag2
    
#header = list(judgments1[0].keys()) + [head for head in judgments2[0].keys() if not head in judgments1[0].keys()]
header = list(judgments1[0].keys())
judgments2 = [{key:value for key, value in row.items() if key in header} for row in judgments2]
judgments_out = judgments1 + judgments2
assert judgments1[0].keys() == judgments2[0].keys()

ids = np.random.randint(low=0, high=len(judgments_out), size=(10,))
sample = np.array(judgments_out)[ids]
#print(sample)
    
# Export data
#with open(judgmentsout, 'w', encoding='utf-8') as f:  
#    w = csv.DictWriter(f, header, delimiter='\t', quoting = csv.QUOTE_NONE)
#    w.writeheader()
#    w.writerows(judgments_out)
 
with open(judgmentsout, 'w') as f:  
    # write header
    f.write('\t'.join(header))
    f.write('\n')
    for row in judgments_out:
        line = '\t'.join(row.values())
        f.write(line)
        f.write('\n')
 
