import sys
import networkx as nx
import pickle
import unicodedata
import csv

[_, table, name, output_file] = sys.argv

# Try reading graph, if doesn't exist create.
try:
    with open(output_file, 'rb') as f:
        graph = pickle.load(f)
except:
    # Initialize graph
    name = unicodedata.normalize('NFC', name)
    graph = nx.Graph(lemma=name)
    

with open(table, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    table = [row for row in reader]
    
# Add uses as nodes
identifier2data = {}
for (k, row) in enumerate(table):
    row = row.copy() | {'type':'usage'}
    identifier = row['identifier']
    identifier2data[identifier] = row
    graph.add_node(identifier)
    
nx.set_node_attributes(graph, identifier2data)
#print(graph.nodes()[identifier])

print('number of nodes: ', len(graph.nodes()))
with open(output_file, 'wb') as f:
    pickle.dump(graph, f, pickle.HIGHEST_PROTOCOL)
