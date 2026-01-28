import sys
import pickle
from modules import get_median, get_disagreement, get_noise, get_judgments, get_annotators_edges, get_groups
import csv

[_, graph, annotators, output_file] = sys.argv

with open(graph, 'rb') as f:
    graph = pickle.load(f)
name = graph.graph['lemma']
    
with open(annotators, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    annotators = [row['annotator'] for row in reader]    
    
combo2median = get_median(graph, annotators)
combo2median_cleaned = get_median(graph, annotators, filter='comedi')
combo2disagreement = get_disagreement(graph, annotators, filter='comedi')
combo2noise = get_noise(graph, annotators, share=0.5)
combo2noise_cleaned = get_noise(graph, annotators, share=0.5, filter='<2')
combo2judgments = get_judgments(graph, annotators)
combo2annotators = get_annotators_edges(graph, annotators)
combo2group = get_groups(graph)
#print(combo2group)

assert combo2median.keys() == combo2median_cleaned.keys() == combo2disagreement.keys() == combo2group.keys() == combo2judgments.keys() == combo2annotators.keys() == combo2noise.keys()

output_data = [{'identifier1':i1, 'identifier2':i2, 'median':m, 'median_cleaned':combo2median_cleaned[(i1, i2)], 'mean_disagreement_cleaned':combo2disagreement[(i1, i2)], 'noise':combo2noise[(i1, i2)], 'noise_cleaned':combo2noise_cleaned[(i1, i2)], 'judgments':list(map(str, combo2judgments[(i1, i2)])), 'annotators':combo2annotators[(i1, i2)], 'lemma':name, 'group':combo2group[(i1, i2)]} for (i1, i2), m in combo2median.items()]    
# Export data
with open(output_file, 'w') as f:  
    w = csv.DictWriter(f, output_data[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE)
    w.writeheader()
    w.writerows(output_data)
