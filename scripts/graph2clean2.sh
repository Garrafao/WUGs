
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

graphdir=$dir/graphs
graphs=($graphdir/*)
outdir=$dir/graphs
mkdir -p $outdir

for graph in "${graphs[@]}"
do
    echo $graph
    python3 $scriptsdir/graph2clean2.py $graph $nonvalue $annotators $isremovenan $isremovenoise $collapse 0 $stdedges $stdnodes $degreeremove $clustersizemin $clusterconnectmin $outdir/$(basename "$graph")
done
