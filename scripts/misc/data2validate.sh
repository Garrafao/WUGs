
echo $(tput bold)$BASH_SOURCE$(tput sgr0)
scriptsdir=${0%/*}

indir=data/dwug_de_3.0.0_unfinished/
outdir=$indir/data_cleaned
python $scriptsdir/data2validate.py $indir
