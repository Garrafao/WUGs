import sys
import networkx as nx
import csv
from collections import defaultdict
from modules import add_annotation, make_weights, clean_annotation

[_, annotation, annotators, output_file] = sys.argv

# Try reading graph, if doesn't exist create.
try:
    graph = nx.read_gpickle(output_file)
except:
    # Initialize graph
    graph = nx.Graph()
    
with open(annotation, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    annotation = [row for row in reader]
    
with open(annotators, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    user2annotator = {row['user']:row['annotator'] for row in reader}
    annotators = list(user2annotator.values())

annotation = [(row['identifier1'],row['identifier2'],float(row['judgment']),row['comment'],user2annotator[row['annotator']]) for row in annotation]
#print(annotation)
#pair2data = defaultdict(list)
#for (identifier1, identifier2, judgment, comment, annotator) in annotation:
#    pair2data[frozenset((identifier1, identifier2))].append(judgment)
#for (pair, judgment) in pair2data.items():
#    print(judgment)
#judgment.blah

#normalization = lambda x: (x-1.0)/3
normalization = lambda x: x
graph = add_annotation(graph, annotation)    
graph = clean_annotation(graph, annotators=annotators, non_value=0.0)    
graph = make_weights(graph, annotators=annotators, normalization=normalization, non_value=0.0)

nx.write_gpickle(graph, output_file)

