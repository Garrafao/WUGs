
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

datadir=$dir/data
datas=($datadir/*)
outdir=$dir/graphs

for data in "${datas[@]}"
do
    if [ ! -f "$data/senses.csv" ]
    then
	continue
    fi
    echo $data
    python3 $scriptsdir/sense2node.py $data/senses.csv $data/judgments_senses.csv $outdir/$(basename "$data")
done
