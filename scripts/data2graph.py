import csv
import pickle
import unicodedata

from modules import *

[_, judgments, uses, name, annotators, output_file, excluded, summary_statistic, non_value, map_identifiers] = sys.argv

# Open user list to exclude, if existent    
if excluded=='None':
    excluded = []
else:
    with open(excluded, encoding='utf-8') as csvfile: 
        reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
        excluded = [row['user'] for row in reader]

# Get summary statistic for edge weights        
if summary_statistic=='median':
    summary_statistic=np.median
if summary_statistic=='mean':
    summary_statistic=np.mean

if map_identifiers=='True':
    map_identifiers=True
else:
    map_identifiers=False

non_value=float(non_value)

# Initialize graph
name = unicodedata.normalize('NFC', name)
graph = nx.Graph(lemma=name, annotators=annotators, summary_statistic=summary_statistic, non_value=non_value)
    
# Open uses
with open(uses, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    uses = [row for row in reader]
    
# Add uses as nodes
identifier2data = {}
for (k, row) in enumerate(uses):
    row = row.copy() | {'type':'usage'}
    identifier = row['identifier']
    identifier2data[identifier] = row
    graph.add_node(identifier)
    
nx.set_node_attributes(graph, identifier2data)
#print(graph.nodes()[identifier])

print('number of nodes: ', len(graph.nodes()))

# Create mapping from system identifiers to use identifiers    
if map_identifiers:    
    identifier2identifier_ = {row['identifier_system']:row['identifier'] for row in uses}    
    identifier2identifier = lambda x: identifier2identifier_[x]
else:
    identifier2identifier = lambda x: x    


# Open judgments
with open(judgments, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    judgments = [row for row in reader]      

# Open annotator list
with open(annotators, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    user2annotator = {row['user']:row['annotator'] for row in reader}
    annotators = list(user2annotator.values())

# Get judgments with mapped identifiers and annotators
groups = []
if map_identifiers:
    if 'group' in judgments[0]: # get groups if exists
        groups = [(identifier2identifier(row['identifier1']),identifier2identifier(row['identifier2']),row['group']) for row in judgments if not row['annotator'] in excluded]
    judgments = [(identifier2identifier(row['identifier1']),identifier2identifier(row['identifier2']),float(row['judgment']),row['comment'],user2annotator[row['annotator']]) for row in judgments if not row['annotator'] in excluded]
else:
    if 'group' in judgments[0]:
        groups = [(row['identifier1'],row['identifier2'],row['group']) for row in judgments if not row['annotator'] in excluded]
    judgments = [(row['identifier1'],row['identifier2'],float(row['judgment']),row['comment'],user2annotator[row['annotator']]) for row in judgments if not row['annotator'] in excluded]

# Make sure judgments don't have more identifiers than uses
identifiers1 = [row[0] for row in judgments]
identifiers2 = [row[1] for row in judgments]
if not set(identifier2data.keys()) >= (set(identifiers1) | set(identifiers2)):
    identifiers_not_in_uses = {x for x in identifiers1 + identifiers2 if not x in identifier2data}
    print('Identifiers found in judgments which are not uses:', identifiers_not_in_uses)
    sys.exit('Breaking: Judgments have more identifiers than uses.')    

graph = add_annotation(graph, judgments)
graph = clean_annotation(graph, annotators=annotators, non_value=non_value) # collapse multiple judgments from same annotator
graph = make_weights(graph, annotators=annotators, summary_statistic=summary_statistic, non_value=non_value)

if groups != []:
    graph = add_edge_attribute(graph, groups, 'group', raise_errors = False) # This assumes that each edge has at least one corresponding pair in the annotation to choose the group from


with open(output_file, 'wb') as f:
    pickle.dump(graph, f, pickle.HIGHEST_PROTOCOL)

