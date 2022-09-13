echo $(tput bold)$BASH_SOURCE$(tput sgr0)
scriptsdir=${0%/*}
dir=.
mkdir -p $dir/source
wget https://codalab.lisn.upsaclay.fr/my/datasets/download/3e22f138-ca00-4b10-a0fd-2e914892200d -nc -P $dir/source/
mv $dir/source/3e22f138-ca00-4b10-a0fd-2e914892200d $dir/source/starting-kit.zip
tar xvzf $dir/source/starting-kit.zip -C $dir/source/


datadir=$dir/wugdata/
mkdir -p $datadir
python3 $dir/evonlp2wug-test.py $dir/source/TempoWiC_Starting_Kit/data/test-codalab-10k.data.jl $datadir 'test'


rm -r $dir/source
