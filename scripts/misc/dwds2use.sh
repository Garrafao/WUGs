
echo $(tput bold)$BASH_SOURCE$(tput sgr0)
scriptsdir=${0%/*}

inputfile=data/dwds/dwds_export_2024-02-15_10-24-25.csv
outputfile=data/dwds/plattenkritik_uses.csv
python3 $scriptsdir/dwds2use.py $inputfile $outputfile
