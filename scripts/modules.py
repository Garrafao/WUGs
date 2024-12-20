import sys
from collections import defaultdict, Counter
from itertools import combinations, chain
import random
import numpy as np
from constellation import Constellation
from cluster_ import get_clusters, get_uncompared_clusters, get_low_prob_clusters, transform_edge_weights, transform_judgments
from correlation import Loss 
from scipy.stats import spearmanr, pearsonr
from scipy.spatial.distance import euclidean, cosine
import krippendorff_ as krippendorff
from sklearn.metrics import hamming_loss, cohen_kappa_score
import networkx as nx
from datetime import datetime
    
def add_annotation(G, annotation, is_non_value=lambda x: np.isnan(x)):
    """
    Update graph with annotations.
    :param G: graph
    :param annotation: mappings from edges to annotators to judgments
    :param is_non_value: function for non-judgment (missing judgment, not even 0)
    :return G: updated graph

    """
    for (i,j,judgment,comment,annotator) in annotation:

        if is_non_value(float(judgment)): # skip missing judgments (not even 0)
            continue

        if (i,j) in G.edges():
            judgments = dict(G[i][j]['judgments'])
            comments = dict(G[i][j]['comments'])
            
            if not annotator in judgments:
                judgments[annotator] = []
                comments[annotator] = []
                
            judgments[annotator].append(float(judgment))
            comments[annotator].append(comment)
                
            # Add updated dictionaries
            G[i][j]['judgments'] = judgments
            G[i][j]['comments'] = comments
            
        elif (j,i) in G.edges():
            judgments = dict(G[j][i]['judgments'])
            comments = dict(G[j][i]['comments'])
            
            if not annotator in judgments:
                judgments[annotator] = []
                comments[annotator] = []
                
            judgments[annotator].append(float(judgment))
            comments[annotator].append(float(judgment))
                
            # Add updated attributes
            G[j][i]['judgments'] = judgments
            G[j][i]['comments'] = comments
            
        else:
            judgments = {}            
            comments = {}            
            judgments[annotator] = []
            comments[annotator] = []
            judgments[annotator].append(float(judgment))
            comments[annotator].append(comment)
            # Add edge
            G.add_edge(i, j)
            G[i][j]['judgments'] = judgments
            G[i][j]['comments'] = comments
        
    return G
    
def get_edge_data(G, normalization = lambda x: x):
    """
    Get data for edges.
    :param G: graph
    :param normalization: function to normalize values (default no normalization)
    :return edge2data: mapping from edges to weights
    """

    edge2data = {}
    for (i,j) in G.edges():
        data = {}
        judgments = G[i][j]['judgments'].copy()
        comments = G[i][j]['comments'].copy()
        data['judgments'] = judgments
        data['comments'] = comments
        weight = normalization(G[i][j]['weight'])
        data['weight'] = weight
        context1 = G.nodes()[i]['context']
        context2 = G.nodes()[j]['context']
        data['context1'] = context1
        data['context2'] = context2
        edge2data[(i,j)] = data

    return edge2data

def clean_annotation(G, annotators=[], non_value=0.0):
    """
    Collapse multiple judgments from same annotator.
    :param G: graph
    :param annotators: list of annotators to be summarized
    :param non_value: value of non-judgment
    :return G: updated graph
    """
    for (i,j) in G.edges():
        for annotator in annotators:
            judgments = G[i][j]['judgments']
            if annotator in judgments:
                annotations = judgments[annotator]           
                non_values = [v for v in annotations if v==non_value]        
                values = [v for v in annotations if v!=non_value]
                if len(values)>0:
                    judgment = np.median(values)
                elif len(non_values)>0:
                    judgment = 0.0
                else:
                    judgment = float('nan')        
            
                G[i][j]['judgments'][annotator] = [judgment] 
        
    return G


def remove_annotators(G, annotators):
    """
    Remove annotator data from edges.
    :param G: graph
    :param annotators: list of annotators to be removed
    :return G: updated graph
    """
    for (i,j) in G.edges():

        judgments = G[i][j]['judgments']
        comments = G[i][j]['comments']

        judgments = {annotator:judgment for (annotator, judgment) in judgments.items() if not annotator in annotators}
        comments = {annotator:comment for (annotator, comment) in comments.items() if not annotator in annotators}
                           
        G[i][j]['judgments'] = judgments
        G[i][j]['comments'] = comments
        
    return G


