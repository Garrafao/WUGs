
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

datadir=$dir/data
words=($datadir/*)
isheader=True
outdir=$dir/data_joint
mkdir -p $outdir

for word in "${words[@]}"
do
    senses=None
    if [ $graphtype == "usg" ]
    then
	senses=$word/senses.csv
    fi
    echo $word
    python3 $scriptsdir/data2join.py $word/uses.csv $word/annotations.csv $senses $isheader $outdir/data_joint
    isheader=False
done
