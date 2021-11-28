
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

datadir=$dir/data
datas=($datadir/*)
outdir=$dir/graphs

for data in "${datas[@]}"
do	
    if [ ! $graphtype == "usg" ]
    then
	continue
    fi
    echo $data
    python3 scripts/sense2graph.py $data/senses.csv $outdir/$(basename "$data")
done
