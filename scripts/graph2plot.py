import sys
import networkx as nx
from modules import get_clusters, get_data_maps_nodes
from plotting_ import plot_graph_interactive, plot_graph_static
import csv
from itertools import combinations
import os


[_, input_file, output_folder, color, mode, style, edge_label_style, annotators, threshold, position, modus] = sys.argv

threshold=float(threshold)
graph = nx.read_gpickle(input_file)
name = graph.graph['lemma']

try:
    clusters, c2n, n2c = get_clusters(graph, is_include_noise = True)
except KeyError:
    print('no clusters found')
    clusters, c2n, n2c = [{n for n in graph.nodes()}], {0:list(graph.nodes())}, {n:0 for n in graph.nodes()}
    
with open(annotators, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    annotators = [row['annotator'] for row in reader]

if modus=='test':
    dpi = 5
if modus=='system':
    dpi = 5
if modus=='full':
    dpi = 300

output_folder_full = output_folder + '/full/'    
if not os.path.exists(output_folder_full):
    os.makedirs(output_folder_full)    

if style=='interactive':
    plot_graph_interactive(graph, output_folder_full + name, c2n, threshold=threshold, period='full', color=color, mode=mode, edge_label_style = edge_label_style, annotators = annotators, position_method = position)
if style=='static':
    plot_graph_static(graph, output_folder_full + name, c2n, threshold=threshold, period='full', color=color, mode=mode, edge_label_style = edge_label_style, annotators = annotators, dpi=dpi, position_method = position, node_size=100)
    
mappings_nodes = get_data_maps_nodes(graph)
node2period = mappings_nodes['node2period']
periods = sorted(set(node2period.values()))
if len(periods) > 1:
    for period in periods:

        output_folder_period = output_folder + '/' + period + '/'
        if not os.path.exists(output_folder_period):
            os.makedirs(output_folder_period)    

        if style=='interactive':
            plot_graph_interactive(graph, output_folder_period + name, c2n, threshold = threshold, period=period, color=color, mode=mode, edge_label_style = edge_label_style,annotators = annotators, position_method = position)
        if style=='static':
            plot_graph_static(graph, output_folder_period + name, c2n, threshold = threshold, period=period, color=color, mode=mode, edge_label_style = edge_label_style, annotators = annotators, dpi=dpi, position_method = position, node_size=100) 

    if style=='interactive':
        output_folder_aligned = output_folder+'/aligned/'    
        if not os.path.exists(output_folder_aligned):
            os.makedirs(output_folder_aligned)    
        combos = combinations(periods, 2)
        for (old, new) in combos:
            with open(output_folder_aligned + name + '_{0}_{1}'.format(old, new) + '.html', 'w', encoding='utf-8') as f_out:
                f_out.write("<html>\n<head>\n</head>\n<frameset cols=\"50\%,\*\">\n<frame src=\"../{0}/{1}\">\n<frame src=\"../{2}/{1}\">\n</frameset>\n</html>\n".format(old, name+'.html', new))

