
echo $(tput bold)$BASH_SOURCE$(tput sgr0)

data=$dir/data_joint/data_joint
python3 $scriptsdir/data2annotators.py $data $isanonymize $annotators
