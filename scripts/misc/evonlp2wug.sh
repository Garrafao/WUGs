echo $(tput bold)$BASH_SOURCE$(tput sgr0)
scriptsdir=${0%/*}
dir=.
mkdir -p $dir/source
wget https://codalab.lisn.upsaclay.fr/my/datasets/download/3e22f138-ca00-4b10-a0fd-2e914892200d -nc -P $dir/source/
mv $dir/source/3e22f138-ca00-4b10-a0fd-2e914892200d $dir/source/starting-kit.zip
unzip $dir/source/starting-kit.zip -d $dir/source/

for data in 'train' 'trial' 'validation'
do
  if [[ "$data" = "trial" ]]
  then
     label='gold'
  else
     label='labels'
  fi
  datadir=$dir/wugdata/
  mkdir -p $datadir
  python3 $dir/evonlp2wug.py $dir/source/TempoWiC_Starting_Kit/data/$data.data.jl $dir/source/TempoWiC_Starting_Kit/data/$data.$label.tsv $datadir $data
done

rm -r $dir/source
