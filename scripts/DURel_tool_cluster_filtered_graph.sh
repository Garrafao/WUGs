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
thresholdplot=${14}
echo "thresholdplot: $thresholdplot"
position=${15}
echo "position: $position"
modes=${16}
echo "modes: $modes"

summarystatistic=${17}
nonvalue=${18}

threshold=${19}

distinguish_graph_types=true
graph_type1=filtered
graph_type2=clustered
annotators=$dir/annotators.csv

source $scriptsdir/graph2cluster2.sh

source $scriptsdir/graph2plot2.sh