
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

input=durel_system/upload_formats/test_uug/judgments/Vorwort.csv
output=durel_system/upload_formats/test_uug/instances/Vorwort.csv

python3 scripts/misc/judgments2instances.py $input $output
