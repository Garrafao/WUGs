import sys
import networkx as nx
import csv
from collections import defaultdict
from modules import *
import unicodedata

[_, annotation, name, min_, max_, annotators, output_file] = sys.argv
        
with open(annotators, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    user2annotator = {row['user']:row['annotator'] for row in reader}
    annotators = list(user2annotator.values())

with open(annotation, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    annotation = [(row['identifier1'],row['identifier2'],user2annotator[row['annotator']],row['judgment']) for row in reader]
    
name = unicodedata.normalize('NFC', name)

combo2annotator2judgment = defaultdict(lambda: defaultdict(lambda: []))
combo2judgments = defaultdict(lambda: [])
for (u,v,a,j) in annotation:
    combo2annotator2judgment[frozenset((u,v))][a].append(float(j))

for pair in combo2annotator2judgment.keys():
    for annotator in combo2annotator2judgment[pair]:
        non_values = [v for v in combo2annotator2judgment[pair][annotator] if v==0.0]        
        values = [v for v in combo2annotator2judgment[pair][annotator] if v!=0.0]
        if len(values)>0:
            j = np.median(values)
        elif len(non_values)>0:
            j = 0.0
        else:
            j = float('nan')
        combo2judgments[pair].append(j)

judgments2edges = defaultdict(int)
totalcombos = 0
judgmentno = []
for pair in combo2judgments:
    totalcombos += 1
    jno = len(combo2judgments[pair])
    judgments2edges[jno] += 1
    judgmentno.append(jno)

annotators = sorted(list(set(annotators)))
annotator2judgments = defaultdict(lambda: [])
for pair in combo2annotator2judgment:
    for annotator in annotators:
        non_values = [v for v in combo2annotator2judgment[pair][annotator] if v==0.0]        
        values = [v for v in combo2annotator2judgment[pair][annotator] if v!=0.0]
        if len(values)>0:
            j = np.median(values)
        elif len(non_values)>0:
            j = 0.0
        else:
            j = float('nan')
        j = np.median(values)
        annotator2judgments[annotator].append(j)

agree_stats = {}
edgeshares = [float(judgments2edges[j])/totalcombos for j in sorted(judgments2edges.keys())]
edgeshares_string = ['%.2f' % (s) for s in edgeshares]
avg_jud_no = np.nanmean(judgmentno)
agree_stats['avg_judgment_no'] = str(avg_jud_no)

# Get Spearman correlation between annotators
agreements = get_agreements(annotator2judgments, non_value=0.0, value_domain=list(range(int(min_), int(max_)+1)),combo2annotator2judgment=combo2annotator2judgment, metrics=['kri','spr'])
limit = 50
for metric in agreements:
    for i, s in enumerate(sorted(agreements[metric].keys(), reverse=True)):
        if i==limit:
            break
        agree_stats[metric+'_'+s] = agreements[metric][s]

annotator2numberjudgments = {}  
# Get judgment frequencies per annotator
for annotator in annotator2judgments:
    data = annotator2judgments[annotator]
    judgments = [d for d in data if not np.isnan(d)]
    annotator2numberjudgments[annotator] = len(judgments)
    agree_stats['judgments_'+annotator] = len(judgments)

agree_stats['judgments_total'] = np.sum(list(annotator2numberjudgments.values()))


general_stats = {'data':name}
stats = general_stats | agree_stats

    
# Export stats
with open(output_file, 'w', encoding='utf-8') as f_out:
    for (k,v) in stats.items():
        f_out.write('{0}\t{1}\n'.format(k,v))
