
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

if [ "$distinguish_graph_types" ]; then
    outdir=$dir/graphs/$graph_type2
else
    outdir=$dir/graphs
fi
datadir=$dir/data
datas=($datadir/*)
mkdir -p $outdir
for data in "${datas[@]}"
do
    echo $data
    python3 $scriptsdir/data2graph.py $data/judgments.csv $data/uses.csv $(basename "$data") $annotators $outdir/$(basename "$data") $excluded $summarystatistic $nonvalue $map_identifiers
done
