#!/bin/bash
# Can be used like this: bash -e scripts/run_system2.sh $dir $algorithm $position
# Attention: modifies graphs iteratively, i.e., current run is dependent on previous run. To avoid, run full pipeline and remove graphs from last round.

scriptsdir=${0%/*}
# folder where the data lives.
dir=$1
dir=${dir%/}
echo "dir: $dir"

# parameters, will be partly overridden below
parameterfile=$5
source $parameterfile
echo "parameterfile: $parameterfile"

algorithm=$2
echo "algorithm: $algorithm"

threshold=$3
echo "threshold: $threshold"

if [ $algorithm == louvain ]
then
    threshold=0.0
    echo 'Adjusting threshold for Louvain method'
    echo "threshold: $threshold"
fi
if [ $algorithm == chinese ]
then
    degree=top
    echo "degree: $degree"
fi

position=$4
echo "position: $position"

rm -rf $dir/data_joint # when running multiple times (e.g. testing)
rm -rf $dir/graphs # when running multiple times (e.g. testing)
rm -rf $dir/plots # when running multiple times (e.g. testing)

source $scriptsdir/data2join.sh
source $scriptsdir/data2annotators.sh
source $scriptsdir/data2agr.sh
source $scriptsdir/data2graph.sh # aggregates the graph according to input options
source $scriptsdir/graph2cluster2.sh
source $scriptsdir/graph2stats.sh
source $scriptsdir/graph2plot2.sh

#rm -rf $dir/data_joint # when running multiple times (e.g. testing)
#rm -rf $dir/graphs_full # when running multiple times (e.g. testing)
#rm -rf $dir/graphs # when running multiple times (e.g. testing)
#rm -rf $dir/stats # when running multiple times (e.g. testing)
#rm $dir/annotators.csv # when running multiple times (e.g. testing)

#todo: remove dependency on data2agr and graph2stats, remove multiple unnecessary plots in system version
