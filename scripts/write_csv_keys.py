import sys

[_, output_location] = sys.argv

# Write the keys to the CSV file
with open(output_location + '/stats_plotting.csv', 'a', encoding='utf-8') as f_out:
    keys = ['lemma', 'node_position']
    f_out.write('\t'.join(keys) + '\n')