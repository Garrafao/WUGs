
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

graphdir=$dir/graphs
graphs=($graphdir/*)
outdir=$dir/labels
mkdir -p $outdir
for graph in "${graphs[@]}"
do
    echo $graph
    python3 $scriptsdir/graph2label.py $graph $annotators $outdir/$(basename "$graph").csv
done
