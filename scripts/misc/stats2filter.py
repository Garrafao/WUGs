import sys
import csv

[_, stats, output_file] = sys.argv
    
with open(stats, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    stats = [row for row in reader]

columns = ['lemma', 'loss', 'loss_normalized', 'conflicts', 'conflicts_normalized', 'conflicts_within_clusters', 'conflicts_between_clusters', 'uncompared_cluster_combinations', 'uncompared_multi_cluster_combinations', 'judgments_per_edge', 'nodes', 'judgments_total', 'edgeshares', 'excluded_nodes', 'lemma', 'grouping', 'nodes', 'nodes1', 'nodes2', 'cluster_freq_dist', 'cluster_freq_dist1', 'cluster_freq_dist2', 'cluster_prob_dist', 'cluster_prob_dist1', 'cluster_prob_dist2', 'change_binary', 'change_graded', 'change_binary_gain', 'change_binary_loss', 'k1', 'n1', 'k2', 'n2', 'EARLIER', 'LATER', 'COMPARE', 'annotator']
    
data_out = []    
for row in stats:
    data_row = {k:v for (k,v) in row.items() if k in columns}
    data_out.append(data_row)
        
# Export data
with open(output_file, 'w') as f:  
    w = csv.DictWriter(f, data_out[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerows(data_out)

    
