import sys
import numpy as np
from cluster_ import transform_edge_weights
from modules import get_annotator_conflicts
from pyvis.network import Network
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from textwrap import wrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
nice_colors = [x for x in mcolors.get_named_colors_mapping().values() if isinstance(x, str)] # Nice colors
colors_global = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00'] # color-blind colors
colors_global = colors_global + nice_colors


def plot_graph_interactive(G, outDir, c2n, threshold=0.5, normalization=lambda x: x, color='colorful', period='full', mode='full', annotators = [], summary_statistic=np.median, s=2, node_size=10, node_label='cluster', edge_label_style='weight', edge_width=2, k = 0.8, position_method='spring', seed=0, pos={}, noise_color='k'):
    """
    Plots interactive graph with cluster structure.  
    :param G: Networkx graph
    :param c2n: mapping of clusters to nodes
    :param outDir: output directory
    :param threshold: edges below threshold will be plotted differently
    :param normalization: normalization function
    """

    G = G.copy() # make sure not to modify the source graph

    elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >=threshold]
    esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <threshold]
    enan=[(u,v) for (u,v,d) in G.edges(data=True) if np.isnan(d['weight'])]


    if pos=={}:
        G_pos = G.copy()        
        G_pos.remove_edges_from(enan) # Remove nan edges for finding positions       
        pos = find_node_positions(G_pos, position_method, k=k, seed=seed, threshold=threshold)

    if color == 'black':
        colors = ['black']*200
    elif color == 'blue':
        colors = ['blue']*200
    else:
        colors = colors_global
        
        
    if period == 'full':
        nodes = G.nodes()
    else:
        nodes = [node for node in G.nodes() if G.nodes()[node]['type']=='sense' or G.nodes()[node]['grouping']==period]
        
    if mode == 'pos':
        G.remove_edges_from(esmall) # Remove negative edges
    elif mode == 'neg':
        G.remove_edges_from(elarge) # Remove positive edges
    elif mode == 'conflicts':
        conflicts = get_annotator_conflicts(G, annotators, non_value=0.0, threshold=threshold, normalization=normalization)
        non_conflicts = [(u,v) for (u,v) in G.edges() if not (u,v) in conflicts]
        G.remove_edges_from(non_conflicts) # Remove non-conflicts
        #print(conflicts)
    elif mode == 'compare':
        ewithin=[(u,v) for u,v in G.edges() if G.nodes()[u]['grouping']==G.nodes()[v]['grouping']]
        G.remove_edges_from(ewithin) # Remove edges which are not between time periods
    else:
        pass       
        
    G_int = Network(height='1000px', width='1000px', directed=False, notebook=False, bgcolor='#ffffff', font_color=False, layout=None, heading=period)

    #G_int.set_template('test_template.html')

    for n, cluster in c2n.items():

        for node in cluster:
            if not node in nodes: # skip nodes not in time period
                continue
            x,y = pos[node]
            node_data = G.nodes()[node]
            #print(node_data)
            type_ = ''
            try:
                type_ = node_data['type']
            except KeyError as e:
                print('KeyError in', e)
                sentence = node_data['context']
                text = '<br>'.join(wrap(sentence,70)) if sentence!='' else ''
                print(text)
            if type_ == 'usage':
                indexes = node_data['indexes_target_sentence'].split(':')
                index_start, index_end = int(indexes[0]), int(indexes[1])
                context = node_data['context']
                preceding_data = context[:index_start]
                sentence = context[index_start:index_end]
                following_data = context[index_end:]
                preceding = '<*>' + preceding_data + '<**>'
                following = '<*>' + following_data + '<**>'                
                #print(index, sentence)
                date = node_data['date']
                grouping = node_data['grouping']
                indexes_target = node_data['indexes_target_token'].split(';')
                #print(indexes_target)
                for pair in indexes_target:
                    id1, id2 = pair.split(':')
                    id1, id2 = int(id1)-index_start, int(id2)-index_start
                    sentence = sentence[:id1] + '<b>' + sentence[id1:id2] + '</b>' + sentence[id2:]
                text = '<br>'.join(wrap(preceding+sentence+following,70))
                #print(text).blah
                meta_text = '<br>'.join([col + ': ' + node_data[col] for col in ['date', 'grouping', 'identifier', 'description', 'type'] if (node_data[col]!='-' and node_data[col]!=' ' and node_data[col]!='')])                
                if 'judgments_senses' in node_data:
                    meta_text = meta_text + '<br>judgments_senses:<ul style="font-size:8px;padding-left:1.25rem;"><li>' + '</li><li>'.join([a+': '+l for a, l in node_data['judgments_senses'].items()]) + '</li></ul>'
                text = text + '<p style="font-size:8px;"><br>' + meta_text + '</p>'
                text = text.replace('<*>', '<span style="color:#808080;">').replace('<**>', '</span>') # make protected HTML valid
                text = text.replace('[newline]', '\n') 
                #print(text)
            if type_ == 'cluster':    
                text = node
            if type_ == 'sense':    
                text = node_data['description']
                meta_text = '<br>'.join([col + ': ' + node_data[col] for col in ['type'] if (node_data[col]!='-' and node_data[col]!=' ' and node_data[col]!='')])                
                text = text + '<p style="font-size:8px;"><br>' + meta_text + '</p>'

            if node_label=='cluster':
                label = str(n)  
            if node_label=='name':
                label = str(node)  
            if node_label=='None':
                label = ' '  

            color = colors[n] if n!=-1 else noise_color   
            G_int.add_node(n_id = node,label = label,shape='circle',size=node_size,physics=False,x=x,y=y,color=color,title=text, date=date)

        
    for (i,j) in elarge:
        try:
            label = make_edge_label((i,j), G, annotators, edge_label_style=edge_label_style, normalization=normalization, summary_statistic=summary_statistic)
            G_int.add_edge(i, j, color = 'black',width=edge_width*2, label=label, weight = normalization(G[i][j]['weight']))
        except (AssertionError, KeyError) as e: # continue in case node is not in time period
            pass

    for (i,j) in esmall:
        try:                 
            label = make_edge_label((i,j), G, annotators, edge_label_style=edge_label_style, normalization=normalization, summary_statistic=summary_statistic)
            G_int.add_edge(i, j, color = 'lightgray',width=edge_width*1, label=label,weight = normalization(G[i][j]['weight'])) 
        except (AssertionError, KeyError) as e: # continue in case node is not in time period
            pass
                
    for (i,j) in enan:
        try:                 
            label = make_edge_label((i,j), G, annotators, edge_label_style=edge_label_style, normalization=normalization, summary_statistic=summary_statistic)
            G_int.add_edge(i, j, color = 'lightgray',width=edge_width*0.5, label=label,weight = normalization(G[i][j]['weight'])) 
        except (AssertionError, KeyError) as e: # continue in case node is not in time period
            pass
            
    G_int.show_buttons(filter_=['nodes', 'edges'])
    G_int.toggle_physics(False)
    #G_int.toggle_hide_nodes_on_drag(True)
    #G_int.toggle_hide_edges_on_drag(True)
    G_int.inherit_edge_colors(False)
    #G_int.from_nx(G)
    #print(G_int.nodes)
    G_int.save_graph(outDir + '.html')

    
