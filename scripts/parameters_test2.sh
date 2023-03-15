
annotators=$dir/annotators.csv
excluded=$dir/annotators_excluded.csv
modus=test
graphtype=uug
isanonymize=True
# clustering
algorithm=correlation # one of correlation, chinese, louvain
iters=1
min=1
threshold=2.5 # should be 0.0 if not correlation or chinese
max=4
degree=None # only needed for chinese whispers, one of "top", "lin", "log"
ambiguity=None # removes influence of ambiguous edges on clustering, one of "scale_edges", "remove_nodes", "None"
# plotting
templatepath=$scriptsdir/misc/DURel_filter_template.html
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
