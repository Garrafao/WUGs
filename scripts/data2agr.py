import sys
import networkx as nx
import csv
from collections import defaultdict, Counter
from modules import *
import unicodedata
import numpy as np

[_, annotation, modus, min_, max_, annotators, excluded, output_file] = sys.argv

if modus=='test':
    metrics=['kri', 'kri2', 'spr', 'ham']
if modus=='system':
    metrics=['kri', 'spr', 'ham']
if modus=='full':
    metrics=['kri', 'kri2', 'spr', 'ham']
        
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

with open(annotation, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    annotation = [(row['identifier1'],row['identifier2'],user2annotator[row['annotator']],row['judgment'],row['lemma']) for row in reader if not row['annotator'] in excluded]

    
annotators = sorted(list(set(annotators)))
value_domain = [float(v) for v in range(int(min_), int(max_)+1)]
non_value = 0.0
combo2annotator2judgment_global = defaultdict(lambda: defaultdict(lambda: []))
lemma2combos = defaultdict(lambda: [])
for (u,v,a,j,l) in annotation:
    combo2annotator2judgment_global[frozenset((u,v))][a].append(float(j))
    lemma2combos[l].append(frozenset((u,v)))

for l, c in lemma2combos.items(): 
    lemma2combos[l] = list(set(c))

stats = []
lemmas = ['full'] + list(lemma2combos.keys())
lemma2combos['full'] = list(set(combo2annotator2judgment_global.keys()))
    
for lemma in lemmas:
    combo2annotator2judgment = {c:combo2annotator2judgment_global[c] for c in lemma2combos[lemma]}
    #print(combo2annotator2judgment)
    combo2judgments = defaultdict(lambda: [])
    for pair, annotator2judgment in combo2annotator2judgment.items():
        for annotator, judgments in annotator2judgment.items():
            if len(judgments) == 0:
                continue
            non_values = [v for v in judgments if v==non_value]        
            values = [v for v in judgments if v!=non_value]
            if len(values)>0:
                j = np.median(values)
                if not j in value_domain: # exclude instances with more than one judgment from the same annotator which don't yield median in the value domain
                    j = float('nan')
            elif len(non_values)>0:
                j = non_value
            else:
                j = float('nan')
            #print(judgments, j)
            combo2judgments[pair].append(j)

    judgments2edges = defaultdict(int)
    totalcombos = 0
    judgmentno = []
    for pair in combo2judgments:
        totalcombos += 1
        jno = len(combo2judgments[pair])
        judgments2edges[jno] += 1
        judgmentno.append(jno)
        #print(combo2judgments[pair], jno)
    #print(totalcombos)

    annotator2judgments = defaultdict(lambda: [])

    judgments_total = 0
    for pair, annotator2judgment in combo2annotator2judgment.items():
        for annotator in annotators:
            judgments = annotator2judgment[annotator]
            judgments_total += len(judgments)
            non_values = [v for v in judgments if v==non_value]        
            values = [v for v in judgments if v!=non_value]
            if len(values)>0:
                if len(values)>1:
                    j = np.median(values)
                    if not j in value_domain: # exclude instances with more than one judgment from the same annotator which don't yield median in the value domain
                        j = float('nan')
                else:
                    j = values[0]
            elif len(non_values)>0:
                j = non_value
            else:
                j = float('nan')
            #print(values, j)
            annotator2judgments[annotator].append(j)
            
    annotator2judgments = dict(annotator2judgments)

    if lemma == 'full':
        global_judgments = [j for a, js in annotator2judgments.items() for j in js if not np.isnan(j) and not j == non_value]
        global_distribution = dict(Counter(global_judgments))
        global_distribution = {v:global_distribution[v] if v in global_distribution else 0.0 for v in value_domain}
        global_distribution = np.array([global_distribution[k] for k in sorted(global_distribution.keys())])
        global_distribution = global_distribution/np.sum(global_distribution) # normalize

    agree_stats = {}
    edgeshares = [float(judgments2edges[j])/totalcombos for j in sorted(judgments2edges.keys())]
    edgeshares_string = ['%.2f' % (s) for s in edgeshares]
    avg_jud_no = np.nanmean(judgmentno)
    agree_stats['avg_judgment_no'] = str(avg_jud_no)

    # Get agreement between annotators
    #print(annotator2judgments)
    agreements = get_agreements(annotator2judgments, non_value=non_value, value_domain=value_domain, expected=global_distribution, combo2annotator2judgment=combo2annotator2judgment, metrics=metrics)
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

    agree_stats['judgments_total'] = judgments_total
    
    # Get judgment frequencies per judgment value
    judgments = [d for d in list(chain.from_iterable(annotator2judgments.values())) if not np.isnan(d)]
    judgment2freq = Counter(judgments)
    for j in value_domain + [non_value]:
        try:
            agree_stats['judgment_'+str(j)] = judgment2freq[j]
        except KeyError:
            pass
        
    general_stats = {'data':lemma}
    stats.append(general_stats | agree_stats)    

    
# Export stats
with open(output_file, 'w') as f:  
    w = csv.DictWriter(f, stats[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerows(stats)
