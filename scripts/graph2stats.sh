
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

graphdir=$dir/graphs
graphs=($graphdir/*)
isheader=True
outdir=$dir/stats
mkdir -p $outdir
for graph in "${graphs[@]}"
do
    echo $graph
    python3 $scriptsdir/graph2stats.py $graph $isheader $annotators $threshold $min $max $lowerrangemin $lowerrangemax $upperrangemin $upperrangemax $lowerprob $upperprob $outdir/
    isheader=False
done
#cd $dir/ && zip -r stats.zip stats/ && cd ../..
