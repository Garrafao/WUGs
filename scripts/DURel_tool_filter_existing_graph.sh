#!/bin/bash

function install_module_if_need() {
  module=$1
  install_script=$2
  echo "Checking if $module is installed..."
  python -c "import $module" 2>/dev/null && echo "$module is installed." || eval $install_script
}

source ~/.bashrc
conda activate wug
install_module_if_need 'mlrose' 'python -m pip install https://github.com/gkhayes/mlrose/archive/refs/heads/master.zip --no-cache-dir'

scriptsdir=${0%/*}

# parameters, will be partly overridden below
parameterfile=$scriptsdir/parameters_system.sh
source $parameterfile
echo "parameterfile: $parameterfile"

# folder where the data lives.
dir=$1
dir=${dir%/}
echo "dir: $dir"

annotator_filter=$2
echo "annotator_filter: $annotator_filter"
grouping=$3
echo "grouping: $grouping"
t1=$4
echo "t1: $t1"
t2=$5
echo "t2: $t2"
edgefilter=$6
echo "edgefilter: $edgefilter"
isnanedges=$7
echo "isnanedges: $isnanedges"
isnannodes=$8
echo "isnannodes: $isnannodes"

# graph2plot2: parameters for visualization
edgestyles=$9
echo "edgestyles: $edgestyles"
thresholdplot=${10}
echo "threshold: $thresholdplot"
position=${11}
echo "position: $position"
modes=${12}
echo "modes: $modes"

distinguish_graph_types=true
graph_type1=original
graph_type2=filtered
annotators=$dir/annotators.csv
map_identifiers=false

source $scriptsdir/graph2filter.sh

source $scriptsdir/graph2plot2.sh