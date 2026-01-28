
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

dir=data/JaSemChange

datadir=$dir/data
datadirsource=$dir/source
words=($datadirsource/shc/*)
for word in "${words[@]}"
do
    echo $word
    mkdir -p $datadir/$(basename "$word")
    python3 scripts/misc/jasemchange2data.py $word $datadirsource/chj/$(basename "$word") $datadir/$(basename "$word") $(basename "$word")
done
