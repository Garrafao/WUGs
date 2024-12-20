
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

graphdir=$dir/graphs
graphs=($graphdir/filtered/*)
outdir=$graphdir/clustered
mkdir -p $outdir

for graph in "${graphs[@]}"
do
    echo $graph
    # Option below suppresses all warnings
    python3 -W ignore $scriptsdir/graph2cluster2.py $graph $threshold $nonvalue $summarystatistic $modus $ambiguity $algorithm $degree $ismultiple $distribution $degcorr $adjacency $degreedl $iters True $dir/$annotators $outdir/$(basename "$graph")
done
