
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

#datadir=$dir/data
#files=($datadir/*)
files=(durel_system/upload_formats/test_uug/uses/demá.csv)
for file in "${files[@]}"
do
    echo $file
    python3 scripts/misc/use2target.py $file
done