def get_annotator_subgraph(G, annotators, name,
                           summary_statistic=np.median, non_value=0.0, normalization=lambda x: x):
    """
    Get annotator subgraph from graph.
    :param G: graph
    :param annotators: list of annotators to get the sub graph for
    :return subgraph: subgraph with judgments, comments and weights
    """
    subgraph = nx.Graph(lemma=name, annotators=annotators, summary_statistic=summary_statistic, non_value=non_value)
    subgraph.add_nodes_from((node, data) for node, data in G.nodes(data=True))
    
    for (i,j) in G.edges():

        judgments = G[i][j]['judgments']
        comments = G[i][j]['comments']

        judgments = {annotator:judgment for (annotator, judgment) in judgments.items() if annotator in annotators}
        comments = {annotator:comment for (annotator, comment) in comments.items() if annotator in annotators}

        if len(judgments)>0:
            subgraph.add_edge(i,j)
            subgraph[i][j]['judgments'] = judgments
            subgraph[i][j]['comments'] = comments

    subgraph = make_weights(subgraph, annotators, summary_statistic=summary_statistic, non_value=non_value, normalization=normalization)    
        
    return subgraph

def make_weights(G, annotators, summary_statistic=np.median, non_value=0.0, normalization=lambda x: x, weight_attribute='weight', is_strict=True):
    """
    Update edge weights from annotated judgments.
    :param G: graph
    :param annotators: list of annotators to be summarized
    :param summary_statistic: statistic to summarize data
    :param non_value: value of non-judgment
    :param normalization: normalization function
    :return G: updated graph
    """
    for (i,j) in G.edges():

        judgments = G[i][j]['judgments']

        values = [summary_statistic(judgments[annotator]) for annotator in annotators if annotator in judgments] # take median of multiple judgments of same annotator       
        
        if values == []:
            if is_strict:
                sys.exit('Breaking: No annotator matching edge: (%s,%s)' % (i,j))
            else:
                data = []
                
        data = [v for v in values if not v == non_value] # exclude non-values

        if data!=[]:        
            weight = normalization(summary_statistic(data))
        else:
            weight = float('nan')
            
        G[i][j][weight_attribute] = weight 
        
    return G

def scale_weights(G, mapping, annotators, exponent=1.0, non_value=0.0, normalization=lambda x: ((x-1)/3.0)):
    """
    Scale edge weights.
    :param G: graph
    :param non_value: value of non-judgment
    :return G: updated graph
    """

    if mapping == 'std': # scale by standard deviation of judgments
        
        combo2std = get_edge_std(G, annotators, non_value=non_value, normalization=normalization)
        mapping = {c:(1.0-std)*exponent for (c,std) in combo2std.items()}
    
    for (i,j) in G.edges():
        
        weight = G[i][j]['weight']
        factor = mapping[(i,j)]
        weight_scaled = weight*factor
        G[i][j]['weight'] = weight_scaled
        #print(weight,factor,weight_scaled)
        #print('-----')
        
    return G

def get_edge_std(G, annotators, non_value=0.0, normalization=lambda x: ((x-1)/3.0)):
    """
    Get edge standard deviation.
    :param G: graph
    :param annotators: list of annotators
    :return combo2std: mapping from edges to their standard deviation
    """
    
    mappings_edges = get_data_maps_edges(G, annotators)
    combo2judgments = mappings_edges['combo2judgments']
    combo2judgments_clean = {c:[normalization(j) for j in js if j != non_value and not np.isnan(j)] for (c,js) in combo2judgments.items()}
    combo2std = {c:np.std(js) for (c,js) in combo2judgments_clean.items()}
    #for (c,s) in combo2std.items():
    #    print((c,s),combo2judgments[c],combo2judgments_clean[c],G[c[0]][c[1]]['weight'])        
        
    return combo2std

def get_node_std(G, annotators, non_value=0.0, normalization=lambda x: ((x-1)/3.0)):
    """
    Get standard deviation an outgoing edges from each node.
    :param G: graph
    :param annotators: list of annotators
    :return node2stds: mapping from nodes to their standard deviation on outgoing edges
    """
    
    combo2std = get_edge_std(G, annotators, non_value=non_value, normalization=normalization)
    node2stds = defaultdict(lambda: [])
    for (i,j) in combo2std:
        std = combo2std[(i,j)]
        node2stds[i].append(std)
        node2stds[j].append(std)
    for i in nx.isolates(G):
        assert not i in node2stds
        node2stds[i] = []
        
    return dict(node2stds)

