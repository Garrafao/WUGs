
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

outdir=$dir/graphs/original
datadir=$dir/data
datas=($datadir/*)
mkdir -p $outdir
for data in "${datas[@]}"
do
    echo $data
    python3 $scriptsdir/data2graph.py $data/annotations.csv $data/uses.csv $(basename "$data") $dir/$annotators $outdir/$(basename "$data") $excluded $summarystatistic $nonvalue
done