def plot_graph_static(G, outDir, c2n, threshold=0.5, normalization=lambda x: x, color='colorful', period='full', mode='full', annotators = [], summary_statistic=np.median, s=2, node_size=80, edge_width=1, k=0.8, position_method='spring', seed=0, is_edge_labels=False, edge_label_style='weight', dpi=300, font_size_nodes=11, font_size_edges=11, node_label_style=None, pos={}, noise_color='k'):
    """
    Plots static graph with cluster structure.  
    :param G: Networkx graph
    :param clusters: list of sets of clusters for nodes in graph
    :param outDir: output directory
    :param threshold: edges below threshold will be plotted differently
    :param normalization: normalization function
    """

    G = G.copy() # make sure not to modify the source graph
        
    elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >=threshold]
    esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <threshold]
    enan=[(u,v) for (u,v,d) in G.edges(data=True) if np.isnan(d['weight'])]


    if pos=={}:
        G_pos = G.copy()        
        G_pos.remove_edges_from(enan) # Remove nan edges for finding positions       
        pos = find_node_positions(G_pos, position_method, k=k, seed=seed, threshold=threshold)
        

    if color == 'black':
        colors = ['black']*300
    elif color == 'blue':
        colors = ['blue']*300
    else:
        colors = colors_global

    #print([G.nodes()[node] for node in G.nodes()])
    #print(len(G.nodes()))
    if period == 'full':
        nodes = G.nodes()
    else:
        nodes = [node for node in G.nodes() if G.nodes()[node]['grouping']==period]

    if mode == 'pos':
        G.remove_edges_from(esmall) # Remove negative edges
    elif mode == 'neg':
        G.remove_edges_from(elarge) # Remove positive edges
    elif mode == 'conflicts':
        conflicts = get_annotator_conflicts(G, annotators, non_value=0.0, threshold=threshold, normalization=normalization)
        non_conflicts = [(u,v) for (u,v) in G.edges() if not (u,v) in conflicts]
        G.remove_edges_from(non_conflicts) # Remove non-conflicts
        #print(conflicts)
    elif mode == 'compare':
        ewithin=[(u,v) for u,v in G.edges() if G.nodes()[u]['grouping']==G.nodes()[v]['grouping']]
        G.remove_edges_from(ewithin) # Remove edges which are not between time periods
        #G.remove_nodes_from(list(nx.isolates(G))) # Remove isolates, outcomment to use
    else:
        pass       
        
    node_labels = {}
    for n, cluster in c2n.items():

        for node in cluster:
            label = ''
            color = colors[n] if n!=-1 else noise_color   
            if not node in nodes: # skip nodes not in time period
                nx.draw_networkx_nodes(G,pos,node_size=node_size,alpha=0.0,node_color=color,nodelist=[node])
                continue
            if node_label_style == 'identifier':
                label = str(node)
            if node_label_style == 'lemma':
                #print(G.nodes()[node])
                label = G.nodes()[node]['lemma'][0]
            node_labels[node] = label
            nx.draw_networkx_nodes(G,pos,node_size=node_size,alpha=1.0,node_color=color,nodelist=[node])

    edge_labels = {}        
    for (i,j) in elarge:
        if not i in nodes or not j in nodes:
            continue
        try:                 
            label = make_edge_label((i,j), G, annotators, edge_label_style=edge_label_style, normalization=normalization, summary_statistic=summary_statistic)
            edge_labels[(i,j)] = label
            nx.draw_networkx_edges(G,pos,edgelist=[(i,j)],width=edge_width*1,alpha=1.0,edge_color='k')
        except (AssertionError, KeyError) as e: # continue in case node is not in time period
            pass

    for (i,j) in esmall:
        if not i in nodes or not j in nodes:
            continue
        try:                 
            label = make_edge_label((i,j), G, annotators, edge_label_style=edge_label_style, normalization=normalization, summary_statistic=summary_statistic)
            edge_labels[(i,j)] = label
            nx.draw_networkx_edges(G,pos,edgelist=[(i,j)],width=edge_width*0.5,alpha=0.2,edge_color='k')
        except (AssertionError, KeyError) as e: # continue in case node is not in time period
            pass

    for (i,j) in enan:
        if not i in nodes or not j in nodes:
            continue
        try:                 
            label = make_edge_label((i,j), G, annotators, edge_label_style=edge_label_style, normalization=normalization, summary_statistic=summary_statistic)
            edge_labels[(i,j)] = label
            nx.draw_networkx_edges(G,pos,edgelist=[(i,j)],width=edge_width*0.2,alpha=0.2,edge_color='k')
        except (AssertionError, KeyError) as e: # continue in case node is not in time period
            pass
            
    if node_label_style != None:
        nx.draw_networkx_labels(G,pos,node_labels,font_size=font_size_nodes,font_color='k')
        
    if is_edge_labels:
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.5, font_size=font_size_edges, font_color='k')     
                
    plt.axis('off')
    plt.tight_layout()    
    plt.savefig(outDir, dpi=dpi ) # save as png
    plt.close()

