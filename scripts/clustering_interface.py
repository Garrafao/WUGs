"""
This module contains multiple functions for clustering (networkx) graphs.
"""

import numpy as np
import networkx as nx
from collections import Counter

import chinese_whispers as cw
import community as community_louvain

def connected_components_clustering(graph: nx.Graph, positive_threshold: float = 0.0, is_non_value=lambda x: np.isnan(x)) -> list:
    """Clusters the graph into connected components.

    Parameters
    ----------
    graph: networkx.Graph
        The graph for which to calculate the cluster labels
    positive_threshold: float
        The threshold for the positive weight. If the weight is below this value, the edge is considered as a negative edge.
    is_non_value: function
        A function that takes a value and returns True if the value is non-value.

    Returns
    -------
    classes : list[Set[int]]
        A list of sets of nodes, where each set is a cluster

    Raises
    ------
    ValueError
        If the graph contains non-value weights
    """
    if _check_nan_weights_exits(graph):
        raise ValueError("NaN weights are not supported by the connected components method.")

    _graph = graph.copy()

    edges_negative = [(i, j) for (i, j) in _graph.edges() if _graph[i][j]['weight'] < positive_threshold or is_non_value(_graph[i][j]['weight'])]
    _graph.remove_edges_from(edges_negative)
    components = nx.connected_components(_graph)

    classes = [set(component) for component in components]
    classes.sort(key=lambda x: len(x), reverse=True)

    return classes


def chinese_whispers_clustering(graph: nx.Graph, weighting: str = 'top', iterations: int = 20, seed: int = None) -> list:
    """Cluster graph based on Chinese Whispers.

    Parameters
    ----------
    graph: networkx.Graph
        The graph for which to calculate the cluster labels
    weighting: str
        The weighting scheme to use. Can be 'top', 'lin' or 'log'
        - 'top': using weights directly
        - 'lin': normalize weights by the degree of the related node
        - 'log': normalize weights by the logarithm of the degree of the related node
    iterations: int
        The number of iterations to run the algorithm
    seed: int
        The seed for the random number generator

    Returns
    -------
    classes : list[Set[int]]
        A list of sets of nodes, where each set is a cluster

    Raises
    ------
    ValueError
        If the graph contains non-value weights
    """
    if _check_nan_weights_exits(graph):
        raise ValueError("NaN weights are not supported by the Chinese Whispers method.")

    _graph = graph.copy()

    _cw_clustering = cw.aggregate_clusters(cw.chinese_whispers(_graph, weighting=weighting, iterations=iterations, seed=seed))

    classes = [v for _, v in _cw_clustering.items()]
    classes.sort(key=lambda x: len(x), reverse=True)

    return classes


def louvain_clustering(graph: nx.Graph, init_partition: dict = None, resolution: float = 1., random_state=None) -> list:
    """Cluster graph based on Louvain Method.

    Parameters
    ----------
    graph: networkx.Graph
        The graph for which to calculate the cluster labels
    init_partition: dict
        A dictionary of node labels to cluster labels, which will be used as initial partition
    resolution: float
        The resolution parameter for the louvain method, see https://arxiv.org/pdf/0812.1770.pdf
    random_state: int, RandomState instance or None
        The random seed or state to use.


    Returns
    -------
    classes : list[Set[int]]
        A list of sets of nodes, where each set is a cluster

    Raises
    ------
    ValueError
        If the graph contains negative weights or non-value weights
    """

    if _negative_weights_exist(graph):
        raise ValueError("Negative weights are not supported by the Louvain method.")

    if _check_nan_weights_exits(graph):
        raise ValueError("NaN weights are not supported by the Louvain method.")

    _graph = graph.copy()

    _louvain_clustering = _invert_cluster_label_dict(community_louvain.best_partition(_graph, partition=init_partition, resolution=resolution, random_state=random_state))

    classes = [v for _, v in _louvain_clustering.items()]
    classes.sort(key=lambda x: len(x), reverse=True)

    return classes


def _invert_cluster_label_dict(cluster_label_dict: dict) -> dict:
    """Invert the cluster label dict.

    Parameters
    ----------
    cluster_label_dict: dict
        The cluster label dict to invert

    Returns
    -------
    inverted_cluster_label_dict: dict
        The inverted cluster label dict
    """
    inv_map = {}
    for k, v in cluster_label_dict.items():
        inv_map[v] = inv_map.get(v, set()).union({k})

    return inv_map


def _negative_weights_exist(graph: nx.Graph):
    """Check if there are negative edges in the graph.

    Parameters
    ----------
    graph: networkx.Graph
        The graph to check negative edges for

    Returns
    -------
    flag: bool
        True if there are negative edges, False otherwise
    """
    for i, j in graph.edges():
        if graph[i][j]['weight'] < 0:
            return True
    return False


def _check_nan_weights_exits(graph: nx.Graph):
    """Check if there are NaN weights in the graph.

    Parameters
    ----------
    graph: networkx.Graph
        The graph to check NaN weights for

    Returns
    -------
    flag: bool
        True if there are NaN weights, False otherwise
    """
    for i, j in graph.edges():
        if np.isnan(graph[i][j]['weight']):
            return True
    return False
