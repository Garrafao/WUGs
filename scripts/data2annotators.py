import sys
import csv

[_, annotation, is_anonymize, output_file] = sys.argv

if is_anonymize=='True':
    is_anonymize=True
if is_anonymize=='False':
    is_anonymize=False
    
with open(annotation, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    annotation = [row for row in reader]

users = sorted(list(set([row['annotator'] for row in annotation])))

if is_anonymize:
    out_data = [{'user':user, 'annotator':'annotator'+str(i)} for i, user in enumerate(users)]
else:
    out_data = [{'user':user, 'annotator':user} for i, user in enumerate(users)]

# Export data
with open(output_file, 'w') as f:  
    w = csv.DictWriter(f, ['user', 'annotator'], delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerows(out_data)

