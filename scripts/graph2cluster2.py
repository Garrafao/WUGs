import sys
import networkx as nx
import pickle
from modules import transform_edge_weights, make_weights, scale_weights, get_annotators, get_node_std, get_data_maps_edges, get_excluded_nodes, get_nan_edges
from cluster_ import add_clusters, get_clusters
from correlation import cluster_correlation_search
from clustering_interface import louvain_clustering, chinese_whispers_clustering
try: # only import graph_tool if it is installed, otherwise assigned default which will be expected not to be used
    from clustering_interface_wsbm import wsbm_clustering
except ImportError as e:
    print('Warning:', str(e)+'.', 'Defaulting wsbm_clustering variables. You can continue, but should not use wsbm_clustering.')
    wsbm_clustering = None
import csv
import numpy as np
 
[_, input_file, threshold, non_value, summary_statistic, modus, ambiguity, algorithm, degree, is_multiple, distribution, degcorr, adjacency, degreedl, iters, is_clean, annotators, output_file] = sys.argv

    
threshold=float(threshold)
non_value=float(non_value)
with open(input_file, 'rb') as f:
    graph = pickle.load(f)

# Get summary statistic for edge weights        
if summary_statistic=='median':
    summary_statistic=np.median
if summary_statistic=='mean':
    summary_statistic=np.mean
    
with open(annotators, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    annotators = [row['annotator'] for row in reader]
    
if is_multiple=='true' or is_multiple == 'True':
    is_multiple=True
if is_multiple=='false' or is_multiple == 'False':
    is_multiple=False
if is_multiple and not algorithm in ['wsbm']:
    sys.exit('Breaking: Multiple edge weights not supported for this clustering algorithm')

if degcorr=='true' or degcorr == 'True':
    degcorr=True
if degcorr=='false' or degcorr == 'False':
    degcorr=False

if adjacency=='true' or adjacency == 'True':
    adjacency=True
if adjacency=='false' or adjacency == 'False':
    adjacency=False

if degreedl=='true' or degreedl == 'True':
    degreedl=True
if degreedl=='false' or degreedl == 'False':
    degreedl=False
    
iters=int(iters)    
#if iters > 1 and not algorithm in ['correlation']:
#    sys.exit('Breaking: Multiple clustering iterations not supported for this clustering algorithm')
    
if is_clean=='True':
    is_clean=True
if is_clean=='False':
    is_clean=False

try: # search previous clustering for initialization
    initial, _, _ = get_clusters(graph)
    noise, _, _ = get_clusters(graph, is_include_noise = True, is_include_main = False)
    print('Initializing with previous clustering.') # has currently only effect for correlation clustering
except KeyError: # no clusters found
    if is_clean: # make noise cluster
        initial = []
        mappings_edges = get_data_maps_edges(graph, annotators, summary_statistic=summary_statistic)
        node2judgments, node2weights = mappings_edges['node2judgments'], mappings_edges['node2weights']
        noise = [set(get_excluded_nodes(node2judgments, node2weights, share=0.5, non_value=non_value))]
    else:
        initial = []
        noise = [{}]

    
# Prepare graph for clustering    
G_clean = graph.copy()
G_clean.remove_nodes_from([node for cluster in noise for node in cluster]) # Remove noise nodes before ambiguity measures
nan_edges = get_nan_edges(G_clean)    
G_clean.remove_edges_from(nan_edges)
transformation = lambda x: x-threshold
G_clean = transform_edge_weights(G_clean, transformation = transformation) # shift edge weights

# Remove influence of ambiguous nodes and edges
if ambiguity == 'remove_nodes':    
    node2stds = get_node_std(G_clean, annotators, non_value=non_value)
    nodes_high_stds = [n for n in G_clean.nodes() if np.nanmean(node2stds[n])>0.3]
    noise.append(set(nodes_high_stds))
    G_clean.remove_nodes_from(nodes_high_stds)    
if ambiguity == 'scale_edges':        
    G_clean = scale_weights(G_clean, 'std', annotators, non_value=non_value)    
if ambiguity == 'None':
    pass

if modus=='test':
    max_attempts = 10
    max_iters = 10
    s = 2
if modus=='system':
    max_attempts = 1000
    max_iters = 5000 
    s = 10
if modus=='full':
    max_attempts = 2000
    max_iters = 50000
    s = 20

    
if algorithm=='correlation':
    runtimes = []
    for i in range(iters):
        clusters, cluster_stats = cluster_correlation_search(G_clean, s = s, max_attempts = max_attempts, max_iters = max_iters, initial = initial) # rather good performance: 2000, 50000
        initial = clusters
        runtimes.append(cluster_stats['runtime'])
    cluster_stats['runtime'] = np.sum(runtimes)    
    cluster_stats = cluster_stats | {'algorithm':algorithm, 'threshold':threshold, 'ambiguity':ambiguity}
if algorithm=='chinese':
    clusters = chinese_whispers_clustering(G_clean, weighting = degree)
    cluster_stats = {}
    cluster_stats = cluster_stats | {'algorithm':algorithm, 'threshold':threshold, 'ambiguity':ambiguity, 'degree':degree}
if algorithm=='wsbm':
    if is_multiple:
        annotators_graph = get_annotators(G_clean)
        enan = []
        # make weights for each annotator
        for annotator in annotators_graph:
            G_clean = make_weights(G_clean, [annotator], non_value=non_value, weight_attribute=annotator, is_strict=False)
            enan = enan + get_nan_edges(G_clean, weight_attribute=annotator)
        enan = list(set(enan))
        G_clean.remove_edges_from(enan) # Remove nan edges where some annotator didn't have a judgment
        print('Removed {0} nan edges leaving a graph with {1} edges.'.format(len(enan),len(G_clean.edges())))
        weight_attributes = annotators_graph
    else:
        weight_attributes = ['weight']
    B_min, B_max = 1, 30 # minimum and maximum number of blocks
    niter = 100 # number of sweeps to perform
    clusters = wsbm_clustering(G_clean, is_weighted=True, weight_attributes = weight_attributes, weight_data_type = 'float', distribution = distribution, B_min = B_min, B_max = B_max, niter = niter, deg_corr = degcorr, adjacency = adjacency, degree_dl = degreedl) # attention: weight_data_type = 'int' will cast median judgments like 3.5 to 3
    cluster_stats = {}
    cluster_stats = cluster_stats | {'algorithm':algorithm, 'is_multiple':is_multiple, 'distribution':distribution, 'B_min':B_min, 'B_max':B_max, 'niter':niter, 'deg_corr':degcorr, 'adjacency':adjacency, 'degree_dl':degreedl, 'threshold':threshold, 'ambiguity':ambiguity}
if algorithm=='louvain':
    clusters = louvain_clustering(G_clean)
    cluster_stats = {}
    cluster_stats = cluster_stats | {'algorithm':algorithm, 'threshold':threshold, 'ambiguity':ambiguity}

# Store results
graph.graph['cluster_stats'] = cluster_stats
print('number of clusters: ', len(clusters))
node2cluster = {node:i for i, cluster in enumerate(clusters) for node in cluster} | {node:-1 for cluster in noise for node in cluster}
graph = add_clusters(graph, node2cluster)

with open(output_file, 'wb') as f:
    pickle.dump(graph, f, pickle.HIGHEST_PROTOCOL)
