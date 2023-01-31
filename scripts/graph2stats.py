import sys
import networkx as nx
from modules import *
from constellation import Constellation
import csv
from itertools import combinations


[_, input_file, is_header, annotators, threshold, min_, max_, lower_range_min, lower_range_max, upper_range_min, upper_range_max, lower_prob, upper_prob, output_file] = sys.argv

threshold=float(threshold)
graph = nx.read_gpickle(input_file)
name = graph.graph['lemma']

if is_header == 'True':
    is_header = True
if is_header == 'False':
    is_header = False


with open(annotators, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    annotators = [row['annotator'] for row in reader]

graph_stats = get_graph_stats(graph, annotators, value_domain=list(range(int(min_), int(max_)+1)), limit=50, metrics=[])
cluster_stats = get_cluster_stats(graph, threshold=threshold, min_val=int(min_), max_val=int(max_))

general_stats = {'lemma':name}
stats = general_stats | cluster_stats | graph_stats

# Export stats
with open(output_file + 'stats.csv', 'a', encoding='utf-8') as f_out:
    if is_header:
        f_out.write('\t'.join([key for key in stats])+'\n')
    f_out.write('\t'.join([str(stats[key]) for key in stats])+'\n')


mappings_nodes = get_data_maps_nodes(graph)
node2period = mappings_nodes['node2period']
periods = sorted(set(node2period.values()))
combos = combinations(periods, 2)
for (old, new) in combos:
    time_stats = get_time_stats(graph, threshold=threshold, lower_range=(int(lower_range_min), int(lower_range_max)), upper_range=(int(upper_range_min), int(upper_range_max)), lower_prob=float(lower_prob), upper_prob=float(upper_prob), old=old, new=new)
    period_stats = {'grouping': '{0}_{1}'.format(old, new)}
    stats = general_stats | period_stats | time_stats

    # Export stats
    with open(output_file + 'stats_groupings' + '.csv', 'a', encoding='utf-8') as f_out:
        if is_header:
            f_out.write('\t'.join([key for key in stats])+'\n')
            is_header = False
        f_out.write('\t'.join([str(stats[key]) for key in stats])+'\n')
