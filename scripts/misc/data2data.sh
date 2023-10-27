
echo $(tput bold)$BASH_SOURCE$(tput sgr0)
scriptsdir=${0%/*}

indir=data/ChiSemShift_1.0.0_unpublished
datadir=$indir/data_original
words=($datadir/*)
outdir=$indir/data
annotators=$indir/annotators.csv
for word in "${words[@]}"
do	
    echo $word
    mkdir -p $outdir/$(basename "$word")
    python3 $scriptsdir/data2data.py $word/uses.csv $word/judgments.csv $outdir/$(basename "$word")/uses.csv $outdir/$(basename "$word")/judgments.csv $annotators
done
