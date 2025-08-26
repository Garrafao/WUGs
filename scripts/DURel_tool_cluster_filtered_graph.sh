#!/bin/bash
function install_module_if_need() {
  module=$1
  install_script=$2
  echo "Checking if $module is installed..."
  python -c "import $module" 2>/dev/null && echo "$module is installed." || eval $install_script
}

source ~/.bashrc
conda activate wug
#install_module_if_need 'mlrose' 'python -m pip install https://github.com/gkhayes/mlrose/archive/refs/heads/master.zip --no-cache-dir'

scriptsdir=${0%/*}

# parameters, will be partly overridden below
parameterfile=$scriptsdir/parameters_system.sh
source $parameterfile
echo "parameterfile: $parameterfile"

# folder where the data lives.
dir=$1
dir=${dir%/}
echo "dir: $dir"

isclean=$2
echo "isclean: $isclean"

ambiguity=$3
echo "ambiguity: $ambiguity"

algorithm=$4
echo "algorithm: $algorithm"

degree=$5
echo "degree: $degree"

ismultiple=$6
echo "ismultiple: $ismultiple"

distribution=$7
echo "distribution: $distribution"

degcorr=$8
echo "degcorr: $degcorr"

adjacency=$9
echo "adjacency: $adjacency"

degreedl=${10}
echo "degreedl: $degreedl"

iters=${11}
echo "iters: $iters"

modus=${12}
echo "modus: $modus"

# graph2plot2: parameters for visualization
edgestyles=${13}
echo "edgestyles: $edgestyles"
threshold=${14}
echo "threshold: $threshold"
position=${15}
echo "position: $position"
modes=${16}
echo "modes: $modes"

summarystatistic=${17}
nonvalue=${18}

distinguish_graph_types=true
graph_type1=filtered
graph_type2=clustered
annotators=$dir/annotators.csv
map_identifiers=false

source $scriptsdir/graph2cluster2.sh

source $scriptsdir/graph2plot2.sh