def get_nan_edges(G, weight_attribute='weight'):
    """
    Get edges with nan weights.
    :param G: graph
    :return nan_edges: list of nan edges
    """
    
    nan_edges = [(u,v) for (u,v,d) in G.edges(data=True) if np.isnan(d[weight_attribute])]
        
    return nan_edges

def get_empty_edges(G, annotators):
    """
    Get edges without annotations.
    :param G: graph
    :param annotators: list of annotators
    :return empty_edges: list of empty edges
    """
    
    empty_edges = [(i,j) for (i,j) in G.edges() if not any([True for annotator in annotators if annotator in G[i][j]['judgments']])]
        
    return empty_edges

def get_weights(G, normalization = lambda x: x):
    """
    Get weights of edges.
    :param G: graph
    :param normalization: function to normalize values (default no normalization)
    :return edge2weight: mapping from edges to weights
    """

    edge2weight = {(i,j): normalization(G[i][j]['weight']) for (i,j) in G.edges()}

    return edge2weight

def get_annotators(G):
    """
    Get all annotators who annotated a graph.
    :param G: graph
    :return annotators: list of annotators
    """

    annotators = list(set([annotator for (i,j) in G.edges() for annotator in G[i][j]['judgments'].keys()]))
              
    return annotators
        
def get_annotator_conflicts(G, annotators, non_value=0.0, deviation_min=1, normalization=lambda x: x, summary_statistic=np.median):
    """
    Get edges with conflicting judgments.
    :param G: graph
    :param annotators: list of annotators
    :param non_value: value for non-judgment
    :param deviation_min: deviation_min
    :param normalization: normalization function
    :return conflicts: list of edges with conflicts
    """

    conflicts = []

    # edges where annotators disagree
    for (i,j) in G.edges():
        
        judgments = G[i][j]['judgments']
        
        values = [summary_statistic(judgments[annotator]) for annotator in annotators if annotator in judgments] # take median of multiple judgments of same annotator       
        
        data = [v for v in values if not v == non_value] # exclude non-values
        combos = combinations(data, 2)
        has_conflict = (abs(x-y)>=deviation_min for (x,y) in combos)
        #print(data, any(has_conflict))
        if any(has_conflict):
            conflicts.append((i,j))

    return list(set(conflicts))
        
def get_annotator_overlap(combo2annotator2judgment, annotators, summary_statistic=np.median):
    """
    Get overlap between set of annotators.
    :param combo2annotator2judgment: data map
    :param annotators: list of annotators
    :return overlap: list of edges with judgments
    """

    combo2data = {}
    # edges annotated by all provided annotators
    for (c,annotator2judgment) in combo2annotator2judgment.items():
        data = [(a,d) for a in  annotators for d in [summary_statistic(annotator2judgment[a])] if not np.isnan(d)] #judgment overlap
        if len(data) == len(annotators):
            combo2data[c] = data

    return combo2data

def get_excluded_nodes(node2judgments, node2weights, non_value=0.0, share=1.0, is_non_value=lambda x: np.isnan(x)):
    """
    Get nodes to be excluded because of non_value judgments.
    :param node2judgments: data map
    :param node2weights: data map
    :param non_value: value of non-judgment
    :param share: share of edges
    :return nodes_excluded: list of excluded nodes
    """
            
    nodes_zero = [node for node in node2judgments if len([judgment for judgment in node2judgments[node] if judgment == non_value])/len(node2judgments[node]) >= share] # nodes with at least half zero-judgments
    nodes_nan = [node for node in node2weights if len([weight for weight in node2weights[node] if is_non_value(weight)]) == len(node2weights[node])] # nodes with only nan edges
    
    nodes_excluded = list(set(nodes_zero + nodes_nan))
    
    return nodes_excluded


