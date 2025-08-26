
echo $(tput bold)$BASH_SOURCE$(tput sgr0)
scriptsdir=${0%/*}

#datadir=data/lexicographer_project/lex_sv_1_sense_random_281/data_source
#datadir=data/lexicographer_project/Euralex_sv_experiment_1_v2.02/xldurel/data_source
datadir=data/lexicographer_project/DURel_data_filtered_fromEmma/data_download
files=($datadir/*)
outdir=$datadir\_data
for file in "${files[@]}"
do	
    echo $file
    word="$(cut -d'_' -f1 <<<"$(basename "$file")")"
    type="$(cut -d'_' -f2 <<<"$(basename "$file")")"
    
    mkdir -p $outdir/$word
    if [ $type == "annotations.csv" ]
    then
	type=judgments.csv
    fi
    cp $file $outdir/$word/$type
done
