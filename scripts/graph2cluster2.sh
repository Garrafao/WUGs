
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
	    if [ ! $algorithm == correlation ]
	    then
		break
	    fi
	fi
	echo $graph
	python3 $scriptsdir/graph2cluster2.py $graph $threshold $modus $ambiguity $algorithm $degree True $annotators $outdir/$(basename "$graph")
   done
done
