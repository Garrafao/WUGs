
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

graphdir=$dir/graphs
graphs=($graphdir/original/*)
outdir=$graphdir/filtered
mkdir -p $outdir

for graph in "${graphs[@]}"
do
    python3 $scriptsdir/graph2filter.py $graph $outdir/$(basename "$graph") $annotator_filter $grouping $t1 $t2  $edgefilter $isnannodes $isnanedges $dir/$annotators
done
