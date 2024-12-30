import sys
import csv


[_, judgments, output_file, annotator] = sys.argv

with open(judgments, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    judgments = [row for row in reader]

judgments_out = []    
for row in judgments:
    if not row['annotator']==annotator:
        judgments_out.append(row)
    
#print(judgments_out).blah

# Export data
with open(output_file, 'w') as f:  
    # write header
    header = '\t'.join(judgments_out[0].keys())
    f.write(header)
    f.write('\n')
    for row in judgments_out:
        line = '\t'.join(row.values())
        f.write(line)
        f.write('\n')
