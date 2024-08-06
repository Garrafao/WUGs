
echo $(tput bold)$BASH_SOURCE$(tput sgr0)
scriptsdir=${0%/*}

indir=data/dwug_de_resampled_1.0.0_unfinished/source/dwug_de_resampled/
datadir=$indir/data_normalized
words=($datadir/*)
outdir=$indir/data_normalized_uses
datadir2=data/dwug_de_3.0.0_unfinished/data
cp -r $datadir/ $outdir/ # this will copy weird umlauts in filenames
for word in "${words[@]}"
do	
    echo $word
    mkdir -p $outdir/$(basename "$word")
    python3 $scriptsdir/copy_uses.py $word/uses.csv $datadir2/$(basename "$word")/uses.csv $outdir/$(basename "$word")/uses.csv
done
