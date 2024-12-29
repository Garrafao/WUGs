
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
    python3 $scriptsdir/graph2filter.py $graph $outdir/$(basename "$graph") $annotator_filter $grouping $t1 $t2  $edgefilter $isnannodes $isnanedges $annotators
done
