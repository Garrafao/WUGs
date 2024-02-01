import sys
import networkx as nx
import pickle
import csv

[_, senses, judgments, output_file] = sys.argv

with open(output_file, 'rb') as f:
    graph = pickle.load(f)    

with open(senses, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    senses = [row for row in reader]
    #print(senses)    
    label2sense = {row['identifier_sense']:row['description_sense'] for row in senses}

with open(judgments, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    judgments = [row for row in reader]
    judgments = [(row['identifier'],row['identifier_sense'],row['annotator']) for row in judgments]
    
identifier2data = {}
for (u,i,a) in judgments:    
    if u in identifier2data:
        if i=='None':        
            identifier2data[u]['judgments_senses'] = identifier2data[u]['judgments_senses'] | {a:'None'}
        else:
            identifier2data[u]['judgments_senses'] = identifier2data[u]['judgments_senses'] | {a:label2sense[i]}
    else:    
        if i=='None':
            identifier2data[u] = {'judgments_senses':{a:'None'}}
        else:
            identifier2data[u] = {'judgments_senses':{a:label2sense[i]}}        
            
nx.set_node_attributes(graph, identifier2data)
#print(graph.nodes()[identifier])

#print('number of nodes: ', len(graph.nodes()))
with open(output_file, 'wb') as f:
    pickle.dump(graph, f, pickle.HIGHEST_PROTOCOL)
