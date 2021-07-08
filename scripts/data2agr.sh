
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

data=$dir/data_joint/data_joint
outdir=$dir/stats
mkdir -p $outdir
python3 $scriptsdir/data2agr.py $data $(basename "$data") $min $max $annotators $outdir/stats_agreement.csv
