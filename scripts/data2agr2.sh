
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

data=$dir/data_joint/data_joint
outdir=$dir/stats
mkdir -p $outdir
python3 $scriptsdir/data2agr2.py $data $modus $min $max $scale $nonvalue $annotators $excluded $outdir/stats_agreement.csv
