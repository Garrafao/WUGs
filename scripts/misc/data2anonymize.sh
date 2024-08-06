
echo $(tput bold)$BASH_SOURCE$(tput sgr0)
scriptsdir=${0%/*}

#indir=data/dwug_de_3.0.0_unfinished/source/data_round_6/dwug_de_uses
#indir=data/dwug_de_3.0.0_unfinished/source/data_round_6/dwug_de_unc
#indir=data/dwug_en_3.0.0_unfinished/source/data_round_1-5/dwug_en_2.0.1
#indir=data/dwug_en_3.0.0_unfinished/source/data_round_6/dwug_en_uses
#indir=data/dwug_en_3.0.0_unfinished/source/data_round_6/dwug_en_unc
#indir=data/dwug_sv_3.0.0_unfinished/source/data_round_6/dwug_sv_uses
#indir=data/dwug_sv_3.0.0_unfinished/source/data_round_6/dwug_sv_uses2
#indir=data/dwug_sv_3.0.0_unfinished/source/data_round_6/dwug_sv_unc
#indir=data/discowug_2.0.0_unfinished/source/data_round_1/discowug_1.1.1
#indir=data/discowug_2.0.0_unfinished/source/data_round_2/discowug_unc
#indir=data/dwug_de_resampled_1.0.0_unfinished/source/dwug_de_resampled
#indir=data/dwug_en_resampled_1.0.0_unfinished/source/dwug_en_resampled
#indir=data/dwug_sv_resampled_1.0.0_unfinished/source/dwug_sv_resampled
indir=data/dwug_sv_resampled_1.0.0_unfinished/source/dwug_sv_resampled2
#datadir=$indir/data
datadir=$indir/data_normalized
outdir=$indir/data_anonymized
#annotators=data/dwug_de_3.0.0_unfinished/source/annotators.csv
#annotators=data/dwug_en_3.0.0_unfinished/source/annotators.csv
#annotators=data/dwug_sv_3.0.0_unfinished/source/annotators.csv
#annotators=data/discowug_2.0.0_unfinished/source/annotators.csv
#annotators=data/dwug_de_resampled_1.0.0_unfinished/source/annotators.csv
#annotators=data/dwug_en_resampled_1.0.0_unfinished/source/annotators.csv
annotators=data/dwug_sv_resampled_1.0.0_unfinished/source/annotators.csv
rm -rf $outdir
cp -r $datadir/ $outdir/ # this will copy weird umlauts in filenames
words=($datadir/*)
for word in "${words[@]}"
do	
    echo $word
    python3 $scriptsdir/data2anonymize.py $word/judgments.csv $outdir $(basename "$word") $annotators
done
