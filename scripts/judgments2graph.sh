
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

outdir=$dir/graphs
datadir=$dir/data
datas=($datadir/*)
mkdir -p $outdir
for data in "${datas[@]}"
do
    echo $data
    python3 $scriptsdir/judgments2graph.py $data/judgments.csv $data/uses.csv $annotators $excluded $outdir/$(basename "$data")
done
