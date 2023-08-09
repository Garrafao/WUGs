
annotators=$dir/annotators.csv
modus=system
graphtype=uug
isanonymize=False
# aggregation
summarystatistic=mean # one of mean, median
excluded=None # path to file with excluded annotators (e.g. $dir/annotators_excluded.csv), or None
isnannodes=True # whether to keep nannodes
isnanedges=True # whether to keep nanedges
grouping=full # which grouping to plot, full means to plot all groupings
edgefilter=None # any special filters on edges, currently one of None, conflicts
# clustering
#algorithm=correlation # one of correlation, chinese, louvain
iters=1
min=1
threshold=2.5
max=4
degree=None # only needed for chinese whispers, one of "top", "lin", "log"
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
# system variables
echo timestamp && date +%F_%T
