
echo $(tput bold)$BASH_SOURCE$(tput sgr0)
scriptsdir=${0%/*}

#indir1=data/dwug_de_3.0.0_unfinished/source/data_round_1-5/dwug_de_2.3.0
indir1=data/dwug_de_3.0.0_unfinished/source/data_round_1-5_6uses
#indir2=data/dwug_de_3.0.0_unfinished/source/data_round_6/dwug_de_uses
indir2=data/dwug_de_3.0.0_unfinished/source/data_round_6/dwug_de_unc
datadir1=$indir1/data
datadir2=$indir2/data_anonymized
#outdir=data/dwug_de_3.0.0_unfinished/source/data_round_1-5_6uses/data
outdir=data/dwug_de_3.0.0_unfinished/source/data_round_1-5_6uses_unc/data
mkdir -p $outdir
annotators=data/dwug_de_3.0.0_unfinished/source/annotators.csv
rm -rf $outdir
cp -r $datadir1/ $outdir/
words=($outdir/*)
for word in "${words[@]}"
do	
    if [ ! -f $datadir2/$(basename "$word")/judgments.csv ]; then
	echo "...Skipping" $(basename "$word")
	continue
    fi
    echo $(basename "$word")
    python3 $scriptsdir/data2concatenate.py $datadir1/$(basename "$word")/judgments.csv $datadir2/$(basename "$word")/judgments.csv $outdir/$(basename "$word")/judgments.csv 6
done
