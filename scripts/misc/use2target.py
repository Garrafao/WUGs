import sys
import csv

[_, uses] = sys.argv
    
with open(uses, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    uses = [row for row in reader]

for row in uses:
    context = row['context']
    indexes_target_token1, indexes_target_token2 = int(row['indexes_target_token'].split(':')[0]), int(row['indexes_target_token'].split(':')[1])
    indexes_target_sentence1, indexes_target_sentence2 = int(row['indexes_target_sentence'].split(':')[0]), int(row['indexes_target_sentence'].split(':')[1])
    for id in [indexes_target_token1, indexes_target_sentence1]:
        if id < 0:
            print(id)
            print(row)
            print('-----')
    for id in [indexes_target_token2, indexes_target_sentence2]:
        if id > len(context):
            print(id)
            print(row)
            print('-----')
print('------------') 
for row in uses:
    context = row['context']
    indexes_target_token1, indexes_target_token2 = int(row['indexes_target_token'].split(':')[0]), int(row['indexes_target_token'].split(':')[1])
    indexes_target_sentence1, indexes_target_sentence2 = int(row['indexes_target_sentence'].split(':')[0]), int(row['indexes_target_sentence'].split(':')[1])
    print(context[indexes_target_token1:indexes_target_token2])
