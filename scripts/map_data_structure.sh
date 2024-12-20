
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

datadir=$dir/data
uses=($datadir/*_uses.csv)
outdir=$dir/data
mkdir -p $outdir

for use in "${uses[@]}"
do
    file=$(basename "$use") 
    echo $file # for testing
    IFS='_' read -ra wordparts <<< "$file" # problematic: assumes word as no _
    word=${wordparts[0]}
    echo $word # for testing
    mkdir -p $outdir/$word
    cp $datadir/$word\_uses.csv $outdir/$word/uses.csv 
    cp $datadir/$word\_instances.csv $outdir/$word/instances.csv 
    cp $datadir/$word\_annotations.csv $outdir/$word/annotations.csv
    rm $datadir/$word\_uses.csv
    rm $datadir/$word\_instances.csv
    rm $datadir/$word\_annotations.csv
done
