
echo $(tput bold)$BASH_SOURCE$(tput sgr0)
scriptsdir=${0%/*}

#dir=data/test_dwug_de
#dir=data/dwug_en
#dir=data/dwug_de
#dir=data/dwug_sv
#dir=data/discowug
#dir=data/refwug
#dir=data/durel
#dir=data/surel
#dir=data/diawug
#dir=data/usim
#dir=data/dups
#dir=data/dwug_la
dir=data/normalize_test

#dataset=dwug_en
#dataset=dwug_de
dataset=dwug_sv
#dataset=discowug
#dataset=usim
#dataset=durel
#dataset=surel
#dataset=dups
#dataset=dwug_la
usedir=$dir/data
words=($usedir/*)
outdir=$dir/use_data/normalize
for word in "${words[@]}"
do	
    echo $word
    mkdir -p $outdir/$(basename "$word")
    python3 $scriptsdir/use2normalize.py $word/uses.csv $dataset $outdir/$(basename "$word")/uses.csv
done
