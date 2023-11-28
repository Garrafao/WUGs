import sys
import networkx as nx
import pickle
import csv
import numpy as np
from modules import get_edge_std, get_node_std, get_data_maps_edges, get_excluded_nodes, get_nan_edges
from cluster_ import add_clusters, get_clusters
 
[_, input_file, non_value, annotators, is_remove_nan, is_remove_noise, collapse, seed, std_edges, std_nodes, degree_remove, output_file] = sys.argv

    
non_value=float(non_value)
with open(input_file, 'rb') as f:
    graph = pickle.load(f)
    
with open(annotators, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    annotators = [row['annotator'] for row in reader]


G_clean_out = graph.copy()
print('Input graph: ', G_clean_out)
G_clean_out.graph['cleaning_stats'] = {}

# remove nan edges
if is_remove_nan:
    nan_edges = get_nan_edges(G_clean_out)    
    G_clean_out.remove_edges_from(nan_edges)
    G_clean_out.graph['cleaning_stats'] = G_clean_out.graph['cleaning_stats'] | {'is_remove_nan':is_remove_nan}

# remove noise cluster
if is_remove_noise:
    noise, _, _ = get_clusters(G_clean_out, is_include_noise = True, is_include_main = False)
    G_clean_out.remove_nodes_from([node for cluster in noise for node in cluster]) # Remove noise nodes before ambiguity measures    
    G_clean_out.graph['cleaning_stats'] = G_clean_out.graph['cleaning_stats'] | {'is_remove_noise':is_remove_noise}

# collapse highly similar clusters
if collapse != 'None':    
    threshold_collapse=float(collapse)
    seed=int(seed)
    np.random.seed(seed)
    graph = nx.read_gpickle(input_file)
    noise, _, _ = get_clusters(G_clean_out, is_include_noise = True, is_include_main = False)
    G_clean = G_clean_out.copy()    
    G_clean.remove_nodes_from([node for cluster in noise for node in cluster])
    found = True
    while found == True:
        found = False
        clusters, c2n, n2c = get_clusters(G_clean)
        print('initial number of clusters: ', len(clusters))
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
    G_clean_out.graph['cleaning_stats'] = G_clean_out.graph['cleaning_stats'] | {'collapse':threshold_collapse}
    print('number of clusters: ', len(clusters))
    node2cluster = {node:i for i, cluster in enumerate(clusters) for node in cluster} | {node:-1 for cluster in noise for node in cluster}
    G_clean_out = add_clusters(G_clean_out, node2cluster)

# remove edges with high standard deviation
std_edges=float(std_edges)    
edge_std = get_edge_std(G_clean_out, annotators, non_value=non_value, normalization=lambda x: ((x-1)/3.0))
edge_std_dirty = [(u, v) for ((u, v), std) in edge_std.items() if std > std_edges]
print('Removing {0} edges with standard deviation above {1}.'.format(len(edge_std_dirty),std_edges))
G_clean_out.remove_edges_from(edge_std_dirty)  
G_clean_out.graph['cleaning_stats'] = G_clean_out.graph['cleaning_stats'] | {'std_edges':std_edges}

# remove nodes with high standard deviation
std_nodes=float(std_nodes)    
node2stds = get_node_std(G_clean_out, annotators, non_value=non_value, normalization=lambda x: ((x-1)/3.0))
nodes_high_stds = [n for n in G_clean_out.nodes() if np.nanmean(node2stds[n]) > std_nodes]
print('Removing {0} nodes with standard deviation above {1}.'.format(len(nodes_high_stds),std_nodes))
G_clean_out.remove_nodes_from(nodes_high_stds)    
G_clean_out.graph['cleaning_stats'] = G_clean_out.graph['cleaning_stats'] | {'std_nodes':std_nodes}

 # remove nodes with low degree
degree_remove=int(degree_remove)    
nodes_degrees = [node for (node, d) in G_clean_out.degree() if d<degree_remove]
G_clean_out.remove_nodes_from(nodes_degrees) 
print('Removing {0} nodes with degree less than {1}.'.format(len(nodes_degrees),degree_remove))
G_clean_out.graph['cleaning_stats'] = G_clean_out.graph['cleaning_stats'] | {'degree_remove':degree_remove}
    
print('Output graph: ', G_clean_out)

with open(output_file, 'wb') as f:
    pickle.dump(G_clean_out, f, pickle.HIGHEST_PROTOCOL)
