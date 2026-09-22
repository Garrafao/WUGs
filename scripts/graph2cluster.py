import sys
import networkx as nx
import pickle
from modules import transform_edge_weights, scale_weights, get_node_std, get_data_maps_edges, get_excluded_nodes, get_nan_edges
from cluster_ import add_clusters, get_clusters
from correlation_clustering.correlation import cluster_correlation_search
import csv
import numpy as np
 
[_, input_file, threshold, modus, is_clean, annotators, output_file] = sys.argv

if __name__ == '__main__':
    threshold=float(threshold)
    with open(input_file, 'rb') as f:
        graph = pickle.load(f)

    with open(annotators, encoding='utf-8') as csvfile: 
        reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
        annotators = [row['annotator'] for row in reader]
                

    if modus=='test':
        max_iter = 10
        s = 2
    if modus=='system':
        max_iter = 50  # to do: needs to be fine-tuned 
        s = 10
    if modus=='full':
        max_iter = 500  # to do: needs to be fine-tuned 
        s = 20

    if is_clean=='True':
        is_clean=True
    if is_clean=='False':
        is_clean=False

    try: # search previous clustering for initialization
        initial, _, _ = get_clusters(graph)
        noise, _, _ = get_clusters(graph, is_include_noise = True, is_include_main = False)
        print('Initializing with previous clustering.')
    except KeyError: # no clusters found
        if is_clean: # make noise cluster
            initial = []
            mappings_edges = get_data_maps_edges(graph, annotators)
            node2judgments, node2weights = mappings_edges['node2judgments'], mappings_edges['node2weights']
            noise = [set(get_excluded_nodes(node2judgments, node2weights, share=0.5))]
        else:
            initial = []
            noise = [{}]

        
    # Prepare graph for clustering    
    G_clean = graph.copy()    
    G_clean.remove_nodes_from([node for cluster in noise for node in cluster])
    nan_edges = get_nan_edges(G_clean)    
    G_clean.remove_edges_from(nan_edges)
    transformation = lambda x: x-threshold
    G_clean = transform_edge_weights(G_clean, transformation = transformation) # shift edge weights

    # Cluster graph
    clusters, cluster_stats = cluster_correlation_search(G_clean, s = s, max_iter = max_iter, initial = initial) # rather good performance: 2000, 50000

    # Store results
    cluster_stats = cluster_stats | {'algorithm':'correlation', 'threshold':threshold}
    graph.graph['cluster_stats'] = cluster_stats
    print(cluster_stats)
    print('number of clusters: ', len(clusters))
    node2cluster = {node:i for i, cluster in enumerate(clusters) for node in cluster} | {node:-1 for cluster in noise for node in cluster}
    graph = add_clusters(graph, node2cluster)

    with open(output_file, 'wb') as f:
        pickle.dump(graph, f, pickle.HIGHEST_PROTOCOL)

