import sys
sys.path.append('./scripts')
import networkx as nx
import numpy as np
from modules import *
from cluster_ import *
from correlation import cluster_correlation_search
from plotting_2 import plot_graph_interactive, plot_graph_static

[_, output_file] = sys.argv


# Initialize graph
graph = nx.Graph()

A, B, C, D, E, F = 'A', 'B', 'C', 'D', 'E', 'F'
graph.add_node(A,grouping='old',date='1824',preceding='',context='and taking a knife from her pocket, she opened a vein in her little arm, and dipping a feather in the blood, wrote something on a piece of white cloth, which was spread before her.',following='',index=14,type='usage')
graph.add_node(B,grouping='old',date='1842',preceding='',context='And those who remained at home had been heavily taxed to pay for the arms, ammunition; fortifications, and all the other endless expenses of a war.',following='',index=14,type='usage')
graph.add_node(C,grouping='old',date='1860',preceding='',context='and though he saw her within reach of his arm, yet the light of her eyes seemed as far off as that of a',following='',index=9,type='usage')
graph.add_node(D,grouping='new',date='1953',preceding='',context='It stood behind a high brick wall, its back windows overlooking an arm of the sea which, at low tide, was a black and stinking mud-flat',following='',index=12,type='usage')
graph.add_node(E,grouping='new',date='1975',preceding='',context='twelve miles of coastline lies in the southwest on the Gulf of Aqaba, an arm of the Red Sea. The city of Aqaba, the only port, plays.',following='',index=14,type='usage')
graph.add_node(F,grouping='new',date='1985',preceding='',context='when the disembodied arm of the Statue of Liberty jets spectacularly out of the sandy beach.',following='',index=3,type='usage')
graph.add_edge(A, B, attributes={'annotator1': 4.0})
graph.add_edge(A, B, weight=1)
graph.add_edge(A, C, weight=4)
graph.add_edge(A, D, weight=2)
graph.add_edge(A, E, weight=2)
graph.add_edge(A, F, weight=3)
graph.add_edge(B, C, weight=1)
graph.add_edge(B, D, weight=1)
graph.add_edge(B, E, weight=1)
graph.add_edge(B, F, weight=1)
graph.add_edge(C, D, weight=2)
graph.add_edge(C, E, weight=2)
graph.add_edge(C, F, weight=3)
graph.add_edge(D, E, weight=4)
graph.add_edge(D, F, weight=2)
graph.add_edge(E, F, weight=2)
#print(graph.edges())


transformation = lambda x: x-2.5
graph = transform_edge_weights(graph, transformation = transformation)
clusters, cluster_stats = cluster_correlation_search(graph, max_attempts = 200, max_iters = 500) # rather good performance: 2000, 50000
transformation = lambda x: x+2.5
graph = transform_edge_weights(graph, transformation = transformation)
node2cluster = {node:i for i, cluster in enumerate(clusters) for node in cluster}
graph = add_clusters(graph, node2cluster)
clusters, c2n, n2c = get_clusters(graph, is_include_noise=True)
#annotators = ['annotator0', 'annotator1', 'annotator2', 'annotator3', 'annotator4', 'annotator5', 'annotator6', 'annotator7', 'annotator8', 'annotator9', 'annotator10', 'annotator11', 'annotator12', 'annotator13', 'annotator14', 'annotator15']
for mode in ['full']:
    for color in ['colorful', 'lightgray']:
        for period in ['old', 'new', 'full']:
            #plot_graph_static(graph, output_file + '_' + mode + '_' + color + '_' + period + '.png', clusters, threshold = 2.5, color=color, period=period, mode=mode, test_statistic=np.median, s=2, node_size=500, edge_width=1.0, k=0.85, is_spring=True, seed=0, is_edge_labels=True, dpi=300, font_size_nodes=16, font_size_edges=11, is_node_labels=True)     
            plot_graph_static(graph, output_file + '_' + mode + '_' + color + '_' + period + '.png', c2n, threshold = 2.5, color=color, period=period, mode=mode, s=2, node_size=800, edge_width=1.0, k=0.85, position_method='spring', seed=0, dpi=300, font_size_nodes=22, font_size_edges=16, is_edge_labels=True, edge_label_style='weight',node_label_style='identifier',transformation=lambda x: (x ** 3.0), node_shape='cclusters')
            #plot_graph_interactive(graph, output_file + '_' + mode + '_' + color + '_' + period + '.png', clusters, threshold = 2.5, color=color, period=period, mode=mode, test_statistic=np.median, s=5, node_size=800, node_label='name', edge_width=1.0, k=0.85, is_spring=True, seed=0)
