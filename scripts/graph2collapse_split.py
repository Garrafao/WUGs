import sys
import networkx as nx
import pickle
from modules import *
from cluster_ import *
import csv
import numpy as np
from random import shuffle

[_, input_file, split, collapse, seed, output_file] = sys.argv

    
threshold_split=float(split)
threshold_collapse=float(collapse)
seed=int(seed)
np.random.seed(seed)
with open(input_file, 'rb') as f:
    graph = pickle.load(f)
noise, _, _ = get_clusters(graph, is_include_noise = True, is_include_main = False)
G_clean = graph.copy()    
G_clean.remove_nodes_from([node for cluster in noise for node in cluster])

# Split
found = True
while found == True:
    found = False
    clusters, c2n, n2c = get_clusters(G_clean)
    print('initial number of clusters before splitting: ', len(clusters))
    graph_meta = make_meta_graph(G_clean, test_statistic=np.nanmean, is_include_between=False, is_include_self=True)
    #print(graph_meta).blah
    edges = list(graph_meta.edges())
    shuffle(edges)
    #print(edges).blah
    for (i,j) in edges:
        #print(graph_meta[i][j]['weight'])
        #if graph_meta[i][j]['weight'] <= threshold_split: # we don't check the cluster level as individual nodes are important           
        cluster = clusters[int(i)]
        subgraph = G_clean.subgraph(cluster)
        node2mean = get_mean_weights_per_node(subgraph)
        minval = min(node2mean.values())
        #print(minimum_weight_node)
        if not minval <= threshold_split:
            continue
        minimum_weight_node = np.random.choice([k for k, v in node2mean.items() if v==minval])
        cluster.remove(minimum_weight_node)
        clusters = [c for n, c in enumerate(clusters) if not n == int(i)]
        clusters.append(cluster)
        clusters.append({minimum_weight_node})
        clusters.sort(key=lambda x:-len(x)) # sort by size            
        node2cluster = {node:i for i, cluster in enumerate(clusters) for node in cluster}
        G_clean = add_clusters(G_clean, node2cluster)
        found = True
        break

# Collapse
found = True
while found == True:
    found = False
    clusters, c2n, n2c = get_clusters(G_clean)
    print('initial number of clusters before collapsing: ', len(clusters))
    graph_meta = make_meta_graph(G_clean, test_statistic=np.nanmean)
    edges = list(graph_meta.edges())
    shuffle(edges)
    #print(edges)
    for (i,j) in edges:
        #print(graph_meta[i][j]['weight'])
        if graph_meta[i][j]['weight'] > threshold_collapse:
            cluster_collapsed = clusters[int(i)] | clusters[int(j)]
            clusters = [c for n, c in enumerate(clusters) if not n in [int(i), int(j)]]
            clusters.append(cluster_collapsed)
            clusters.sort(key=lambda x:-len(x)) # sort by size            
            node2cluster = {node:i for i, cluster in enumerate(clusters) for node in cluster}
            G_clean = add_clusters(G_clean, node2cluster)
            found = True
            break

clusters, c2n, n2c = get_clusters(G_clean)
graph.graph['cluster_stats'] = graph.graph['cluster_stats'] | {'split': threshold_split, 'collapse':threshold_collapse}
print('number of clusters: ', len(clusters))
node2cluster = {node:i for i, cluster in enumerate(clusters) for node in cluster} | {node:-1 for cluster in noise for node in cluster}
graph = add_clusters(graph, node2cluster)


with open(output_file, 'wb') as f:
    pickle.dump(graph, f, pickle.HIGHEST_PROTOCOL)
