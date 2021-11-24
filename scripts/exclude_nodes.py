
import sys
import networkx as nx
from modules import *
import unicodedata
import csv

[_, graph, stats_file, is_header, annotators, output_file] = sys.argv

graph = nx.read_gpickle(graph)
name = graph.graph['lemma']

if is_header=='True':
    is_header=True
if is_header=='False':
    is_header=False

    
with open(annotators, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    annotators = [row['annotator'] for row in reader]

empty_edges = get_empty_edges(graph, annotators)    
graph.remove_edges_from(empty_edges)

mappings_edges = get_data_maps_edges(graph, annotators)
node2judgments, node2weights = mappings_edges['node2judgments'], mappings_edges['node2weights']
excluded_nodes = get_excluded_nodes(node2judgments, node2weights, share=0.5)
#print(excluded_nodes)

graph.remove_nodes_from(excluded_nodes)
normalization = lambda x: x
graph = make_weights(graph, annotators, normalization=normalization, non_value=0.0)
    
nx.write_gpickle(graph, output_file)

stats = {}
stats['lemma'] = name
stats['excluded_nodes'] = len(excluded_nodes)
# Export stats
with open(stats_file, 'a', encoding='utf-8') as f_out:
    if is_header:
        f_out.write('\t'.join([key for key in stats])+'\n')
    f_out.write('\t'.join([str(stats[key]) for key in stats])+'\n')


