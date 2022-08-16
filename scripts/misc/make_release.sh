
dir=data/dwug_es

: '
'
outdir=$dir/release
rm -rf $outdir #!!!
mkdir -p $outdir
mkdir -p $outdir/graphs
mkdir -p $outdir/stats
mkdir -p $outdir/plots
mkdir -p $outdir/clusters
if [ -f "$dir/README.html" ]
then
    cp $dir/README.html $outdir/README.html
fi
cp -r $dir/data $outdir/data
#cp -r $dir/graphs_full $outdir/graphs/full
cp -r $dir/graphs $outdir/graphs/opt
#cp $dir/graphs/* $outdir/graphs # only for DURel/SURel
#cp -r $dir/plots_full/interactive/full/blue $outdir/plots/full
cp -r $dir/plots/interactive/full/colorful $outdir/plots/opt
#cp -r $dir/plots/interactive/full/blue/* $outdir/plots/ # only for DURel/SURel
cp -r $dir/clusters $outdir/clusters/opt
: '
'
mkdir -p $outdir/stats/opt
python3 scripts/misc/stats2filter.py $dir/stats/stats.csv $outdir/stats/opt/stats.csv
python3 scripts/misc/stats2filter.py $dir/stats/stats_groupings.csv $outdir/stats/opt/stats_groupings.csv
cp $dir/stats/stats_agreement.csv $outdir/stats/stats_agreement.csv
#cp $dir/stats/stats_groupings.csv $outdir/stats/stats_groupings.csv # only for DURel/SURel

mkdir -p $outdir/guidelines
cp -r $dir/guidelines/* $outdir/guidelines/

#copy and filter annotators
python3 scripts/misc/stats2filter.py $dir/annotators.csv $outdir/annotators.csv
: '

# SemEval
cp -r $dir/$prev/graphs $outdir/graphs/$prev
cp -r $dir/$prev/clusters $outdir/clusters/$prev
cp -r $dir/$prev/plots/interactive/full/colorful $outdir/plots/$prev
mkdir -p $outdir/stats/$prev
python3 scripts/misc/stats2filter.py $dir/$prev/stats/stats.csv $outdir/stats/$prev/stats.csv
python3 scripts/misc/stats2filter.py $dir/$prev/stats/stats_groupings.csv $outdir/stats/$prev/stats_groupings.csv
'
if [ -d "$dir/misc" ]
then
    cp -r $dir/misc $outdir/misc
fi
#rm -r $outdir/plots/*/judgments # only for DUPS

rm -rf $dir/$(basename "$dir")
rm -rf $dir/$(basename "$dir").zip
mkdir $dir/$(basename "$dir")
cp -r $dir/release/* $dir/$(basename "$dir")/
ls $dir/$(basename "$dir")
cd $dir/
zip -r $(basename "$dir").zip $(basename "$dir")
cd ../..

# to do: copy release version to semrel
cp $dir/$(basename "$dir").zip /mount/projekte50/projekte/semrel/Annotations/Semantic-Change/WUGs/$(basename "$dir").zip

# exchange release online

