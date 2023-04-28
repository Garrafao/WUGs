import sys
import csv


[_, judgments, output_file] = sys.argv

with open(judgments, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    rows = [row for row in reader]

pairs = {frozenset((row['identifier1'],row['identifier2'])) for row in rows}
pair2lemma = {frozenset((row['identifier1'],row['identifier2'])) : row['lemma'] for row in rows}
pairs = [list(pair) for pair in pairs]
instances = [{'lemma': pair2lemma[frozenset(pair)], 'identifier1':pair[0], 'identifier2':pair[1]} for pair in pairs]


#print(instances)

# Export data
with open(output_file, 'w') as f:  
    w = csv.DictWriter(f, ['lemma', 'identifier1', 'identifier2'], delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerows(instances)
