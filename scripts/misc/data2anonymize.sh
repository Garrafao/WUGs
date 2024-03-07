
echo $(tput bold)$BASH_SOURCE$(tput sgr0)
scriptsdir=${0%/*}

indir=data/dwug_de_3.0.0_unfinished/source/data_round_6/dwug_de_unc
#indir=data/dwug_de_3.0.0_unfinished/source/data_round_6/dwug_de_uses
datadir=$indir/data
outdir=$indir/data_anonymized
annotators=data/dwug_de_3.0.0_unfinished/source/annotators.csv
rm -rf $outdir
cp -r $datadir/ $outdir/
words=($outdir/*)
for word in "${words[@]}"
do	
    echo $word
    python3 $scriptsdir/data2anonymize.py $word/judgments.csv $outdir $(basename "$word") $annotators
done
