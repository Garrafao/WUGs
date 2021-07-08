
# Attention: modifiesgraphs iteratively, i.e., current run is dependent on previous run. To avoid, run full pipeline and remove graphs from last round.

# specify script directory
scriptsdir=${0%/*}

# specify data directory
dir=test1

# load parameters
source $scriptsdir/parameters_test.sh
#source $scriptsdir/parameters_opt.sh
#source $scriptsdir/parameters_semeval.sh

# remove when running multiple times (e.g. testing)
rm -rf $dir/data_joint
rm -rf $dir/graphs
rm -rf $dir/graphs_full
rm -rf $dir/graphs1
rm -rf $dir/clusters
rm -rf $dir/stats

# run pipeline
source $scriptsdir/data2join.sh
source $scriptsdir/data2annotators.sh # skip if annotator mapping is manual
source $scriptsdir/data2agr.sh
source $scriptsdir/use2graph.sh 
source $scriptsdir/sense2node.sh
source $scriptsdir/judgments2graph.sh
source $scriptsdir/exclude_nodes.sh
source $scriptsdir/graph2cluster.sh
source $scriptsdir/extract_clusters.sh
source $scriptsdir/graph2stats.sh
