
import sys
import networkx as nx
from modules import get_clusters
import csv
   
[_, graph, output_file] = sys.argv

graph = nx.read_gpickle(graph)
clusters = get_clusters(graph)
#print(clusters)

output_data = [{'identifier':identifier, 'cluster':str(i)} for (i, cluster) in enumerate(clusters) for identifier in cluster]    
# Export data
with open(output_file, 'w') as f:  
    w = csv.DictWriter(f, ['identifier', 'cluster'], delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerows(output_data)
