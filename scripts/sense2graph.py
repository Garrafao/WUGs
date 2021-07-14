import sys
import networkx as nx
import csv

[_, senses, output_file] = sys.argv

# Try reading graph, if doesn't exist create.
try:
    graph = nx.read_gpickle(output_file)
except:
    # Initialize graph
    graph = nx.Graph()
    

with open(senses, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    senses = [row for row in reader]
   
for row in senses:
    text = row['description_sense']
    graph.add_node(row['identifier_sense'],description=text,type='sense')

nx.write_gpickle(graph, output_file)
