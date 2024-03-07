import sys
import csv
import numpy as np

[_, uses, output_file] = sys.argv
    
with open(uses, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter=',')
    uses = [row for row in reader]

data_out = []
for row in uses:
    lemma = 'plattenkritik'
    pos = ''
    date = row['Date']
    grouping = '1'
    identifier = row['No.']
    description = row['Genre']    
    context = ''
    indexes_target_token = ''
    indexes_target_sentence = ''
    
    ContextBefore = row['ContextBefore'] 
    Hit = row['Hit'] 
    ContextAfter = row['ContextAfter']

    if len(ContextBefore)>0 and len(ContextAfter)>0:
        context = ContextBefore + ' ' + Hit + ' ' + ContextAfter
        indexes_target_token = '{0}:{1}'.format(len(ContextBefore)+1,len(ContextBefore)+1+len(Hit))
    elif len(ContextBefore)>0 and len(ContextAfter)==0:
        context = ContextBefore + ' ' + Hit
        indexes_target_token = '{0}:{1}'.format(len(ContextBefore)+1,len(ContextBefore)+1+len(Hit))
    elif len(ContextBefore)==0 and len(ContextAfter)>0:
        context = Hit + ' ' + ContextAfter
        indexes_target_token = '{0}:{1}'.format(0,len(Hit))
    else:
        assert 1 == 0

    indexes_target_sentence = '{0}:{1}'.format(0,len(context))
    context = context.replace('\"','\'')
       
    print('target: ',context[int(indexes_target_token.split(':')[0]):int(indexes_target_token.split(':')[1])])
    data_row = {'lemma': lemma, 'pos': pos, 'date': date, 'grouping': grouping, 'identifier': identifier, 'description': description, 'context': context, 'indexes_target_token':indexes_target_token, 'indexes_target_sentence':indexes_target_sentence}
    data_out.append(data_row)
        
# Export data
with open(output_file, 'w') as f:  
    w = csv.DictWriter(f, data_out[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, escapechar='\\')
    w.writeheader()
    w.writerows(data_out)
   
