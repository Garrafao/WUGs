# test pipeline

bash -e scripts/run_uug.sh
dir=test_uug
rm -rf $dir/data_joint
rm -rf $dir/graphs
rm -rf $dir/graphs_full
rm -rf $dir/graphs1
rm -rf $dir/clusters
rm -rf $dir/stats
rm -rf $dir/plots
rm -f $dir/annotators.csv
rm -rf scripts/__pycache__
bash -e scripts/run_usg.sh
dir=test_usg
rm -rf $dir/data_joint
rm -rf $dir/graphs
rm -rf $dir/graphs_full
rm -rf $dir/graphs1
rm -rf $dir/clusters
rm -rf $dir/stats
rm -rf $dir/plots
rm -f $dir/annotators.csv
rm -rf scripts/__pycache__

# test system pipeline for word with non-complete judgment domain (no judgments of 1)
#dir=test_uug1
#bash -e scripts/run_system.sh $dir
#rm -rf $dir/plots

# test pipeline 2
bash -e scripts/run_uug2.sh
dir=test_uug
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
dirs=(test_uug_system)
#algorithms=(correlation chinese louvain)
#positions=(spring sfdp spectral)
algorithms=(correlation)
thresholds=(2.5 2.0)
positions=(spring)
for dir in "${dirs[@]}"
do
  for algorithm in "${algorithms[@]}"
  do
	  for threshold in "${thresholds[@]}"
	  do
	    for position in "${positions[@]}"
	    do
		    cp -r $dir/data_original/ $dir/data/
        bash -e scripts/DURel_tool_create_graph_from_data.sh $dir False median 0.0 weight $threshold $position full
        bash -e scripts/DURel_tool_filter_existing_graph.sh $dir all full None None None True True weight $threshold $position full
        bash -e scripts/DURel_tool_cluster_filtered_graph.sh $dir True None $algorithm None False discrete-binomial False False False 1 system weight $threshold $position full median 0.0 $threshold
        rm -rf $dir/data_joint
        rm -rf $dir/graphs
        rm -rf $dir/graphs_full
        rm -rf $dir/graphs1
        rm -rf $dir/clusters
        rm -rf $dir/stats
        rm -rf $dir/plots
        rm -rf $dir/data
        rm -f $dir/annotators.csv
        rm -rf scripts/__pycache__
	    done
	  done
  done
done
