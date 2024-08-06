
echo $(tput bold)$BASH_SOURCE$(tput sgr0)
scriptsdir=${0%/*}

#indir=data/discowug_2.0.0_unfinished/source/data_round_1/discowug_1.1.1
#indir=data/dwug_de_resampled_1.0.0_unfinished/source/dwug_de_resampled
#indir=data/dwug_en_resampled_1.0.0_unfinished/source/dwug_en_resampled
#indir=data/dwug_sv_resampled_1.0.0_unfinished/source/dwug_sv_resampled
indir=data/dwug_sv_resampled_1.0.0_unfinished/source/dwug_sv_resampled2
datadir=$indir/data
outdir=$indir/data_normalized
rm -rf $outdir
words=($datadir/*)
for word in "${words[@]}"
do	
    echo $word
    python3 $scriptsdir/data2normalizepath.py $word/uses.csv $word/judgments.csv $outdir $(basename "$word")
done
