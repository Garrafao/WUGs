import sys
from itertools import combinations, product, chain
from collections import defaultdict
import matplotlib.pyplot as plt
import random
import networkx as nx
import numpy as np
from scipy.stats import spearmanr
from networkx.algorithms.dag import transitive_closure
import six
sys.modules['sklearn.externals.six'] = six
import mlrose
import time
from sklearn import metrics
from scipy.optimize import linear_sum_assignment
import multiprocessing as mp


def cluster_correlation_search(G, s = 10, max_attempts = 200, max_iters = 5000, initial = [], split_flag = True):
    """
    Apply correlation clustering. Assumes that negative edges have weights < 0, and positive edges have weights >= 0, that edges with nan have been removed and that weights are stored under edge attribute G[i][j]['weight'].

    :param G: graph
    :param s: maximal number of senses a word can have
    :param max_attempts: number of restarts for optimization
    :param max_iters: number of iterations for optimization
    :param initial: optional clustering for initialization
    :param split_flag: optional flag, if non evidence cluster should be splitted
    :return classes, stats: list of clusters, list of stats
    """
 
    start_time = time.time()    
    stats = {}
    G = G.copy()    

    if initial == []: # initialize with connected components unless initial clustering is provided
        classes = cluster_connected_components(G)
    else:
        classes = initial

    n2i = {node:i for i, node in enumerate(G.nodes())}
    i2n = {i:node for i, node in enumerate(G.nodes())}
    n2c = {n2i[node]:i for i, cluster in enumerate(classes) for node in cluster}
   
    edges_positive = set([(n2i[i],n2i[j],G[i][j]['weight']) for (i,j) in G.edges() if G[i][j]['weight'] >= 0.0])
    edges_negative = set([(n2i[i],n2i[j],G[i][j]['weight']) for (i,j) in G.edges() if G[i][j]['weight'] < 0.0])
    
    Linear_loss = Loss('linear_loss', edges_positive=edges_positive, edges_negative=edges_negative)
    #conflict_loss = test_loss
    
    # Define initial state
    init_state = np.array([n2c[n] for n in sorted(n2c.keys())])
    loss_init = Linear_loss.loss(init_state)

    if loss_init == 0.0:
        print('loss_init: ', loss_init)
        classes.sort(key=lambda x:-len(x)) # sort by size
        end_time = time.time()
        stats['runtime'] = (end_time - start_time)/60
        return classes, stats

    l2s = defaultdict(lambda: [])
    l2s[loss_init].append((init_state,len(classes)))

    # Initialize multiprocessing.Pool()
    pool = mp.Pool(mp.cpu_count())
    #pool = mp.Pool(1)
    #print(mp.cpu_count())

    # `pool.apply`
    solutions = pool.starmap(Linear_loss.optimize_simulated_annealing, [(n, classes, G.nodes(), init_state, max_attempts, max_iters) for n in range(2,s)])
    pool.close()    
    #print(solutions[0])
    
    # Merge solutions
    for l2s_ in solutions:
        #print(l2s_)
        for (l,ss) in l2s_.items():        
            for s in ss:        
                l2s[l].append(s)

    #print(l2s.values())

    id = np.random.choice(range(len(l2s[min(l2s.keys())])))
    best_state, best_fitness = l2s[min(l2s.keys())][id], min(l2s.keys())
    print('loss: ', best_fitness)

    #print(best_state)
    best_state = best_state[0]
    #print(best_state)
    
    c2n = defaultdict(lambda: [])
    for i, c in enumerate(best_state):
        c2n[c].append(i2n[i])

    classes = [set(c2n[c]) for c in c2n]

    # Split collapsed clusters without evidence
    if split_flag: classes = split_non_evidence_clusters(G, classes)

    classes.sort(key=lambda x:-len(x)) # sort by size

    end_time = time.time()
    stats['runtime'] = (end_time - start_time)/60
    #print(stats['runtime'])
    
    return classes, stats

