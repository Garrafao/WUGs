import sys
import networkx as nx
import csv
import unicodedata
import numpy as np
from collections import defaultdict
from modules import *
from cluster_ import *

[_, judgments, uses, name, annotators, output_file, excluded, summary_statistic, isnannodes, isnanedges, grouping, edgefilter, threshold, non_value] = sys.argv

# Open user list to exclude, if existent    
if excluded=='None':
    excluded = []
else:
    with open(excluded, encoding='utf-8') as csvfile: 
        reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
        excluded = [row['user'] for row in reader]

# Get summary statistic for edge weights        
if summary_statistic=='median':
    summary_statistic=np.median
if summary_statistic=='mean':
    summary_statistic=np.mean

if isnannodes=='True':
    isnannodes=True
if isnannodes=='False':
    isnannodes=False    

if isnanedges=='True':
    isnanedges=True
if isnanedges=='False':
    isnanedges=False    
    
threshold=float(threshold)

non_value=float(non_value)

# Initialize graph
name = unicodedata.normalize('NFC', name)
graph = nx.Graph(lemma=name)
    
# Open uses
with open(uses, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    uses = [row for row in reader]
    
# Add uses as nodes
identifier2data = {}
for (k, row) in enumerate(uses):
    row = row.copy() | {'type':'usage'}
    identifier = row['identifier']
    identifier2data[identifier] = row
    graph.add_node(identifier)
    
nx.set_node_attributes(graph, identifier2data)
#print(graph.nodes()[identifier])

print('number of nodes: ', len(graph.nodes()))    

# Create mapping from system identifiers to use identifiers    
try:    
    identifier2identifier_ = {row['identifier_system']:row['identifier'] for row in uses}    
    identifier2identifier = lambda x: identifier2identifier_[x]
except KeyError:
    identifier2identifier = lambda x: x    


# Open judgments
with open(judgments, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    judgments = [row for row in reader]

# Open annotator list
with open(annotators, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    user2annotator = {row['user']:row['annotator'] for row in reader}
    annotators = list(user2annotator.values())

# Get judgments with mapped identifiers and annotators    
judgments = [(identifier2identifier(row['identifier1']),identifier2identifier(row['identifier2']),float(row['judgment']),row['comment'],user2annotator[row['annotator']]) for row in judgments if not row['annotator'] in excluded]




graph = add_annotation(graph, judgments)
graph = clean_annotation(graph, annotators=annotators, non_value=non_value) # collapse multiple judgments from same annotator
graph = make_weights(graph, annotators=annotators, summary_statistic=summary_statistic, non_value=non_value)

# Apply graph postprocessing/cleaning

if not grouping == 'full':
    nodesgrouping = [node for node in graph.nodes() if not graph.nodes()[node]['grouping'] == grouping]
    graph.remove_nodes_from(nodesgrouping) # Remove nodes not in grouping
    if len(graph.nodes()) == 0 and len(nodesgrouping) > 0:
        sys.exit('Breaking: grouping filter removing all nodes: %s' % grouping)

if edgefilter == 'conflicts':
    conflicts = get_annotator_conflicts(graph, annotators, non_value=non_value, threshold=threshold)
    non_conflicts = [(u, v) for (u, v) in graph.edges() if not (u, v) in conflicts]
    graph.remove_edges_from(non_conflicts)  # Remove non-conflicts
    # print(conflicts)
elif edgefilter == 'None':
    pass
else:
    sys.exit('Breaking: invalid edge filter argument: %s' % edgefilter)
    
#if edgefilter == 'compare': # to do: add filtering of nodes and edges according to time or grouping combination
#    ewithin = [(u, v) for u, v in graph.edges() if G.nodes()[u]['grouping'] == G.nodes()[v]['grouping']]
#    G.remove_edges_from(ewithin)  # Remove edges which are not between time periods
    
if not isnanedges:
    nan_edges = get_nan_edges(graph)    
    graph.remove_edges_from(nan_edges)
if not isnannodes: # Important to apply this at the end because it depends on the remaining nodes in the graph which is modified by the previous steps
    mappings_edges = get_data_maps_edges(graph, annotators, summary_statistic=summary_statistic)
    node2judgments, node2weights = mappings_edges['node2judgments'], mappings_edges['node2weights']
    nannodes = get_excluded_nodes(node2judgments, node2weights, share=0.5, non_value=non_value)
    graph.remove_nodes_from(nannodes) # Remove noise nodes


nx.write_gpickle(graph, output_file)

