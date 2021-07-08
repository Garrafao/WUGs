import sys
from collections import defaultdict
from docopt import docopt
import random
import numpy as np
from scipy.stats import entropy
from scipy.spatial import distance
from cluster_ import get_clusters

               
class Constellation(object):
    """
    Semantic Constellation that can be instantiated by providing two distributions:
    
        Constellation(distribution1=distribution1, distribution2=distribution1)

    Attributes
    ----------
    distribution1 : list, old word frequency distribution
    distribution2 : list, new word frequency distribution
    ...

    Notes
    -----

    -

    Examples
    --------
    
    -

    """
    
    def __init__(self, distribution1=None, distribution2=None, old='old', new='new', graph=None, is_cluster=False, algorithm=None, threshold=0.5, bound1=1, bound2=1, lowerbound1=1, lowerbound2=1, is_prob=False):
 
        self.distribution1 = distribution1
        self.distribution2 = distribution2
        self.prob1 = None
        self.prob2 = None
        
        self.distribution = None
        
        self.G = None
        self.oldnodes = None
        self.newnodes = None         
        self.restnodes = None         
        self.nodes = None
        self.clusters = None
        self.clustersold = None
        self.clustersnew = None
        self.cluster_stats = None
        self.cluster_conflicts = None

        self.usenoearlier = None
        self.usenolater = None
        self.meaningnoearlier = None
        self.meaningnolater = None      
        self.newuseno = None
        self.olduseno = None
        self.newmeaningno = None
        self.oldmeaningno = None

        self.c_u = None
        self.i_m = None
        self.r_m = None
        self.c_m = None
        self.i_mb = None
        self.r_mb = None
        self.c_mb = None
        
        if self.distribution1!=None and self.distribution2!=None:
                
            self.prob1 = list(distribution1/np.sum(distribution1))
            self.prob2 = list(distribution2/np.sum(distribution2))
            self.distribution = [x+y for x,y in zip(distribution1, distribution2)]
            self.prob = list(self.distribution/np.sum(self.distribution))
            self._make_graph(old=old, new=new) 
            self._make_change_scores(bound1=bound1, bound2=bound2, lowerbound1=lowerbound1, lowerbound2=lowerbound2, is_prob=is_prob) 
            
        elif graph!=None:

            self.G = graph
            self._make_graph_stats(old=old, new=new)

            if is_cluster:
                self._make_dist(algorithm=algorithm, threshold=threshold)
            else:
                clusters = get_clusters(graph)
                self._make_cluster_stats(clusters, threshold=threshold)
                
            self._make_change_scores(bound1=bound1, bound2=bound2, lowerbound1=lowerbound1, lowerbound2=lowerbound2, is_prob=is_prob)             
            
        else:
            sys.exit('Breaking. No valid input: provide either distributions or graph to instantiate.')
            

    def _make_dist(self, algorithm=None, threshold=0.5):
        """
        Get distributions from graph.  
        :param self: Constellation instance
        :param algorithm: algorithm for clustering
        """

        self._cluster_graph(algorithm, threshold=threshold)
        
            
    def _cluster_graph(self, algorithm, **kwargs):
        """
        Cluster graph.  
        :param self: Constellation instance
        :param algorithm: algorithm for clustering
        :param cutoff: threshold for cutoff algorithm
        :param is_conflicts: whether to search for low-conflict clusterings
        """

        graph, classes = cluster_graph(self.G, algorithm, **kwargs)
        self.G = graph
        self._make_cluster_stats(classes, threshold=kwargs['threshold'])
        
        
    def _make_cluster_stats(self, clusters, threshold=0.5):
        """
        Get basic statistics from clusters.  
        :param self: Constellation instance
        :param clusters: list of clusters
        """

        self.clusters = clusters
        self.clustersold = [set([use for use in cluster if use in self.oldnodes]) for cluster in self.clusters]
        self.clustersnew = [set([use for use in cluster if use in self.newnodes]) for cluster in self.clusters]
        self.distribution =  [len(cluster) for cluster in self.clusters]
        self.distribution1 = [len(cluster) for cluster in self.clustersold]
        self.distribution2 = [len(cluster) for cluster in self.clustersnew]
        self.prob1 = list(self.distribution1/np.sum(self.distribution1))
        self.prob2 = list(self.distribution2/np.sum(self.distribution2))
        self.prob = list(self.distribution/np.sum(self.distribution))

        
    def _make_graph_stats(self, old='old', new='new'):
        """
        Get basic statistics from graph.  
        :param self: Constellation instance
        """

        self.nodes = list(self.G.nodes)
        self.oldnodes = [node for node in self.nodes if self.G.nodes()[node]['grouping']==old]
        self.newnodes = [node for node in self.nodes if self.G.nodes()[node]['grouping']==new]
        self.restnodes = [node for node in self.nodes if (not self.G.nodes()[node]['grouping']==new) and (not self.G.nodes()[node]['grouping']==old)]

        if len(self.oldnodes + self.newnodes)!=len(self.nodes):
            #sys.exit('Breaking. Found non-time-tagged nodes.')
            #print('Found non-time-tagged nodes.')
            pass

        # to-do: add old and new subgraph    

                    
    def _make_dist_stats(self, bound1=1, bound2=1, lowerbound1=1, lowerbound2=1, is_prob=False):
        """
        Get basic statistics from distributions.  
        :param self: Constellation instance
        """

        if is_prob:
            distribution1 = self.prob1
            distribution2 = self.prob2
        else:
            distribution1 = self.distribution1
            distribution2 = self.distribution2

        if len(distribution1)!=len(distribution2):
            sys.exit('Breaking. Distributions have different lengths.')
                
        self.usenoearlier = np.sum(distribution1)
        self.usenolater = np.sum(distribution2)
        
        # Bound-related statistics
        self.meaningnoearlier = np.sum([1 if f1>=bound1 else 0 for f1 in distribution1])
        self.meaningnolater = np.sum([1 if f2>=bound2 else 0 for f2 in distribution2])           
        self.newuseno = np.sum([f2 for (f1,f2) in zip(distribution1,distribution2) if f1<=lowerbound1 and f2>=bound2])
        self.olduseno = np.sum([f1 for (f1,f2) in zip(distribution1,distribution2) if f2<=lowerbound2 and f1>=bound1])
        self.newmeaningno = int(np.sum([1 for (f1,f2) in zip(distribution1,distribution2) if f1<=lowerbound1 and f2>=bound2]))
        self.oldmeaningno = int(np.sum([1 for (f1,f2) in zip(distribution1,distribution2) if f2<=lowerbound2 and f1>=bound1]))

 
    def _make_change_scores(self, bound1=1, bound2=1, lowerbound1=1, lowerbound2=1, is_prob=False):
        """
        Compute change scores between both distributions.  
        :param self: Constellation instance
        :param bound: lower threshold for binary notions
        """
        
        self._make_dist_stats(bound1=bound1, bound2=bound2, lowerbound1=lowerbound1, lowerbound2=lowerbound2, is_prob=is_prob)

        if self.usenoearlier!=0 and self.usenolater!=0:           
        
            ## Compute change measure
            # Jensen-Shannon distance
            c_u = distance.jensenshannon(self.distribution1, self.distribution2, 2.0)

            # Absolute notions
            i_m = self.newmeaningno
            r_m = self.oldmeaningno
            c_m = i_m + r_m
            # Binary notions
            i_mb = 1 if i_m > 0 else 0
            r_mb = 1 if r_m > 0 else 0
            c_mb = 1 if i_m > 0 or r_m > 0 else 0
            
            self.c_u = c_u
            self.i_m = i_m
            self.r_m = r_m
            self.c_m = c_m
            self.i_mb = i_mb
            self.r_mb = r_mb
            self.c_mb = c_mb
        
    def _make_graph(self, old='old', new='new'):
        """
        Makes graph from two distributions.  
        :param self: Constellation instance
        """
    
        # To-do: make cluster generation smarter
        
        s1 = self.distribution1
        s2 = self.distribution2
        clustersno = len(s1)
          
        clustersold = {}
        clustersnew = {}
        clusters = {}
        cnames = []
        for n in range(clustersno):
            cname = alpha[n]
            cnames.append(cname)
            # Generate t1
            cluster = ['use_%s_old_%d' % (alpha[n], i) for i in range(s1[n])]
            clustersold[cname] = cluster
            # Generate t2
            cluster = ['use_%s_new_%d' % (alpha[n], i) for i in range(s2[n])]
            clustersnew[cname] = cluster
            # Get unified cluster
            clusters[cname] = clustersold[cname] + clustersnew[cname]

        # Generate graph
        G=nx.Graph() # Full graph

        # Add nodes
        oldnodes = [u for l in clustersold.values() for u in l]
        newnodes = [u for l in clustersnew.values() for u in l]            
        for u in oldnodes:
            G.add_node(u,period=old)
        for u in newnodes:
            G.add_node(u,period=new)


        # Connect clusters
        for (n1,n2) in product(range(clustersno), repeat=2):
            cname1 = alpha[n1]
            cname2 = alpha[n2]
            # Weight within clusters
            if n1==n2:                    
                for (i,j) in combinations(clustersold[cname1]+clustersnew[cname1], 2):
                    weight = np.random.choice([4])
                    G.add_edge(i,j,weight=weight)
                 
            # Weight between clusters
            else:
                for (i,j) in product(clustersold[cname1]+clustersnew[cname1], clustersold[cname2]+clustersnew[cname2]):
                    weight = np.random.choice([2])
                    G.add_edge(i,j,weight=weight)

        self.G = G
        self.oldnodes = oldnodes
        self.newnodes = newnodes
        self.nodes = oldnodes + newnodes
        self.clusters = [clusters[cname] for cname in clusters]
        self.clustersold = [clustersold[cname] for cname in clusters]
        self.clustersnew = [clustersnew[cname] for cname in clusters]
        
