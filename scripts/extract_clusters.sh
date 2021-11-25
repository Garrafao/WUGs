
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

graphdir=$dir/graphs
graphs=($graphdir/*)
outdir=$dir/clusters
mkdir -p $outdir
for graph in "${graphs[@]}"
do
    echo $graph
    python3.9 $scriptsdir/extract_clusters.py $graph $outdir/$(basename "$graph").csv
done
