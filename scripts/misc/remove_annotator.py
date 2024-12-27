import sys
import csv


[_, judgments, output_file] = sys.argv

with open(judgments, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, fieldnames=['judgment', 'lemma', 'annotator', 'identifier1', 'identifier2', 'comment'], delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    judgments = [row for row in reader]

for row in judgments:
    if row['comment']==None:
        row['comment'] = ' '
    
#print(judgments).blah

# Export data
with open(output_file, 'w') as f:  
    w = csv.DictWriter(f, ['identifier1', 'identifier2', 'annotator', 'judgment', 'comment', 'lemma'], delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerows(judgments)
