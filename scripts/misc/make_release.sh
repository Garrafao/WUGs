 # Define input folder
dir=data/lexicographer_project/swewug_2.0.0

# Remove previous data from release folder
outdir=$dir/release
rm -rf $outdir

# Make release folder and subfolders
mkdir -p $outdir
#mkdir -p $outdir/graphs
#mkdir -p $outdir/stats
mkdir -p $outdir/plots
#mkdir -p $outdir/clusters

# Copy data, graphs, plots and clusters
cp -r $dir/data $outdir/data
cp -r $dir/graphs $outdir/graphs
#cp -r $dir/graphs $outdir/ # for data without clusters
cp -r $dir/plots/interactive/full/colorful/weight $outdir/plots/weight
cp -r $dir/clusters $outdir/clusters
#cp -r $dir/plots/interactive/full/blue $outdir/plots/full # for data without clusters
#cp -r $dir/plots/interactive/compare/blue $outdir/plots/compare # for data without clusters

# Copy and filter stats
mkdir -p $outdir/stats
python3 scripts/misc/stats2filter.py $dir/stats/stats.csv $outdir/stats/stats.csv
python3 scripts/misc/stats2filter.py $dir/stats/stats_groupings.csv $outdir/stats/stats_groupings.csv
#python3 scripts/misc/stats2filter.py $dir/stats/stats.csv $outdir/stats/stats.csv # for data without clusters
#python3 scripts/misc/stats2filter.py $dir/stats/stats_groupings.csv $outdir/stats/stats_groupings.csv # for data without clusters
#cp $dir/stats/stats_agreement.csv $outdir/stats/stats_agreement.csv

# Copy and filter annotators
python3 scripts/misc/stats2filter.py $dir/annotators.csv $outdir/annotators.csv

# Put readme manually to $dir/README.html, from there it will be copied
if [ -f "$dir/README.html" ]
then
    cp $dir/README.html $outdir/README.html
fi

#cp $dir/README.md $outdir/README.md # only for special data

# Copy guidelines if existent, to include the guidelines used for annotation is recommended
if [ -d "$dir/guidelines" ]
then
    cp -r $dir/guidelines $outdir/guidelines
fi

# Copy miscellaneous data
if [ -d "$dir/misc" ]
then
    cp -r $dir/misc $outdir/misc
fi

# Package data
mkdir $dir/$(basename "$dir")
cp -r $dir/release/* $dir/$(basename "$dir")/
ls $dir/$(basename "$dir")
cd $dir/
zip -r $(basename "$dir").zip $(basename "$dir")
cd ../..

# Remove intermediate data
rm -r $outdir
rm -r $dir/$(basename "$dir")/

# Publish online, see e.g. here: https://www.ims.uni-stuttgart.de/data/wugs