def get_data_maps_edges(G, annotators, summary_statistic=np.median):
    """
    Get edge data maps.
    :param G: graph
    :param annotators: list of annotators
    :return : several data maps
    """

    mappings = {}
    combo2annotator2judgment = defaultdict(lambda: {})
    combo2annotator2comment = defaultdict(lambda: {})
    for (i,j) in G.edges():
        judgments = G[i][j]['judgments']        
        comments = G[i][j]['comments']        
        judgments = {annotator:summary_statistic(judgments[annotator]) for annotator in annotators if annotator in judgments}
        comments = {annotator:comments[annotator] for annotator in annotators if annotator in comments}
        for annotator in judgments:
            combo2annotator2judgment[(i,j)][annotator] = judgments[annotator]
        for annotator in comments:
            combo2annotator2comment[(i,j)][annotator] = comments[annotator]
                    
    annotator2judgments = {annotator:[summary_statistic(combo2annotator2judgment[(i,j)][annotator]) if annotator in combo2annotator2judgment[(i,j)] else float('nan') for (i,j) in combo2annotator2judgment.keys()] for annotator in annotators}

    combo2judgments = {combo:[combo2annotator2judgment[combo][annotator] for annotator in combo2annotator2judgment[combo]] for combo in combo2annotator2judgment.keys()}
    
    node2judgments = defaultdict(lambda: [])
    node2weights = defaultdict(lambda: [])
    for (i,j) in combo2judgments:
        node2judgments[i] += combo2judgments[(i,j)]
        node2judgments[j] += combo2judgments[(i,j)]
        weight = G[i][j]['weight']
        node2weights[i].append(weight)
        node2weights[j].append(weight)

    mappings['combo2annotator2judgment'] = combo2annotator2judgment    
    mappings['combo2annotator2comment'] = combo2annotator2comment    
    mappings['annotator2judgments'] = annotator2judgments    
    mappings['combo2judgments'] = combo2judgments    
    mappings['node2judgments'] = node2judgments   
    mappings['node2weights'] = node2weights    
                               
    return mappings 


def get_data_maps_nodes(G, attributes={'type':'usage'}):
    """
    Get node data maps. Ignores non-usage nodes by default.
    :param G: graph
    :return : several data maps
    """
    
    mappings = {}
    node2period = {}
    for node in G.nodes():
        node_data = G.nodes()[node]
        #print(node_data)
        if all([node_data[k]==v for (k,v) in attributes.items()]):
            node2period[node] = node_data['grouping']
                               
    mappings['node2period'] = node2period
    
    return mappings

def get_graph_stats(G, annotators, annotation_values=range(5), share=0.5, expected=None, limit=300):
    """
    Get statistics from annotated graph.
    :param G: Networkx graph
    :return stats: dictionary with statistics
    """
    
    mappings_edges = get_data_maps_edges(G, annotators)
    combo2annotator2judgment, annotator2judgments, node2judgments, node2weights = mappings_edges['combo2annotator2judgment'], mappings_edges['annotator2judgments'], mappings_edges['node2judgments'], mappings_edges['node2weights']    

    stats = {}
    judgments, combos = 0, 0
    judgmentno = []

    for (i,j) in combo2annotator2judgment:               
        values = [judgment for judgment in combo2annotator2judgment[(i,j)].values()]
        judgments += len(values)
        combos += 1
        judgmentno.append(len(values))

    judgments2edgesize = Counter(judgmentno)
    judgment_levels = sorted(judgments2edgesize.keys())
    edgesizes = [judgments2edgesize[j] for j in judgment_levels]
    avg_jud_no = np.nanmean(judgmentno)
    stats['judgments_per_edge'] = str(avg_jud_no)
    edgeshares = [float(judgments2edgesize[j])/combos if combos!=0 else float('nan') for j in judgment_levels]
    edgeshares_string = ','.join(['{0}={1:.2f}'.format(judgment_levels[i],s) for i, s in enumerate(edgeshares)])
    stats['edgeshares'] = str(edgeshares_string)
    excluded_nodes = get_excluded_nodes(node2judgments, node2weights, share=share)
    stats['excluded_nodes'] = len(excluded_nodes)
    stats['nodes'] = len(node2judgments.keys())
    
    '''
    # Get agreements between annotators
    agreements = get_agreements(annotator2judgments, non_value=non_value, value_domain=value_domain, expected=expected, metrics=metrics)
    for metric in agreements:
        for i, s in enumerate(sorted(agreements[metric].keys(), reverse=True)):
            if i==limit:
                break
            stats[metric+'_'+s] = agreements[metric][s]
    '''
            
    annotator2numberjudgments = {}  
    # Get judgment frequencies per annotator
    for annotator in annotator2judgments:
        data = annotator2judgments[annotator]
        judgments = [d for d in data if not np.isnan(d)]
        annotator2numberjudgments[annotator] = len(judgments)
        stats['judgments_'+annotator] = len(judgments)
        
    stats['judgments_total'] = np.sum(list(annotator2numberjudgments.values()))
    
    # Get judgment frequencies per judgment value
    judgment2freq = Counter(chain.from_iterable(annotator2judgments.values()))
    for j in annotation_values:
        try:
            stats['judgment_'+str(j)] = judgment2freq[j]
        except KeyError:
            pass      
        
        
    return stats


