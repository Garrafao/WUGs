# test pipeline
dir=test_uug
bash -e scripts/run_uug.sh
rm -rf $dir/data_joint
rm -rf $dir/graphs
rm -rf $dir/graphs_full
rm -rf $dir/graphs1
rm -rf $dir/clusters
rm -rf $dir/stats
rm -rf $dir/plots
rm -f $dir/annotators.csv
rm -rf scripts/__pycache__
dir=test_usg
bash -e scripts/run_usg.sh
rm -rf $dir/data_joint
rm -rf $dir/graphs
rm -rf $dir/graphs_full
rm -rf $dir/graphs1
rm -rf $dir/clusters
rm -rf $dir/stats
rm -rf $dir/plots
rm -f $dir/annotators.csv
rm -rf scripts/__pycache__

# test system pipeline
dir=test_uug
bash -e scripts/run_system.sh $dir
rm -rf $dir/plots
#exit 0

# test pipeline 2
dir=test_uug
bash -e scripts/run_uug2.sh
rm -rf $dir/data_joint
rm -rf $dir/graphs
rm -rf $dir/graphs_full
rm -rf $dir/graphs1
rm -rf $dir/clusters
rm -rf $dir/stats
rm -rf $dir/plots
rm -f $dir/annotators.csv
rm -rf scripts/__pycache__

# test system pipeline 2
dir=test_uug
#algorithms=(correlation chinese louvain)
#positions=(spring sfdp spectral)
algorithms=(correlation)
positions=(spring)
for algorithm in "${algorithms[@]}"
do
    for position in "${positions[@]}"
    do
	bash -e scripts/run_system2.sh $dir $algorithm $position
    done
done
rm -rf $dir/plots
