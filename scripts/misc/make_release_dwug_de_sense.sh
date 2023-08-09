 # Define input folder
dir=data/dwug_de_sense

# Make release folder and subfolders
outdir=$dir/release
mkdir -p $outdir

# Copy data, graphs, plots and clusters
cp -r $dir/data $outdir/data
cp -r $dir/labels $outdir/labels
cp -r $dir/plots $outdir/plots
cp -r $dir/stats $outdir/stats

# Copy annotators
cp $dir/annotators.csv $outdir/annotators.csv

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

# Package data
mkdir $dir/$(basename "$dir")
cp -r $dir/release/* $dir/$(basename "$dir")/
ls $dir/$(basename "$dir")
cd $dir/
zip -r $(basename "$dir").zip $(basename "$dir")
cd ../..

# Publish online, see e.g. here: https://www.ims.uni-stuttgart.de/data/wugs

