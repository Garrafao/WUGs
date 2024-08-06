
echo $(tput bold)$BASH_SOURCE$(tput sgr0)
scriptsdir=${0%/*}

#indir1=data/dwug_de_3.0.0_unfinished/source/data_round_1-5/dwug_de_2.3.0
#indir1=data/dwug_de_3.0.0_unfinished/source/data_round_1-5_6uses
#indir1=data/dwug_en_3.0.0_unfinished/source/data_round_1-5/dwug_en_2.0.1
#indir1=data/dwug_en_3.0.0_unfinished/source/data_round_1-5_6uses
#indir1=data/dwug_sv_3.0.0_unfinished/source/data_round_1-5/dwug_sv_2.0.1
#indir1=data/dwug_sv_3.0.0_unfinished/source/data_round_1-5_6uses
#indir1=data/dwug_sv_3.0.0_unfinished/source/data_round_1-5_6uses_uses2
#indir2=data/dwug_de_3.0.0_unfinished/source/data_round_6/dwug_de_uses
#indir1=data/discowug_2.0.0_unfinished/source/data_round_1/discowug_1.1.1
indir1=data/dwug_sv_resampled_1.0.0_unfinished/source/dwug_sv_resampled
#indir2=data/dwug_de_3.0.0_unfinished/source/data_round_6/dwug_de_unc
#indir2=data/dwug_en_3.0.0_unfinished/source/data_round_6/dwug_en_uses
#indir2=data/dwug_en_3.0.0_unfinished/source/data_round_6/dwug_en_unc
#indir2=data/dwug_sv_3.0.0_unfinished/source/data_round_6/dwug_sv_uses
#indir2=data/dwug_sv_3.0.0_unfinished/source/data_round_6/dwug_sv_uses2
#indir2=data/dwug_sv_3.0.0_unfinished/source/data_round_6/dwug_sv_unc
#indir2=data/discowug_2.0.0_unfinished/source/data_round_2/discowug_unc
indir2=data/dwug_sv_resampled_1.0.0_unfinished/source/dwug_sv_resampled2
#datadir1=$indir1/data
#datadir1=$indir1/data_normalized
datadir1=$indir1/data_anonymized
datadir2=$indir2/data_anonymized
#outdir=data/dwug_de_3.0.0_unfinished/source/data_round_1-5_6uses/data
#outdir=data/dwug_de_3.0.0_unfinished/source/data_round_1-5_6uses_unc/data
#outdir=data/dwug_en_3.0.0_unfinished/source/data_round_1-5_6uses/data
#outdir=data/dwug_en_3.0.0_unfinished/source/data_round_1-5_6uses_unc/data
#outdir=data/dwug_sv_3.0.0_unfinished/source/data_round_1-5_6uses/data
#outdir=data/dwug_sv_3.0.0_unfinished/source/data_round_1-5_6uses_uses2/data
#outdir=data/dwug_sv_3.0.0_unfinished/source/data_round_1-5_6uses_uses2_unc/data
#outdir=data/discowug_2.0.0_unfinished/source/data_round_1-2_unc/data
outdir=data/dwug_sv_resampled_1.0.0_unfinished/source/dwug_sv_resampled_resampled2
mkdir -p $outdir
#annotators=data/dwug_de_3.0.0_unfinished/source/annotators.csv
#annotators=data/dwug_en_3.0.0_unfinished/source/annotators.csv
#annotators=data/dwug_sv_3.0.0_unfinished/source/annotators.csv
#annotators=data/discowug_2.0.0_unfinished/source/annotators.csv
annotators=data/dwug_sv_resampled_1.0.0_unfinished/source/annotators.csv
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
    python3 $scriptsdir/data2concatenate.py $datadir1/$(basename "$word")/judgments.csv $datadir2/$(basename "$word")/judgments.csv $outdir/$(basename "$word")/judgments.csv 1 2
done
