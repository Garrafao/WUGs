import sys
from itertools import combinations, product, chain
from collections import defaultdict, Counter
import networkx as nx
import numpy as np

def transform_edge_weights(G, transformation = lambda x: x):
    """
    Transform edge weights.       
    :param G: graph
    :param transformation: transformation function
    :return G: graph with transformed edges
    """

    G = G.copy()
    
    for (i,j) in G.edges():
        G[i][j]['weight'] = transformation(G[i][j]['weight'])
    
    return G

def transform_judgments(G, non_value=0.0, transformation = lambda x: x):
    """
    Transform judgments.       
    :param G: graph
    :param transformation: transformation function
    :return G: graph with transformed edges
    """

    G = G.copy()
    
    for (i,j) in G.edges():

        judgments = G[i][j]['judgments']

        data = {a:[transformation(v) if not v == non_value else float('nan') for v in vs] for (a,vs) in judgments.items()}
        
        G[i][j]['judgments'] = data
    
    return G

    
def get_clusters(G, is_include_noise = False, is_include_main = True, noise_label = -1):
    """
    Get clusters stored in graph.       
    :param G: graph
    :param is_include_noise: include noise cluster
    :param is_include_main: include main clusters
    :param noise_label: label for noise cluster
    :return clusters, c2n, n2c: clusters and mappings
    """

    c2n = defaultdict(lambda: [])
    n2c = {}
    for node in G.nodes():
        cluster = G.nodes()[node]['cluster']
        if cluster == noise_label and not is_include_noise:
            continue
        if cluster != noise_label and not is_include_main:
            continue
        c2n[cluster].append(node)
        n2c[node] = cluster

    c2n = dict(c2n)
    clusters = [set(c2n[c]) for c in c2n]
    clusters.sort(key=lambda x:-len(x)) # sort by size
        
    return clusters, c2n, n2c


def add_clusters(G, node2cluster, allow_missing=False, missing_label=-1):
    """
    Add clusters to graph.       
    :param G: graph
    :param allow_missing: whether to allow missing cluster labels for nodes
    :param node2cluster: mapping of nodes to clusters
    :return G: 
    """
    
    if set(G.nodes()) != set(node2cluster.keys()):
        if allow_missing:
            print('Warning: Cluster labels are missing for some nodes in graph.')
            node2cluster = node2cluster | {node:missing_label for node in G.nodes() if not node in node2cluster.keys()}
        else:
            sys.exit('Breaking: Cluster labels are missing for some nodes in graph.')
        
    nx.set_node_attributes(G, node2cluster, 'cluster')
        
    return G


def get_uncompared_clusters(G, clusters, is_non_value=lambda x: np.isnan(x)):
    """
    Get cluster combinations without connection.       
    :param G: graph
    :param clusters: clusters
    :param is_non_value: function for non-judgment
    :return uncompared: list of uncompared cluster index tuples
    """
        
    G = G.copy()
    non_jud_edges = [(i,j) for (i,j) in G.edges() if is_non_value(G[i][j]['weight'])] # exclusive no-judgment-edges
    G.remove_edges_from(non_jud_edges) # treat non-edges as non-comparisons
    uncompared = []       
    for (c1,c2) in combinations(range(len(clusters)), 2):
        cluster1, cluster2 = clusters[c1], clusters[c2]
        is_found = False
        for (i,j) in product(cluster1,cluster2):                                
            if j in G.neighbors(i):
                is_found = True
                break
        if is_found==False:
            uncompared.append((c1,c2))

    return uncompared
   

def get_low_prob_clusters(clusters, threshold=2):
    """
    Get low-probability clusters.
    :param clusters: clusters
    :param threshold: minimum size for high-probability clusters
    :return clearclusters_low_prob: list of cluster indices below threshold
    """
               
    clusters_low_prob = [c for c, cluster in enumerate(clusters) if len(cluster) < threshold]
       
    return clusters_low_prob


def make_meta_graph(graph, test_statistic=np.nanmedian):
    """
    Make meta-graph from input graph.
    :param clusters: clusters
    :return graph_meta: meta-graph
    """
               
    clusters, c2n, n2c = get_clusters(graph, is_include_noise = True)
    graph_meta = nx.Graph(lemma=graph.graph['lemma'])
    node_attribute_keys = list(graph.nodes()[list(graph.nodes().keys())[0]].keys()) # infer node format from first node in input graph
    node_attribute_keys.remove('type')
    node_attributes = {k:'-' for k in node_attribute_keys} | {'type':'cluster'}

    n2c_meta = {str(c):c for c in c2n.keys()}
    graph_meta.add_nodes_from(n2c_meta.keys())
            
    identifier2data = {node:node_attributes.copy() for node in graph_meta.nodes()}
    nx.set_node_attributes(graph_meta, identifier2data)
    
    combo2weights = defaultdict(lambda: [])
    for (u,v,d) in graph.edges(data=True):
        c1 = n2c[u]
        c2 = n2c[v]
        if c1==c2:
            continue
        d = d['weight']
        combo2weights[frozenset((c1,c2))].append(d)

    for combo, weights in combo2weights.items():
        combo = list(combo)
        graph_meta.add_edge(str(combo[0]), str(combo[1]), weight=test_statistic(weights))
       
    graph_meta = add_clusters(graph_meta, n2c_meta)
    
    return graph_meta


def cluster_accuracy(y_true, y_pred):
    """
    Calculates and returns the accuracy for two lists of labels.
    :param y_true: y_true
    :param y_pred: y_pred
    :return accuracy: accuracy
    """
    
    # compute confusion matrix
    contingency_matrix = metrics.cluster.contingency_matrix(y_true, y_pred)
    # Find best mapping between cluster labels and gold labels
    row_ind, col_ind = linear_sum_assignment(-contingency_matrix)
    #return result
    return contingency_matrix[row_ind, col_ind].sum() / np.sum(contingency_matrix)


def extract_majority_label(labels, threshold):
    """
    Gets the majority label from a list of labels.
    :param labels: labels
    :param threshold: minimum threshold for number of occurrences of majority label
    :return label: majority label
    """
    labels = list(labels)
    label2count = Counter(labels)
    majority_labels = [l for l, c in label2count.items() if c >= threshold]
    if len(majority_labels) > 0:
        label = np.random.choice(majority_labels)
    else:
        label = np.NaN  
    return label
