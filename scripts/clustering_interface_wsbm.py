"""
This module contains multiple functions for clustering (networkx) graphs.
"""

import numpy as np
import networkx as nx
from collections import Counter

import graph_tool
from graph_tool.inference import minimize_blockmodel_dl
from graph_tool.inference.blockmodel import BlockState


def wsbm_clustering(graph: nx.Graph, distribution: str = 'discrete-binomial', is_weighted: bool = False, weight_data_type: str = 'int', weight_attributes = ['weight']) -> list:
    """ Cluster graph based on Weighted Stochastic Block Model.

    Parameters
    ----------
    graph: networkx.Graph
        The graph for which to calculate the cluster labels
    distribution: str
        The distribution to use for the WSBM algorithm.
        Can be "real-exponential", "real-normal", "discrete-geometric", "discrete-poisson" or "discrete-binomial"

    Returns
    -------
    classes : list[Set[int]]
        A list of sets of nodes, where each set is a cluster

    Raises
    ------
    ValueError
        If the graph contains negative weights or non-value weights
    """

    if _negative_weights_exist(graph, weight_attributes = weight_attributes):
        raise ValueError("Negative weights are not supported by the WSBM algorithm.")

    if _check_nan_weights_exits(graph, weight_attributes = weight_attributes):
        raise ValueError("NaN weights are not supported by the WSBM algorithm.")

    gt_graph, _, gt2nx = _nxgraph_to_graphtoolgraph(graph.copy(), is_weighted = is_weighted, weight_data_type = weight_data_type, weight_attributes = weight_attributes)
    state: BlockState = _minimize(gt_graph, distribution, weight_attributes = weight_attributes)

    block2clusterid_map = {}
    for i, (k, _) in enumerate(dict(sorted(Counter(state.get_blocks().get_array()).items(), key=lambda item: item[1], reverse=True)).items()):
        block2clusterid_map[k] = i

    communities = {}
    for i, block_id in enumerate(state.get_blocks().get_array()):
        nx_vertex_id = gt2nx[i]
        community_id = block2clusterid_map[block_id]
        if communities.get(community_id, None) is None:
            communities[community_id] = []
        communities[community_id].append(nx_vertex_id)

    classes = [set(v) for _, v in communities.items()]
    classes.sort(key=lambda x: len(x), reverse=True)

    return classes


def _nxgraph_to_graphtoolgraph(graph: nx.Graph, is_weighted: bool = False, weight_data_type: str = 'int', weight_attributes: list = ['weight']):
    """Convert a networkx graph to a graphtool graph.

    Parameters
    ----------
    graph: networkx.Graph
        The graph to convert

    Returns
    -------
    gt_graph: graphtool.Graph
        The converted graph
    """
    graph_tool_graph = graph_tool.Graph(directed=False)

    nx2gt_vertex_id = dict()
    gt2nx_vertex_id = dict()
    for i, node in enumerate(graph.nodes()):
        nx2gt_vertex_id[node] = i
        gt2nx_vertex_id[i] = node
        v = graph_tool_graph.add_vertex()
        assert i == v

    if is_weighted:
        for i, j in graph.edges():
            graph_tool_graph.add_edge(nx2gt_vertex_id[i], nx2gt_vertex_id[j])
  
        for attribute in weight_attributes:
            new_weights = []
            for i, j in graph.edges():
                current_weight = graph[i][j][attribute]
                #print(current_weight)
                new_weights.append(current_weight)

            original_edge_weights = graph_tool_graph.new_edge_property(weight_data_type)
            original_edge_weights.a = new_weights
            graph_tool_graph.ep[attribute] = original_edge_weights
    else:
        for i, j in graph.edges():
            graph_tool_graph.add_edge(nx2gt_vertex_id[i], nx2gt_vertex_id[j])
        

    new_vertex_id = graph_tool_graph.new_vertex_property('string')
    for k, v in nx2gt_vertex_id.items():
        new_vertex_id[v] = str(k)
    graph_tool_graph.vp.id = new_vertex_id

    return graph_tool_graph, nx2gt_vertex_id, gt2nx_vertex_id



def _minimize(graph: graph_tool.Graph, distribution: str, weight_attributes: list = ['weight']) -> BlockState:
    """Minimize the graph using the given distribution as described by graph-tool.

    Parameters
    ----------
    graph: graphtool.Graph
        The graph to minimize
    distribution: str
        The distribution to use for the WSBM algorithm.

    Returns
    -------
    state: BlockState
        The minimized graph as BlockState object.
    """

    return minimize_blockmodel_dl(graph,
                                  state_args=dict(deg_corr=False, recs=[graph.ep[attr] for attr in weight_attributes], rec_types=[distribution for attr in weight_attributes]),
                                  multilevel_mcmc_args=dict(B_min=1, B_max=30, niter=100, entropy_args=dict(adjacency=False, degree_dl=False)))


def _negative_weights_exist(graph: nx.Graph, weight_attributes: list = ['weight']):
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
    for attr in weight_attributes:
        for i, j in graph.edges():
            print(graph[i][j][attr])
            if graph[i][j][attr] < 0:
                return True
        return False


def _check_nan_weights_exits(graph: nx.Graph, weight_attributes: list = ['weight']):
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
    for attr in weight_attributes:
        for i, j in graph.edges():
            if np.isnan(graph[i][j][attr]):
                return True
        return False
