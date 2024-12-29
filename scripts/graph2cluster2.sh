
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

graphdir=$dir/graphs
if [ "$distinguish_graph_types" ]; then
    graphs=($graphdir/$graph_type1/*)
    outdir=$graphdir/$graph_type2
else
    graphs=($graphdir/*)
    outdir=$graphdir/
fi
mkdir -p $outdir

for graph in "${graphs[@]}"
do
    echo $graph
    # Option below suppresses all warnings
    python3 -W ignore $scriptsdir/graph2cluster2.py $graph $threshold $nonvalue $summarystatistic $modus $ambiguity $algorithm $degree $ismultiple $distribution $degcorr $adjacency $degreedl $iters True $annotators $outdir/$(basename "$graph")
done
