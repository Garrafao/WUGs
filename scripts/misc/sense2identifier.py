import sys
import csv

[_, senses_path, judgments_path] = sys.argv
    
with open(senses_path, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    senses = [row for row in reader]
    
with open(judgments_path, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    judgments = [row for row in reader]

lemma = judgments[0]['lemma']
    
senses_out = []    
for row in senses:
    if row['identifier_sense']=='andere' or row['identifier_sense']=='None':
        pass
    else:        
        row['identifier_sense'] = 'dwug_de_sense-' + lemma + '-' + row['identifier_sense']
    senses_out.append(row)

judgments_out = []    
for row in judgments:
    if row['identifier_sense']=='andere' or row['identifier_sense']=='None':
        pass
    else:        
        row['identifier_sense'] = 'dwug_de_sense-' + lemma + '-' + row['identifier_sense']
    judgments_out.append(row)

#print(judgments_out).blah
    
# Export data
with open(senses_path, 'w') as f:  
    w = csv.DictWriter(f, senses_out[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerows(senses_out)

with open(judgments_path, 'w') as f:  
    w = csv.DictWriter(f, judgments_out[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerows(judgments_out)

     
