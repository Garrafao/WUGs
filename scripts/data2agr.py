import sys
import networkx as nx
import csv
from collections import defaultdict, Counter
from modules import *
import unicodedata

[_, annotation, min_, max_, annotators, output_file] = sys.argv
        
with open(annotators, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    user2annotator = {row['user']:row['annotator'] for row in reader}
    annotators = list(user2annotator.values())

with open(annotation, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    annotation = [(row['identifier1'],row['identifier2'],user2annotator[row['annotator']],row['judgment'],row['lemma']) for row in reader]

    
annotators = sorted(list(set(annotators)))
value_domain = [float(v) for v in range(int(min_), int(max_)+1)]
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
            non_values = [v for v in judgments if v==0.0]        
            values = [v for v in judgments if v!=0.0]
            if len(values)>0:
                j = np.median(values)
                if not j in value_domain: # exclude instances with more than one judgment from the same annotator which don't yield median in the value domain
                    j = float('nan')
            elif len(non_values)>0:
                j = 0.0
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
    
    for pair, annotator2judgment in combo2annotator2judgment.items():
        for annotator in annotators:
            judgments = annotator2judgment[annotator]
            non_values = [v for v in judgments if v==0.0]        
            values = [v for v in judgments if v!=0.0]
            if len(values)>0:
                j = np.median(values)
                if not j in value_domain: # exclude instances with more than one judgment from the same annotator which don't yield median in the value domain
                    j = float('nan')
            elif len(non_values)>0:
                j = 0.0
            else:
                j = float('nan')
            annotator2judgments[annotator].append(j)

    if lemma == 'full':
        global_judgments = [j for a, js in annotator2judgments.items() for j in js if not np.isnan(j) and not j == 0.0]
        global_distribution = Counter(global_judgments)
        #print(global_distribution)
        global_distribution = np.array([global_distribution[k] for k in sorted(global_distribution.keys())])
        #print(global_distribution).blah
        global_distribution = global_distribution/np.sum(global_distribution) # normalize

    agree_stats = {}
    edgeshares = [float(judgments2edges[j])/totalcombos for j in sorted(judgments2edges.keys())]
    edgeshares_string = ['%.2f' % (s) for s in edgeshares]
    avg_jud_no = np.nanmean(judgmentno)
    agree_stats['avg_judgment_no'] = str(avg_jud_no)

    # Get agreement between annotators
    #print(annotator2judgments)
    agreements = get_agreements(annotator2judgments, non_value=0.0, value_domain=value_domain, expected=global_distribution, combo2annotator2judgment=combo2annotator2judgment, metrics=['kri', 'kri2', 'spr'])
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

    general_stats = {'data':lemma}
    stats.append(general_stats | agree_stats)    

    
# Export stats
with open(output_file, 'w') as f:  
    w = csv.DictWriter(f, stats[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerows(stats)
