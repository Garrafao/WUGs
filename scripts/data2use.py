import sys
import csv
import os

[_, uses, data, output_file] = sys.argv
    
with open(uses, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    uses = [row for row in reader]

id2data = {}
for root, subdirectories, files in os.walk(data):
    for f in files:    
        with open(os.path.join(root, f), encoding='utf-8') as csvfile: 
            reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
            data_ = [row for row in reader]
            id2data_ = {row['identifier']:row for row in data_}
            id2data = id2data | id2data_

uses_out = []
for row in uses:
    identifier = row['identifier']    
    if identifier in id2data.keys():
        data_row = {l:d.strip(' ') for l,d in id2data[identifier].items() if ((not l in row) or (l in row and row[l]==' '))}
        row = row | data_row
        uses_out.append(row)
        if 'context_pos' in row and (row['pos']==' ' or row['pos']=='-' or row['pos']==''):
            target = (row['context_lemmatized'].split(' ')[int(row['indexes_target_token_tokenized'])],row['context_pos'].split(' ')[int(row['indexes_target_token_tokenized'])])
            indexes_target = int(row['indexes_target_token_tokenized']) # may later be various indexes, not yet
            row['pos'] = row['context_pos'].split(' ')[indexes_target]
    else:
        uses_out.append(row)
        print('no data')
        pass

# Export data
with open(output_file, 'w') as f:  
    w = csv.DictWriter(f, uses_out[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerows(uses_out)

    