def get_agreements(annotator2judgments, non_value=0.0, level_of_measurement='ordinal', value_domain=None, expected=None, metrics=['kri', 'kri2', 'coh', 'spr', 'ham', 'prs', 'eud'], combo2annotator2judgment=None, is_data=False):
    """
    Get agreement between annotators.
    :param annotator2judgments: mapping from annotators to judgment list
    :param non_value: value of non-judgment
    :return stats: dictionary with statistics
    """
    min_value = min(value_domain)
    max_value = max(value_domain)
    max_difference = max_value - min_value

    stats = {metric:{} for metric in metrics}
    stats['overlap'] = {}
    if is_data:
        stats['overlap_data'] = {}
    for (anno1,anno2) in combinations(annotator2judgments.keys(), 2):        
        # Get data
        data1 = np.array(annotator2judgments[anno1])
        data2 = np.array(annotator2judgments[anno2])
        # replace missing values
        np.place(data1, data1==non_value, np.nan)
        np.place(data2, data2==non_value, np.nan)
        data1_ = [d for j, d in enumerate(data1) if not np.isnan(d) and not np.isnan(data2[j])] #judgment overlap
        data2_ = [d for j, d in enumerate(data2) if not np.isnan(d) and not np.isnan(data1[j])]
        stats['overlap'][anno1+','+anno2] = len(data1_)
        if is_data:
            stats['overlap_data'][anno1+','+anno2] = str(data1_) + ' / ' + str(data2_)
        # compute correlation
        if 'kri' in metrics:
            reliability_data = [data1, data2]
            try:
                #print(list(data1))
                #print(list(data2))
                kri = krippendorff.alpha(reliability_data=reliability_data, level_of_measurement=level_of_measurement, value_domain=value_domain)
            except AssertionError as e:
                kri = float('nan')
            stats['kri'][anno1+','+anno2] = kri
                
        if 'kri2' in metrics:
            if expected is None:
                sys.exit('Breaking: no expected distribution provided for kri2.')
            reliability_data = [data1, data2]
            try:
                kri = krippendorff.alpha(reliability_data=reliability_data, level_of_measurement=level_of_measurement, value_domain=value_domain, expected=expected)
            except ValueError as e:
                kri = float('nan')
            stats['kri2'][anno1+','+anno2] = kri

        if 'spr' in metrics:
            try:
                rho, p = spearmanr(data1_, data2_)
            except ValueError as e:
                rho, p = float('nan'), float('nan')
            stats['spr'][anno1+','+anno2] = rho

        if 'coh' in metrics:
            try:
                coh = cohen_kappa_score(data1_, data2_)
            except ValueError as e:
                coh = float('nan')
            stats['coh'][anno1+','+anno2] = coh

        if 'prs' in metrics:
            try:
                prs, p = pearsonr(data1_, data2_)
            except ValueError as e:
                prs, p = float('nan'), float('nan')
            stats['prs'][anno1+','+anno2] = prs

        if 'eud' in metrics:
            try:
                data1_[0]
                eud = euclidean(data1_, data2_)
                max_ = np.sqrt(len(data1_)*(max_difference**2))
                eud = 1-(eud/max_)
            except IndexError as e:
                eud = float('nan')
            stats['eud'][anno1+','+anno2] = eud

        if 'ham' in metrics:
            try:
                ham = 1.0 - hamming_loss(data1_, data2_)
            except ValueError as e:
                ham = float('nan')
            stats['ham'][anno1+','+anno2] = ham        

    if 'kri' in metrics or 'kri2' in metrics:
        reliability_data = []
        for annotator in annotator2judgments:
            # Get data
            data = np.array(annotator2judgments[annotator])
            # replace missing values
            np.place(data, data==non_value, np.nan)
            reliability_data.append(data)

        if 'kri' in metrics:
            kri = krippendorff.alpha(reliability_data=reliability_data, level_of_measurement=level_of_measurement, value_domain=value_domain) 
            stats['kri']['full'] = kri

        if 'kri2' in metrics:
            if expected is None:
                sys.exit('Breaking: no expected distribution provided for kri2.')
            #print(value_domain, expected)
            kri = krippendorff.alpha(reliability_data=reliability_data, level_of_measurement=level_of_measurement, value_domain=value_domain, expected=expected) 
            stats['kri2']['full'] = kri
    
    for metric in metrics:
        if metric == 'kri' or metric == 'kri2':
            continue       
        stats[metric]['mean'] = np.nanmean(list(stats[metric].values()))        

        overlap_total_non_nan = np.sum([overlap for pair, overlap in stats['overlap'].items() if not np.isnan(stats[metric][pair])])
        mean_weighted = np.nansum([(stats['overlap'][annotators]/overlap_total_non_nan)*stats[metric][annotators] for annotators in stats['overlap']]) # todo: take care of cases where overlap is 1
        stats[metric]['mean_weighted'] = mean_weighted       

    column2others = {i : [j for j in annotator2judgments if i!=j] for i in annotator2judgments}
    for i in column2others:
        if column2others[i] == []:
            continue
        # Get data
        data1 = np.array(annotator2judgments[i])
        data2 = np.asarray([annotator2judgments[j] for j in column2others[i]])
        # replace missing values
        np.place(data1, data1==non_value, np.nan)
        np.place(data2, data2==non_value, np.nan)
        data2 = np.nanmean(data2, dtype=np.float64, axis=0)
        data1_ = [d for j, d in enumerate(data1) if not np.isnan(d) and not np.isnan(data2[j])] #judgment overlap
        data2_ = [d for j, d in enumerate(data2) if not np.isnan(d) and not np.isnan(data1[j])]
        # compute alpha
        if 'kri' in metrics:
            reliability_data = [data1, data2]
            try:
                kri = krippendorff.alpha(reliability_data=reliability_data, level_of_measurement=level_of_measurement) # currently not done with external expected distribution, as value_domain changes for averages
            except AssertionError as e:
                kri = float('nan')
            stats['kri'][i+','+'mean_others'] = kri
                
        if 'coh' in metrics:
            try:
                coh = cohen_kappa_score(data1_, data2_)
            except ValueError as e:
                coh = float('nan')
            stats['coh'][i+','+'mean_others'] = coh

        # compute correlation
        if 'spr' in metrics:
            try:
                rho, p = spearmanr(data1_, data2_)
            except ValueError as e:
                rho, p = float('nan'), float('nan')
            stats['spr'][i+','+'mean_others'] = rho        

        if 'prs' in metrics:
            try:
                prs, p = pearsonr(data1_, data2_)
            except ValueError as e:
                prs, p = float('nan'), float('nan')
            stats['prs'][i+','+'mean_others'] = prs

        if 'eud' in metrics:
            try:
                data1_[0]
                eud = euclidean(data1_, data2_)
                max_ = np.sqrt(len(data1_)*(max_difference**2))
                eud = 1-(eud/max_)
            except IndexError as e:
                eud = float('nan')
            stats['eud'][i+','+'mean_others'] = eud
            
        # compute hamming loss
        if 'ham' in metrics:
            try:
                ham = 1.0 - hamming_loss(data1_, data2_)
            except ValueError as e:
                ham = float('nan')
            stats['ham'][i+','+'mean_others'] = ham

    return stats


