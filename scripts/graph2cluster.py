import sys
import networkx as nx
from modules import *
from cluster_ import *

[_, input_file, threshold, modus, output_file] = sys.argv
   
threshold=float(threshold)
graph = nx.read_gpickle(input_file)
#transformation = lambda x: ((x*3)+1.0) # to unnormalize
#transformation = lambda x: ((x*3)+1.0)-threshold # to unnormalize and shift
transformation = lambda x: x-threshold # only shift
graph = transform_edge_weights(graph, transformation = transformation)

if modus=='test':
    max_attempts = 10
    max_iters = 10
    s = 2
if modus=='system':
    max_attempts = 10
    max_iters = 10
    s = 5
if modus=='full':
    max_attempts = 2000
    max_iters = 50000
    s = 20

try: # use previous clustering for initialization
    initial = get_clusters(graph)
except KeyError:
    initial = []

clusters, cluster_stats = cluster_correlation_search(graph, s = s, max_attempts = max_attempts, max_iters = max_iters, initial = initial) # rather good performance: 2000, 50000
graph.graph['cluster_stats'] = cluster_stats
transformation = lambda x: x+threshold
graph = transform_edge_weights(graph, transformation = transformation)
print('number of clusters: ', len(clusters))
graph = add_clusters(graph, clusters)

nx.write_gpickle(graph, output_file)
