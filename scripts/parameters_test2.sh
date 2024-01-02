annotators=$dir/annotators.csv
excluded=$dir/annotators_excluded.csv
modus=test
graphtype=uug
isanonymize=True
# aggregation
summarystatistic=median # one of mean, median
excluded=None # path to file with excluded annotators (e.g. $dir/annotators_excluded.csv), or None
isnannodes=True # whether to keep nannodes
isnanedges=True # whether to keep nanedges
grouping=full # which grouping to keep, full means to keep all groupings
edgefilter=None # any special filters on edges, currently one of None, conflicts
#the threshold parameter from below is also used here for the conflict edge filter, we could introduce it as separate parameter here
# clustering
algorithm=correlation # one of correlation, chinese, louvain
iters=1
nonvalue=0.0 # must be some float
scale=ordinal
min=1
threshold=2.5 # should be 0.0 if not correlation or chinese
max=4
degree=None # only needed for chinese whispers, one of "top", "lin", "log"
ismultiple=False # only needed for wsbm, whether each edge has multiple weights (one per annotator)
distribution=discrete-binomial # only needed for wsbm, distribution for edge weights, one of "real-exponential", "real-normal", "discrete-geometric", "discrete-binomial", "discrete-poisson"
degcorr=False # only needed for wsbm, degree correction
adjacency=False # only needed for wsbm, if True, the adjacency term of the description length will be included
degreedl=False # only needed for wsbm, if True, and dl == True the degree sequence description length will be included (for degree-corrected models)
ambiguity=None # removes influence of ambiguous edges on clustering, one of "scale_edges", "remove_nodes", "None"
# plotting
templatepath=$scriptsdir/misc/DURel_filter_template_springboot.html
position=spring # one of "spring", "sfdp", "spectral"
colors=(colorful)
periods=(full)
modes=(full)
styles=(interactive)
edgestyles=(weight)
thresholdplot=2.5
# change scores
lowerrangemin=1
lowerrangemax=3
upperrangemin=3
upperrangemax=5
lowerprob=0.01
upperprob=0.1
# conflicts
deviationmin=3 # minimum absolute deviation between two annotators above which a disagreement is regarded a conflict
# system variables
echo timestamp && date +%F_%T