def get_cluster_stats(G, threshold=0.5, min_val=0.0, max_val=1.0, loss_function='linear_loss', noise_label = -1):
    """
    Get clusters with conflicting judgments.       
    :param G: graph
    :param stats: dictionary with conflicts
    :param threshold: threshold
    :return :
    """
    try:
        clusters, _, _ = get_clusters(G, is_include_noise = False)
    except KeyError:
        print('No clusters found.')
        return {}
        
    noise, _, _ = get_clusters(G, is_include_noise = True, is_include_main = False)
    G_clean = G.copy()    
    G_clean.remove_nodes_from([node for cluster in noise for node in cluster])
    
    stats = {}
    max_error = max(threshold-min_val,max_val-threshold)

    n2i = {node:i for i, node in enumerate(G_clean.nodes())}
    i2n = {i:node for i, node in enumerate(G_clean.nodes())}
    n2c = {n2i[node]:i for i, cluster in enumerate(clusters) for node in cluster}
    
    edges_positive = set([(n2i[i],n2i[j],w-threshold) for (i,j,w) in G_clean.edges.data("weight") if w >= threshold])
    edges_negative = set([(n2i[i],n2i[j],w-threshold) for (i,j,w) in G_clean.edges.data("weight") if w < threshold])
    valid_edges = len(edges_positive) + len(edges_negative)
    
    cluster_state = np.array([n2c[n] for n in sorted(n2c.keys())])
    loss = Loss('linear_loss', edges_positive=edges_positive, edges_negative=edges_negative).loss(cluster_state)

    stats['loss'] = loss
    stats['loss_normalized'] = loss/(valid_edges*max_error) if (valid_edges*max_error) != 0.0 else 0.0

    between_conflicts = Loss('binary_loss', edges_positive=edges_positive, edges_negative=edges_negative, signs=['pos']).loss(cluster_state)
    within_conflicts = Loss('binary_loss', edges_positive=edges_positive, edges_negative=edges_negative, signs=['neg']).loss(cluster_state)
    stats['conflicts'] = between_conflicts + within_conflicts
    stats['conflicts_normalized'] = stats['conflicts']/valid_edges if valid_edges != 0.0 else 0.0
    stats['conflicts_between_clusters'] = between_conflicts
    stats['conflicts_within_clusters'] = within_conflicts

    edges_min = set([(n2i[i],n2i[j],w) for (i,j,w) in G_clean.edges.data("weight") if w == min_val])
    edges_max = set([(n2i[i],n2i[j],w) for (i,j,w) in G_clean.edges.data("weight") if w == max_val])
    edges_min_no = len(edges_min)
    edges_max_no = len(edges_max)
    edges_min_max_no = edges_min_no + edges_max_no
    loss_min = Loss('binary_loss_poles', edges_min=edges_min, edges_max=edges_max, signs=['min']).loss(cluster_state)
    loss_max = Loss('binary_loss_poles', edges_min=edges_min, edges_max=edges_max, signs=['max']).loss(cluster_state)
    loss_min_max = loss_min + loss_max
    win_min = edges_min_no - loss_min
    win_max = edges_max_no - loss_max
    win_min_max = win_min + win_max
    #stats['win_min'] = win_min
    #stats['win_max'] = win_max
    #stats['win_min_max'] = win_min_max
    stats['win_min_normalized'] = win_min / edges_min_no if edges_min_no != 0.0 else float('nan') 
    stats['win_max_normalized'] = win_max / edges_max_no if edges_max_no != 0.0 else float('nan') 
    stats['win_min_max_normalized'] = win_min_max / edges_min_max_no if edges_min_max_no != 0.0 else float('nan')   

    uncompared_cluster_combs = get_uncompared_clusters(G_clean, clusters)
    low_prob_clusters = get_low_prob_clusters(clusters)
    uncompared_high_prob_cluster_combs = [(c1,c2) for (c1,c2) in uncompared_cluster_combs if not (c1 in low_prob_clusters or c2 in low_prob_clusters)]
    stats['uncompared_cluster_combinations'] = len(uncompared_cluster_combs)
    stats['uncompared_multi_cluster_combinations'] = len(uncompared_high_prob_cluster_combs)
    stats['excluded_nodes'] = len(noise)

    try:
        cluster_stats_inner = G.graph['cluster_stats']
        #cluster_stats_inner['s'] = '20' # only used for repair reasons
        for stat in cluster_stats_inner:
            stats[stat] = cluster_stats_inner[stat]
    except KeyError:
        pass           
    
    return stats


