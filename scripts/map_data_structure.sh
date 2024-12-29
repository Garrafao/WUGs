#!/bin/bash
echo $(tput bold)$BASH_SOURCE$(tput sgr0)
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
datadir=$dir/data
uses=($datadir/*_uses.csv)
outdir=$dir/data
mkdir -p $outdir

for use in "${uses[@]}"
do
    file=$(basename "$use") 
    echo $file # for testing
    word=${file%_*}
    echo $word # for testing
    mkdir -p $outdir/$word
    cp $datadir/$word\_uses.csv $outdir/$word/uses.csv 
    cp $datadir/$word\_instances.csv $outdir/$word/instances.csv 
    cp $datadir/$word\_judgments.csv $outdir/$word/judgments.csv
    rm $datadir/$word\_uses.csv
    rm $datadir/$word\_instances.csv
    rm $datadir/$word\_judgments.csv
done
