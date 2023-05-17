
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

inputdir=data/testwug_en_2.0.0/data
outputdir=data/testwug_en_2.0.0/data
files=($inputdir/*/judgments.csv)
for file in "${files[@]}"
do
    echo $file
    echo $(basename $(dirname ${file}))
    python3 scripts/misc/judgments2instances.py $file $outputdir/$(basename $(dirname ${file}))/instances.csv
done

