import sys
import csv
import os


[_, uses1, uses2, usesoutpath] = sys.argv

with open(uses1, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    uses1 = [row for row in reader]
    identifiers1 = [row['identifier'] for row in uses1]
print(len(uses1))    

with open(uses2, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    uses2 = [row for row in reader]
print(len(uses2))    
    
usesout = [use for use in uses2 if use['identifier'] in identifiers1]
print(len(usesout))    
assert len(usesout) == len(uses1)

# Export data
with open(usesoutpath, 'w') as f:  
    # write header
    header = '\t'.join(usesout[0].keys())
    f.write(header)
    f.write('\n')
    for row in usesout:
        line = '\t'.join(row.values())
        f.write(line)
        f.write('\n')
