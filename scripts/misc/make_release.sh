 # Define input folder
dir=test_uug

# Remove previous data from release folder
outdir=$dir/release
rm -r $outdir

# Make release folder and subfolders
mkdir -p $outdir
mkdir -p $outdir/graphs
mkdir -p $outdir/stats
mkdir -p $outdir/plots
mkdir -p $outdir/clusters

# Copy data, graphs, plots and clusters
cp -r $dir/data $outdir/data
cp -r $dir/graphs $outdir/graphs/opt
cp -r $dir/plots/interactive/full/colorful $outdir/plots/opt
cp -r $dir/clusters $outdir/clusters/opt

# Copy and filter stats
mkdir -p $outdir/stats/opt
python3 scripts/misc/stats2filter.py $dir/stats/stats.csv $outdir/stats/opt/stats.csv
python3 scripts/misc/stats2filter.py $dir/stats/stats_groupings.csv $outdir/stats/opt/stats_groupings.csv
cp $dir/stats/stats_agreement.csv $outdir/stats/stats_agreement.csv

# Copy and filter annotators
python3 scripts/misc/stats2filter.py $dir/annotators.csv $outdir/annotators.csv

# Put readme manually to $dir/README.html, from there it will be copied
if [ -f "$dir/README.html" ]
then
    cp $dir/README.html $outdir/README.html
fi

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
