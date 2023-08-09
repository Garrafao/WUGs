
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

datadir=data/dwug_de_sense_1.0.0_unfinished/data
folders=($datadir/*)

for folder in "${folders[@]}"
do
    echo $folder
    python3 scripts/misc/sense2identifier.py $folder/senses.csv $folder/judgments_senses.csv
done
