
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

graphdir=$dir/graphs
graphs=($graphdir/*)
outdir=$dir/graphs
mkdir -p $outdir

for graph in "${graphs[@]}"
do
    if [ ! $split == None ] && [ ! $collapse == None ]
    then
       echo $graph
       python3 $scriptsdir/graph2collapse_split.py $graph $split $collapse 0 $outdir/$(basename "$graph")
    fi
done
