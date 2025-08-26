# Attention: modifies graphs iteratively, i.e., current run is dependent on previous run. To avoid, run full pipeline and remove graphs from last round.

scriptsdir=${0%/*}

#dataset=dwug_de_test
dataset=dwug_de_2.3.0
#dataset=chiwug_1.0.0
#dataset=chiwug_1.0.0_test

#experiments=experiments
#experiments=experiments1
#experiments=experiments_cluster_clean/experiments2
#experiments=experiments_cluster_clean/experiments3
#experiments=experiments_cluster_clean/experiments4
#experiments=experiments_cluster_clean/experiments5
experiments=experiments_cluster_clean/experiments_binary_change_thesis
#experiments=experiments_cluster_clean/experiments_test

algorithms=(correlation wsbm chinese)
#algorithms=(wsbm)
thresholds=(0.0 1.8 1.9 2.0 2.1 2.2 2.3 2.4 2.5 2.6 2.7 2.8 2.9 3.0 3.1 3.2)
#thresholds=(0.0 2.5)
#thresholds=(0.0)
#ambiguitys=("scale_edges" "remove_nodes" "None")
ambiguitys=("scale_edges" "None")
#ambiguitys=("None")
#ambiguitys=("scale_edges")
degrees=("None" "top" "lin" "log")
#degrees=("None")
ismultiple=False # only needed for wsbm, whether each edge has multiple weights (one per annotator)
distributions=("None-None" "discrete-geometric" "discrete-binomial" "discrete-poisson")
#distributions=("discrete-binomial")
#distributions=("real-exponential" "real-normal")
degcorrs=("None" "False" "True")
#degcorrs=("False")
adjacencys=("None" "False" "True")
#adjacencys=("False")


modus=full
#modus=test
graphtype=uug
isanonymize=True
map_identifiers=False
iters=2
itersglobal=$iters
min=1
max=4
summarystatistic=median
isnannodes=True # whether to keep nannodes
isnanedges=True # whether to keep nanedges
grouping=full # which grouping to keep, full means to keep all groupings
edgefilter=None # any special filters on edges, currently one of None, conflicts
nonvalue=0.0
position=spring # one of spring, sfdp, neato, spectral
colors=(colorful)
periods=(full)
modes=(full)
styles=(interactive)
edgestyles=(weight)
lowerrangemin=1
lowerrangemax=3
upperrangemin=3
upperrangemax=5
lowerprob=0.01
upperprob=0.1
templatepath=$scriptsdir/misc/DURel_filter_template.html
deviationmin=3 # minimum absolute deviation between two annotators above which a disagreement is regarded a conflict


#dir=data/experiments_cluster_clean/experiments_binary_change_thesis/dwug_de_test1 
dir=data/experiments_cluster_clean/experiments_binary_change_thesis/dwug_de_2.3.0 
#dir=data/experiments_cluster_clean/experiments_binary_change_thesis/chiwug_1.0.0_test 

annotators=$dir/annotators.csv
threshold=2.5
# Post-hoc cleaning parameters
isremovenan=True # This should be set to True for most cases
isremovenoise=True # This should be set to True for most cases
collapse=None # None or some threshold
stdedges=999 # choose 999 to remove nothing
stdnodes=999 # choose 999 to remove nothing
degreeremove=1 # choose 0 to remove nothing and 1 to remove isolates
clustersizemin=1 # size below which clusters will be removed, choose 1 to remove nothing
clusterconnectmin=0.0 # size connection percentage below which clusters will be removed, choose 0.0 to remove nothing

diroriginal=$dir

clustersizemins=(50 70 150)
for clustersizemin in "${clustersizemins[@]}"
do
    # Redefine some variables
    dir=$diroriginal/clustersizemin_$clustersizemin
    mkdir -p $dir
    cp -r $diroriginal/graphs $dir/
    source $scriptsdir/graph2clean2.sh 
    source $scriptsdir/extract_clusters.sh
    source $scriptsdir/graph2stats.sh
	thresholdplot=2.5		
	source $scriptsdir/graph2plot2.sh

done