def get_time_stats(G, threshold=0.5, lower_range=(1,3), upper_range=(3,5), lower_prob=0.01, upper_prob=0.1, old='old', new='new', attributes={'type':'usage'}):
    """
    Get time-related statistics from clustered graph.
    :param G: Networkx graph
    :return stats: dictionary with statistics
    """
    
    G = G.copy()

    stats = {}

    # Get node stats
    nodes = [node for node in G.nodes if all([G.nodes()[node][k]==v for (k,v) in attributes.items()])]
    oldnodes = [node for node in nodes if G.nodes()[node]['grouping']==old]
    newnodes = [node for node in nodes if G.nodes()[node]['grouping']==new]
    frequency = len(nodes)
    frequency1 = len(oldnodes) # this includes the noise cluster for calculation of total frequency
    frequency2 = len(newnodes)
    stats['nodes'] = frequency
    stats['nodes1'] = frequency1
    stats['nodes2'] = frequency2

    # Define thresholds
    lower_prob1 = round(lower_prob*frequency1)
    lower_prob2 = round(lower_prob*frequency2)
    upper_prob1 = round(upper_prob*frequency1)
    upper_prob2 = round(upper_prob*frequency2)
    lowerbound1 = min(max(lower_range[0],lower_prob1),lower_range[1])
    lowerbound2 = min(max(lower_range[0],lower_prob2),lower_range[1])
    upperbound1 = min(max(upper_range[0],upper_prob1),upper_range[1])
    upperbound2 = min(max(upper_range[0],upper_prob2),upper_range[1])    

    try:    
        co = Constellation(graph=G, bound1=upperbound1, bound2=upperbound2, lowerbound1=lowerbound1, lowerbound2=lowerbound2, is_prob=False, old=old, new=new, threshold=threshold)        
        is_clusters = True
    except KeyError:
        print('No clusters found.')
        is_clusters = False

    if is_clusters:    
    
        stats['cluster_freq_dist'] = co.distribution
        stats['cluster_freq_dist1'] = co.distribution1
        stats['cluster_freq_dist2'] = co.distribution2
        stats['cluster_prob_dist'] = [round(pr, 3) for pr in co.prob]
        stats['cluster_prob_dist1'] = [round(pr, 3) for pr in co.prob1]
        stats['cluster_prob_dist2'] = [round(pr, 3) for pr in co.prob2]
        stats['cluster_number'] = len(co.prob)
        stats['cluster_number1'] = len([1 for pr in co.prob1 if pr > 0.0])
        stats['cluster_number2'] = len([1 for pr in co.prob2 if pr > 0.0])
    
        stats['change_binary'] = co.c_mb
        stats['change_binary_gain'] = co.i_mb
        stats['change_binary_loss'] = co.r_mb
        stats['change_graded'] = co.c_u
    
        stats['k1'] = lowerbound1
        stats['n1'] = upperbound1
        stats['k2'] = lowerbound2
        stats['n2'] = upperbound2

    # Get DURel statistics, currently done on median edge weights, but was originally done on mean edge weights!
    non_target_nodes = [n for n in G.nodes() if not all([G.nodes()[n][k]==v for (k,v) in attributes.items()])]
    G_target = G.copy()
    G_target.remove_nodes_from(non_target_nodes) # Ignore non-usage nodes by default
    wearlier=[d['weight'] for (u,v,d) in G_target.edges(data=True) if G_target.nodes()[u]['grouping']==old and G_target.nodes()[v]['grouping']==old]
    wlater=[d['weight'] for (u,v,d) in G_target.edges(data=True) if G_target.nodes()[u]['grouping']==new and G_target.nodes()[v]['grouping']==new]
    wcompare=[d['weight'] for (u,v,d) in G_target.edges(data=True) if (G_target.nodes()[u]['grouping']==old and G_target.nodes()[v]['grouping']==new) or (G_target.nodes()[u]['grouping']==new and G_target.nodes()[v]['grouping']==old)]
    #print(wearlier)

    stats['EARLIER'] = np.nanmean(wearlier)
    stats['LATER'] = np.nanmean(wlater)
    stats['COMPARE'] = np.nanmean(wcompare)
    
    return stats


