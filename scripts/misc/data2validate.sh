
echo $(tput bold)$BASH_SOURCE$(tput sgr0)
scriptsdir=${0%/*}

#indir=data/dwug_de_3.0.0_unfinished
#indir=data/dwug_en_3.0.0_unfinished
#indir=data/dwug_sv_3.0.0_unfinished
#indir=data/discowug_2.0.0_unfinished
#indir=data/dwug_de_resampled_1.0.0_unfinished
#indir=data/dwug_en_resampled_1.0.0_unfinished
indir=data/dwug_sv_resampled_1.0.0_unfinished
datadir=$indir/data_uncleaned
#datadir=$indir/data
words=($datadir/*)
outdir=$indir/data
#outdir=$indir/data_cleaned_cleaned
annotators=$indir/annotators.csv
for word in "${words[@]}"
do	
    echo $word
    mkdir -p $outdir/$(basename "$word")
    python3 $scriptsdir/data2validate.py $word/uses.csv $word/judgments.csv $outdir/$(basename "$word")/uses.csv $outdir/$(basename "$word")/judgments.csv $annotators
    #python3 $scriptsdir/data2validate.py $word/uses.csv $word/judgments.csv None None $annotators
done
