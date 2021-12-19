import sys
import networkx as nx
import csv
from collections import defaultdict
from modules import add_annotation, make_weights, clean_annotation

[_, annotation, uses, annotators, excluded, output_file] = sys.argv

# Try reading graph, if doesn't exist create.
try:
    graph = nx.read_gpickle(output_file)
except:
    # Initialize graph
    graph = nx.Graph()
    
with open(annotation, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    annotation = [row for row in reader]

with open(uses, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    uses = [row for row in reader]    
    try:    
        identifier2identifier_ = {row['identifier_system']:row['identifier'] for row in uses}    
        identifier2identifier = lambda x: identifier2identifier_[x]
    except KeyError:
        identifier2identifier = lambda x: x    

    
with open(annotators, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    user2annotator = {row['user']:row['annotator'] for row in reader}
    annotators = list(user2annotator.values())

try:
    with open(excluded, encoding='utf-8') as csvfile: 
        reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
        excluded = [row['user'] for row in reader]
except FileNotFoundError:
    excluded = []

annotation = [(identifier2identifier(row['identifier1']),identifier2identifier(row['identifier2']),float(row['judgment']),row['comment'],user2annotator[row['annotator']]) for row in annotation if not row['annotator'] in excluded]

normalization = lambda x: x
graph = add_annotation(graph, annotation)    
graph = clean_annotation(graph, annotators=annotators, non_value=0.0)    
graph = make_weights(graph, annotators=annotators, normalization=normalization, non_value=0.0)

nx.write_gpickle(graph, output_file)

