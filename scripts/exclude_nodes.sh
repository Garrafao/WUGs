
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

graphdir=$dir/graphs
graphs=($graphdir/*)
isheader=True
statsdir=$dir/stats
outdir=$dir/graphs
mkdir -p $outdir
mkdir -p $statsdir
for graph in "${graphs[@]}"
do	
    echo $graph
    python3.9 $scriptsdir/exclude_nodes.py $graph $statsdir/excluded_nodes.csv $isheader $annotators $outdir/$(basename "$graph")
    isheader=False
done
