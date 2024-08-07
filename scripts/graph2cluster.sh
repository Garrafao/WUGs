
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

graphdir=$dir/graphs
graphs=($graphdir/*)
outdir=$graphdir
mkdir -p $outdir

for graph in "${graphs[@]}"
do
    for (( c=1; c<=$iters; c++ ))
    do
	if [ $c -eq 2 ]
	then
	   mkdir -p $dir/graphs1
	   cp $graph $dir/graphs1/$(basename "$graph")
	fi
	echo $graph
	# Option below suppresses all warnings
	python3 -W ignore $scriptsdir/graph2cluster.py $graph $threshold $modus True $annotators $outdir/$(basename "$graph")
    done
done
