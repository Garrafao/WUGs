
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

outdir=$dir/graphs
datadir=$dir/data
mkdir -p $outdir
datas=($datadir/*)
for data in "${datas[@]}"
do
    echo $data
    python3.9 $scriptsdir/use2graph.py $data/uses.csv $(basename "$data") $outdir/$(basename "$data")
done
