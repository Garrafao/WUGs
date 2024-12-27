#!/bin/bash
scriptsdir=${0%/*}

# parameters, will be partly overridden below
parameterfile=$scriptsdir/parameters_system2.sh
source $parameterfile
echo "parameterfile: $parameterfile"

# folder where the data lives.
dir=$1
dir=${dir%/}
echo "dir: $dir"

# data2annotators: whether to anonymize the annotators
isanonymize=$2
echo "isanonymize: $isanonymize"

# data2graph
summarystatistic=$3
echo "summarystatistic: $summarystatistic"
nonvalue=$4
echo "nonvalue: $nonvalue"

# graph2plot2: parameters for visualization
edgestyles=$5
echo "edgestyles: $edgestyles"
thresholdplot=$6
echo "threshold: $thresholdplot"
position=$7
echo "position: $position"
modes=$8
echo "modes: $modes"

graph_type2=original
annotators=$dir/annotators.csv

rm -rf $dir/data_joint # when running multiple times (e.g. testing)
rm -rf $dir/graphs # when running multiple times (e.g. testing)
rm -rf $dir/plots # when running multiple times (e.g. testing)
rm -rf $dir/stats # when running multiple times (e.g. testing)
rm -f $dir/annotators.csv # when running multiple times (e.g. testing)

source $scriptsdir/map_data_structure.sh
source $scriptsdir/data2join.sh
source $scriptsdir/data2annotators.sh
source $scriptsdir/data2graph.sh

source $scriptsdir/graph2plot2.sh