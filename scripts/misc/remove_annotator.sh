
echo $(tput bold)$BASH_SOURCE$(tput sgr0)
scriptsdir=${0%/*}

indir=data/dwug_es_4.0.1
datadir=$indir/data
words=($datadir/*)
outdir=$indir/data_cleaned
annotator=gecsa

for word in "${words[@]}"
do
    echo $word
    mkdir -p $outdir/$(basename "$word")
    cp $word/uses.csv $outdir/$(basename "$word")/uses.csv
    python3 $scriptsdir/remove_annotator.py $word/judgments.csv $outdir/$(basename "$word")/judgments.csv $annotator
done
