
echo $(tput bold)$BASH_SOURCE$(tput sgr0)
scriptsdir=${0%/*}

dir=.
mkdir -p $dir/source
wget http://www.dianamccarthy.co.uk/downloads/WordMeaningAnno2012/cl-meaningincontext.tgz -nc -P $dir/source/
unzip $dir/source/cl-meaningincontext.tgz -d $dir/source/

datadir=$dir/data
mkdir -p $datadir
python3 $dir/usim2data.py $dir/source/Data/lexsub_wcdata.xml $dir/source/Markup/UsageSimilarity/usim2ratings.csv $datadir

dataset=usim
usedir=$dir/data
words=($usedir/*)
outdir=$dir/use_data/normalize
for word in "${words[@]}"
do	
    echo $word
    mkdir -p $outdir/$(basename "$word")
    python3 $dir/use2normalize.py $word/uses.csv $dataset $outdir/$(basename "$word")/uses.csv
done

datadir=$dir/use_data/normalize
mkdir -p $datadir
usedir=$dir/data
words=($usedir/*)
outdir=$dir/data
for word in "${words[@]}"
do	
    echo $word
    mkdir -p $outdir/$(basename "$word")
    python3 $dir/data2use.py $word/uses.csv $datadir $outdir/$(basename "$word")/uses.csv
done
