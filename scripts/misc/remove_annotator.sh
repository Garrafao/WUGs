
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

datadir=$dir/data
words=($datadir/*)

for word in "${words[@]}"
do
    echo $word
    python3 $scriptsdir/misc/judgments2header.py $word/judgments.csv $word/judgments.csv
done