class Loss(object):
    """
    """
    
    def __init__(self, fitness_fn, edges_positive=None, edges_negative=None, edges_min=None, edges_max=None, signs=None):
 
        self.edges_positive = edges_positive
        self.edges_negative = edges_negative
        self.edges_min = edges_min
        self.edges_max = edges_max
        self.signs = signs
        if fitness_fn == 'test_loss':
            self.fitness_fn = self.test_loss
        if fitness_fn == 'linear_loss':
            self.fitness_fn = self.linear_loss
        if fitness_fn == 'binary_loss':
            self.fitness_fn = self.binary_loss
        if fitness_fn == 'binary_loss_poles':
            self.fitness_fn = self.binary_loss_poles

    def loss(self, state):        
        return self.fitness_fn(state)

    def test_loss(self, state):        
        return 50.0

    def linear_loss(self, state):        
        loss_pos = np.sum([w for (i,j,w) in self.edges_positive if state[i] != state[j]])
        loss_neg = np.sum([abs(w) for (i,j,w) in self.edges_negative if state[i] == state[j]])        
        loss = loss_pos + loss_neg        
        return loss

    def binary_loss(self, state):        
        loss_pos = len([1 for (i,j,w) in self.edges_positive if state[i] != state[j]])
        loss_neg = len([1 for (i,j,w) in self.edges_negative if state[i] == state[j]])
        if self.signs==['pos', 'neg']:
            loss = loss_pos + loss_neg        
        elif self.signs==['pos']:
            loss = loss_pos        
        elif self.signs==['neg']:
            loss = loss_neg
        else:
            loss = float('nan')
        return loss

    def binary_loss_poles(self, state):
        loss_min = len([1 for (i,j,w) in self.edges_min if state[i] == state[j]])
        loss_max = len([1 for (i,j,w) in self.edges_max if state[i] != state[j]])
        if self.signs==['min', 'max']:
            loss = loss_min + loss_max        
        elif self.signs==['min']:
            loss = loss_min        
        elif self.signs==['max']:
            loss = loss_max
        else:
            loss = float('nan')
        return loss

    def optimize_simulated_annealing(self, n, classes, nodes, init_state, max_attempts, max_iters):

        # Important to reseed to have different seeds in different pool processes
        np.random.seed()
        
        # Initialize custom fitness function object
        fitness_fn = mlrose.CustomFitness(self.fitness_fn)

        l2s_ = defaultdict(lambda: [])

        # With initial state
        max_val = max(n,len(classes))
        problem = mlrose.DiscreteOpt(length = len(nodes), fitness_fn = fitness_fn, maximize = False, max_val = max_val)

        # Define decay schedule
        schedule = mlrose.ExpDecay()
        # Solve problem using simulated annealing
        best_state, best_fitness = mlrose.simulated_annealing(problem, schedule = schedule, init_state = init_state, max_attempts = max_attempts, max_iters = max_iters)

        l2s_[best_fitness].append((best_state,max_val))

        # Important to reseed to have different seeds in different pool processes
        np.random.seed()
        
        # Repeat without initial state
        max_val = n
        problem = mlrose.DiscreteOpt(length = len(nodes), fitness_fn = fitness_fn, maximize = False, max_val = max_val)

        schedule = mlrose.ExpDecay()
        best_state, best_fitness = mlrose.simulated_annealing(problem, schedule = schedule, max_attempts = max_attempts, max_iters = max_iters)

        l2s_[best_fitness].append((best_state,max_val))

        return dict(l2s_)

    
def cluster_connected_components(G, is_non_value=lambda x: np.isnan(x)):
    """
    Apply connected_component clustering.       
    :param G: graph
    :return classes: list of clusters
    """

    G = G.copy()

    edges_negative = [(i,j) for (i,j) in G.edges() if G[i][j]['weight'] < 0.0 or is_non_value(G[i][j]['weight'])]
    G.remove_edges_from(edges_negative)
    components = nx.connected_components(G)
    classes = [set(component) for component in components]
    classes.sort(key=lambda x:list(x)[0])

    return classes


def split_non_evidence_clusters(G, clusters, is_non_value=lambda x: np.isnan(x)):
    """
    Split non-positively-connected components.       
    :param G: graph
    :param clusters: list of clusters
    :return G: 
    """

    G = G.copy()
    
    nodes_in = [node for cluster in clusters for node in cluster]
    edges_negative = [(i,j) for (i,j) in G.edges() if G[i][j]['weight'] < 0.0 or is_non_value(G[i][j]['weight'])]
    G.remove_edges_from(edges_negative) # treat non-edges as non-comparisons

    classes_out = []
    for cluster in clusters:
        subgraph = G.subgraph(cluster)
        components = cluster_connected_components(subgraph)
        for class_ in components:
            classes_out.append(set(class_))
     
    # check that nodes stayed the same
    nodes_out = [node for class_ in classes_out for node in class_]
    if set(nodes_in) != set(nodes_out):
        sys.exit('Breaking: nodes_in != nodes_out.')
    if len(nodes_in) != len(nodes_out):
        sys.exit('Breaking: len(nodes_in) != len(nodes_out).')
    
    return classes_out

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

    
def get_clusters(G):
    """
    Get clusters stored in graph.       
    :param G: graph
    :param classes: list of clusters
    :return G: 
    """

    c2n = defaultdict(lambda: [])
    for node in G.nodes():
        c2n[G.nodes()[node]['cluster']].append(node)
        
    classes = [set(c2n[c]) for c in c2n]
    classes.sort(key=lambda x:-len(x)) # sort by size
        
    return classes


def add_clusters(G, clusters):
    """
    Add clusters to graph.       
    :param G: graph
    :param classes: list of clusters
    :return G: 
    """

    n2c = {}
    for i, clas in enumerate(clusters):
        for node in clas:
            n2c[node] = i
            
    nx.set_node_attributes(G, n2c, 'cluster')
        
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
               
    clusters = get_clusters(graph)
    graph_meta = nx.Graph(lemma=graph.graph['lemma'])
    node_attribute_keys = list(graph.nodes()[list(graph.nodes().keys())[0]].keys()) # infer node format from first node in input graph
    node_attribute_keys.remove('type')
    node_attributes = {k:'-' for k in node_attribute_keys} | {'type':'cluster'}

    n2c = {}
    for i, clas in enumerate(clusters):
        graph_meta.add_node(str(i))
        for node in clas:
            n2c[node] = i
            
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
       
    clusters = [{n} for n in graph_meta.nodes()]
    graph_meta = add_clusters(graph_meta, clusters)
    
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
