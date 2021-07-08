import sys
import networkx as nx
import csv

[_, senses, judgments, output_file] = sys.argv

graph = nx.read_gpickle(output_file)
    

with open(senses, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    senses = [row for row in reader]
    #print(senses)    
    label2sense = {row['identifier_sense']:row['description_sense'] for row in senses}

with open(judgments, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    judgments = [row for row in reader]
    use2label = {row['identifier']:(row['identifier_sense'],row['annotator']) for row in judgments}
    
identifier2data = {}
for (u, l) in use2label.items():        
    if 'judgments_senses' in identifier2data:
        if l[0]=='None':        
            identifier2data['judgments_senses'].append({l[1]:'None'})
        else:
            identifier2data['judgments_senses'].append({l[1]:label2sense[l[0]]})
    else:    
        if l[0]=='None':
            identifier2data[u] = {'judgments_senses':{l[1]:'None'}}
        else:
            identifier2data[u] = {'judgments_senses':{l[1]:label2sense[l[0]]}}        
    
nx.set_node_attributes(graph, identifier2data)
#print(graph.nodes()[identifier])

#print('number of nodes: ', len(graph.nodes()))
nx.write_gpickle(graph, output_file)
