
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

#dir=data/test_dwug_de
#dir=data/dwug_en
#dir=data/dwug_de
#dir=data/dwug_sv
#dir=data/discowug
#dir=data/refwug
dir=data/durel
#dir=data/surel
#dir=data/diawug
#dir=data/usim
#dir=data/dups

#datadir=$dir/use_data/normalize
#datadir=$dir/use_data/lemma_pos
datadir=$dir/use_data/spelling
usedir=$dir/data
words=($usedir/*)
outdir=$dir/data
for word in "${words[@]}"
do	
    echo $word
    mkdir -p $outdir/$(basename "$word")
    python3 scripts/misc/data2use.py $word/uses.csv $datadir $outdir/$(basename "$word")/uses.csv
done