def make_edge_label(edge, graph, annotators, edge_label_style='weight', normalization=lambda x: x, summary_statistic=np.median):
    """
    Make edge label.
    :param edge: edge
    :return : label
    """
    
    i, j = edge
    if edge_label_style == 'weight':
        label = normalization(graph[i][j]['weight'])
        if label.is_integer():
            label = int(label)
    elif edge_label_style == 'judgments':
        judgments = graph[i][j]['judgments']        
        values = [str(int(summary_statistic(judgments[annotator]))) if annotator in judgments else '-' for annotator in annotators]       
        label = '/'.join(values)
    else:
        sys.exit('Breaking: No valid edge label style argument provided')                
               
    return label   

def find_node_positions(G, method, transformation = lambda x: x, s=750, k=0.8, seed=0, threshold=0.5):
    """
    Find node positions with different methods.
    :param method: method for finding positions
    :param transformation: transformation function for edge weights
    :param s: constant to scale the final positions
    :param k: optimal distance between nodes for spring layout
    :param k: random seed for reproducibility
    :return n2p: dictionary mapping nodes to positions
    """
 
    G = G.copy()

    if method=='spring':
        G = transform_edge_weights(G, transformation = lambda x: (x**3)) # transform edge weights
        n2p=nx.spring_layout(G, k=k, seed=seed) # positions for all nodes
        n2p = {node:(p[0]*s,p[1]*s) for (node,p) in n2p.items()} # strongly spread nodes
    if method=='sfdp':
        G = transform_edge_weights(G, transformation = lambda x: (x**3)) # transform edge weights
        esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <threshold]
        G.remove_edges_from(esmall) # Remove negative edges for finding positions
        n2p = graphviz_layout(G,prog='sfdp')
    if method=='spectral':
        G = transform_edge_weights(G, transformation = lambda x: (x**3)) # transform edge weights
        n2p=nx.spectral_layout(G)    
        n2p = {node:(p[0]*s,p[1]*s) for (node,p) in n2p.items()} # strongly spread nodes

    return n2p
