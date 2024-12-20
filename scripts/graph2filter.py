import pickle
import sys
import csv
from datetime import datetime

from modules import get_annotator_conflicts, get_nan_edges, get_data_maps_edges, get_excluded_nodes, get_annotator_subgraph, get_date_format, date_fits, make_weights

[_, input_file, output_file, annotators, grouping, t1, t2, edgefilter, remove_nan_nodes, remove_nan_edges, annotators_file] = sys.argv

with open(annotators_file, encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    user2annotator = {row['user']:row['annotator'] for row in reader}


with open(input_file, 'rb') as f:
    graph = pickle.load(f)

if remove_nan_nodes== 'true':
    remove_nan_nodes=True
if remove_nan_nodes== 'false':
    remove_nan_nodes=False

if remove_nan_edges== 'true':
    remove_nan_edges=True
if remove_nan_edges== 'false':
    remove_nan_edges=False



# Apply graph postprocessing/cleaning
# 1 - Filter by annotator
graph_name = graph.graph['lemma']
summary_statistic = graph.graph['summary_statistic']
non_value = graph.graph['non_value']
if annotators == 'all':
    annotators = []
else:
    annotators = annotators.replace('"', '')
    annotators = annotators.replace('!', ' ')
    annotators = annotators.strip().split(',')
    annotators = [user2annotator[annotator] for annotator in annotators if annotator in user2annotator.keys()]
if len(annotators) > 0 and annotators[0] != '':
    print('Filtering by annotators: %s' % annotators)
    graph = get_annotator_subgraph(graph, annotators, name=graph_name, summary_statistic=summary_statistic, non_value=non_value)
    if len(graph.nodes()) == 0:
        sys.exit('Breaking: timespan filter removing all nodes: %s' % (annotators))

# 2 - Filter by grouping
if not grouping == 'full':
    print('Filtering by grouping: %s' % grouping)
    nodesgrouping = [node for node in graph.nodes() if not graph.nodes()[node]['grouping'] == grouping]
    graph.remove_nodes_from(nodesgrouping)  # Remove nodes not in grouping
    if len(graph.nodes()) == 0 and len(nodesgrouping) > 0:
        sys.exit('Breaking: grouping filter removing all nodes: %s' % grouping)

# 3 - Filter by timespan
dt_format = get_date_format(t1)
if dt_format != 'Unknown format' and dt_format == get_date_format(t2):
    print('Filtering by timespan: %s-%s' % (t1, t2))
    t1 = datetime.strptime(t1, dt_format)
    t2 = datetime.strptime(t2, dt_format)
    nodes_not_in_timespan = [node for node in graph.nodes()
                             if not date_fits(graph.nodes()[node]['date'], t1, t2)]
    if len(graph.nodes()) == 0 and len(nodes_not_in_timespan) > 0:
        sys.exit('Breaking: timespan filter removing all nodes: %s-%s' % (t1, t2))
    graph.remove_nodes_from(nodes_not_in_timespan)

# 4 - Remove non-conflict edges (only keep conflicts)
if edgefilter == 'conflicts':
    print('Filtering by conflicts')
    conflicts = get_annotator_conflicts(graph, annotators, non_value=non_value)
    non_conflicts = [(u, v) for (u, v) in graph.edges() if not (u, v) in conflicts]
    graph.remove_edges_from(non_conflicts)  # Remove non-conflicts
    # print(conflicts)
elif edgefilter == 'None':
    pass
else:
    sys.exit('Breaking: invalid edge filter argument: %s' % edgefilter)

# 5 - Remove nan edges
# Important to apply this in the second to last step
if remove_nan_edges:
    print('Filtering by nan edges')
    nan_edges = get_nan_edges(graph)
    graph.remove_edges_from(nan_edges)

# 6 - Remove nan nodes
# Important to apply this at the end because it depends on the remaining nodes in the graph which is modified by the previous steps
if remove_nan_nodes:
    print('Filtering by nan nodes')
    mappings_edges = get_data_maps_edges(graph, annotators, summary_statistic=summary_statistic)
    node2judgments, node2weights = mappings_edges['node2judgments'], mappings_edges['node2weights']
    nannodes = get_excluded_nodes(node2judgments, node2weights, share=0.5, non_value=non_value)
    graph.remove_nodes_from(nannodes)  # Remove noise nodes

with open(output_file, 'wb') as f:
    pickle.dump(graph, f, pickle.HIGHEST_PROTOCOL)