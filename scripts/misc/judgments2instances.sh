
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

input=durel_system/upload_formats/test_uug/judgments/Aufkommen.csv
output=durel_system/upload_formats/test_uug/instances/Aufkommen.csv

python3 scripts/misc/judgments2instances.py $input $output
