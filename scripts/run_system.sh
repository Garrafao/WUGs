#!/bin/bash
# Attention: modifies graphs iteratively, i.e., current run is dependent on previous run. To avoid, run full pipeline and remove graphs from last round.

scriptsdir=${0%/*}
# folder where the data lives.
dir=$1
dir=${dir%/}
echo $dir

# parameters
source $scriptsdir/parameters_system.sh

rm -rf $dir/data_joint # when running multiple times (e.g. testing)
rm -rf $dir/graphs # when running multiple times (e.g. testing)
rm -rf $dir/plots # when running multiple times (e.g. testing)

source $scriptsdir/data2join.sh
source $scriptsdir/data2annotators.sh
source $scriptsdir/use2graph.sh
source $scriptsdir/judgments2graph.sh
source $scriptsdir/graph2cluster.sh
source $scriptsdir/graph2plot.sh

rm -rf $dir/data_joint # when running multiple times (e.g. testing)
rm -rf $dir/graphs_full # when running multiple times (e.g. testing)
rm -rf $dir/graphs # when running multiple times (e.g. testing)
rm -rf $dir/stats # when running multiple times (e.g. testing)
rm $dir/annotators.csv # when running multiple times (e.g. testing)