def perturb_graph(G, annotators, range_ = (1,4), share = 0.1, normalization = lambda x: x):
    """
    Perturb graph with set of random annotations      
    :param G: graph
    :param range_: range of annotation values
    :return graph: perturbed graph
    """

    G = G.copy()

    U = len(G.nodes())
    F = (U*(U-1))/2
    P = int(share*F)

    weights_noise = [random.randint(range_[0],range_[1]) for i in range(P)]
    combos = list(combinations(G.nodes(), 2))
    random.shuffle(combos)
    
    annotation = [(combos[i][0],combos[i][1],float(w),'-','annotator_noise') for i, w in enumerate(weights_noise)]
    G = add_annotation(G, annotation)    
    G = make_weights(G, annotators+['annotator_noise'], normalization=normalization, non_value=0.0)
    
    return G

def get_date_format(date_string: str) -> str:
    for fmt in ["%Y", "%Y-%m-%d"]:
        try:
            datetime.strptime(date_string, fmt)
            return fmt
        except ValueError:
            pass
    return "Unknown format"

def date_fits(date_string: str, t1: datetime, t2: datetime) -> bool:
    try:
        fmt = get_date_format(date_string)
        date = datetime.strptime(date_string, fmt)
        if t1 < date < t2:
            return True
    except ValueError:
        pass
    return False