
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

outdir=$dir/graphs
datadir=$dir/data
datas=($datadir/*)
mkdir -p $outdir
for data in "${datas[@]}"
do
    echo $data
    python3.9 $scriptsdir/judgments2graph.py $data/judgments.csv $data/uses.csv $annotators $outdir/$(basename "$data")
done
cp -r $dir/graphs $dir/graphs_full
