# Attention: modifies graphs iteratively, i.e., current run is dependent on previous run. To avoid, run full pipeline and remove graphs from last round.

scriptsdir=${0%/*}

#dataset=dwug_de_test
#dataset=dwug_de_2.3.0
dataset=chiwug_1.0.0

#experiments=experiments
#experiments=experiments1
#experiments=experiments_cluster_clean/experiments2
#experiments=experiments_cluster_clean/experiments3
experiments=experiments_cluster_clean/experiments4
#experiments=experiments_cluster_clean/experiments_test

algorithms=(correlation wsbm chinese)
#algorithms=(wsbm)
thresholds=(0.0 1.8 1.9 2.0 2.1 2.2 2.3 2.4 2.5 2.6 2.7 2.8 2.9 3.0 3.1 3.2)
#thresholds=(0.0)
#ambiguitys=("scale_edges" "remove_nodes" "None")
ambiguitys=("scale_edges" "None")
#ambiguitys=("None")
degrees=("None" "top" "lin" "log")
ismultiple=False # only needed for wsbm, whether each edge has multiple weights (one per annotator)
distributions=("None-None" "discrete-geometric" "discrete-binomial")
#distributions=("real-exponential" "real-normal")
degcorrs=("None" "False" "True")
adjacencys=("None" "False" "True")


modus=full
#modus=test
graphtype=uug
isanonymize=True
map_identifiers=False
iters=5
itersglobal=$iters
min=1
max=4
summarystatistic=median
isnannodes=True # whether to keep nannodes
isnanedges=True # whether to keep nanedges
grouping=full # which grouping to keep, full means to keep all groupings
edgefilter=None # any special filters on edges, currently one of None, conflicts
nonvalue=0.0
isspring=False
colors=(colorful)
periods=(full)
modes=(full)
styles=(interactive)
edgestyles=(weight)
lowerrangemin=1
lowerrangemax=3
upperrangemin=3
upperrangemax=5
lowerprob=0.01
upperprob=0.1

for algorithm in "${algorithms[@]}"
do
    for thr in "${thresholds[@]}"
    do
	if ([ ! $algorithm == correlation ] && [ ! $algorithm == chinese ]) && [ ! $thr == 0.0 ]
	then
	    continue
	fi
	for degree in "${degrees[@]}"
	do
	    if ([ ! $algorithm == chinese ] && [ ! $degree == None ]) || ([ $algorithm == chinese ] && [ $degree == None ])
	    then
		continue
	    fi
	    for amb in "${ambiguitys[@]}"
	    do
		if [ $algorithm == wsbm ] && [ ! $amb == None ] && [ ! $amb == "remove_nodes" ] && [ ! $distribution == "real-normal" ] && [ ! $distribution == "real-exponential" ]
		then
		    continue
		fi
		for distribution in "${distributions[@]}"
		do
		    if ([ ! $algorithm == wsbm ] && [ ! $distribution == "None-None" ]) || ([ $algorithm == wsbm ] && [ $distribution == "None-None" ]) 
		    then
			continue
		    fi
		    for adjacency in "${adjacencys[@]}"
		    do
			if ([ ! $algorithm == wsbm ] && [ ! $adjacency == None ]) || ([ $algorithm == wsbm ] && [ $adjacency == None ]) 
			then
			    continue
			fi
			for degcorr in "${degcorrs[@]}"
			do
			    if ([ ! $algorithm == wsbm ] && [ ! $degcorr == None ]) || ([ $algorithm == wsbm ] && [ $degcorr == None ]) 
			    then
				continue
			    fi
			    
			    
			    IFS='-' read -ra distributionnameparts <<< "$distribution"
			    distributionname=${distributionnameparts[1]}
			    dir=data/$experiments/$algorithm/$dataset\-$thr\-$amb-$degree-$distributionname-$adjacency-$degcorr
			    echo $dir # for testing
				if [ -d "$dir" ]; then
					echo "Directory exists. Skipping…"
					continue
				fi
			    #continue

			    mkdir -p $dir

			    annotators=$dir/annotators.csv
			    excluded=None
			    ambiguity=$amb
			    threshold=$thr

			    degreedl=$degcorr

			    iters=$itersglobal
			    if [ ! $algorithm == correlation ]
			    then
				iters=1
			    fi
			    
			    cp -r data/$dataset/data $dir/
			    source $scriptsdir/data2join.sh
			    source $scriptsdir/data2annotators.sh
			    source $scriptsdir/data2graph.sh
			    source $scriptsdir/graph2cluster2.sh
			    source $scriptsdir/extract_clusters.sh
			    source $scriptsdir/graph2stats.sh
			    
			done
		    done
		done
	    done
	done
    done
done

collapses=(2.0 2.1 2.2 2.3 2.4)
#collapses=(2.0 2.1)

for algorithm in "${algorithms[@]}"
do
    folders=(data/$experiments/$algorithm/$dataset*)
    for collapse in "${collapses[@]}"
    do
	for folder in "${folders[@]}"
	do
	    dir=$folder\-$collapse
	    echo $dir
		#continue

	    rm -rf $dir
	    mkdir -p $dir
	    cp -r $folder/graphs $dir
	    cp  $folder/annotators.csv $dir/annotators.csv
	    
	    annotators=$dir/annotators.csv
	    thr="$(cut -d'-' -f2 <<<"$folder")"
	    threshold=$thr
	    
	    source $scriptsdir/graph2collapse.sh
	    source $scriptsdir/extract_clusters.sh
	    source $scriptsdir/graph2stats.sh
	    
	done
    done
done

: '
for algorithm in "${algorithms[@]}"
do
    folders=(data/$experiments/$algorithm/$dataset*)
	for folder in "${folders[@]}"
	do
	    dir=$folder
	    echo $dir

	    mkdir -p $dir/plots
	    
	    annotators=$dir/annotators.csv
	    thr="$(cut -d'-' -f2 <<<"$folder")"
	    threshold=$thr
	    
	    source $scriptsdir/graph2plot.sh
	    
	done
done
'
exit 0

dir=data/experiments_cluster_clean/cleaning/dwug_de_230/correlation_published # published clusterings
#dir=data/experiments_cluster_clean/cleaning/dwug_de_230/wsbm_dwug_de_2.3.0-0.0-None-None-binomial-False-True # previously introduced model with theoretical motivation
#dir=data/experiments_cluster_clean/cleaning/dwug_de_230/chinese_dwug_de_2.3.0-2.0-scale_edges-top-None-None-None-2.4 # one of the top models in cross-validation

annotators=$dir/annotators.csv
threshold=0.0
# Post-hoc cleaning parameters
isremovenan=True # This should be set to True for most cases
isremovenoise=True # This should be set to True for most cases
collapse=None # None or some threshold
stdedges=999 # choose 999 to remove nothing
stdnodes=999 # choose 999 to remove nothing
degreeremove=1 # choose 0 to remove nothing and 1 to remove isolates
clustersizemin=1 # size below which clusters will be removed, choose 1 to remove nothing
clusterconnectmin=0.0 # size connection percentage below which clusters will be removed, choose 0.0 to remove nothing

diroriginal=$dir

#stdedgess=(0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)
stdedgess=(0.0 0.14433756729740643 0.15713484026367722 0.15713484026367724 0.16666666666666666 0.16666666666666669 0.2721655269759087 0.3142696805273545 0.5)
for stdedges in "${stdedgess[@]}"
do
    # Redefine some variables
    dir=$diroriginal/stdedge_$stdedges
    mkdir -p $dir
    cp -r $diroriginal/graphs $dir/
    source $scriptsdir/graph2clean2.sh 
    source $scriptsdir/extract_clusters.sh
    source $scriptsdir/graph2stats.sh
done

stdedges=999 # choose 999 to remove nothing

#degreeremoves=(0 1 2 3 4 5 6 7 8 9 10 15 20 25 30)
degreeremoves=(0 1 2 3 4 5 6 7 8 9 11 12 13 15 16 17 19 21 26 107)
for degreeremove in "${degreeremoves[@]}"
do
    # Redefine some variables
    dir=$diroriginal/degreeremove_$degreeremove
    mkdir -p $dir
    cp -r $diroriginal/graphs $dir/
    source $scriptsdir/graph2clean2.sh 
    source $scriptsdir/extract_clusters.sh
    source $scriptsdir/graph2stats.sh
done

degreeremove=1 # choose 0 to remove nothing and 1 to remove isolates

#stdnodess=(0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)
stdnodess=(0.0 0.010416666666666668 0.018131211614501635 0.023128679066453134 0.027777777777777776 0.03142696805273544 0.03435259622814437 0.039283710065919304 0.04166666666666667 0.04625735813290627 0.050548833866436715 0.053033738680930344 0.05555555555555556 0.05659640207640626 0.06317105855372249 0.06870519245628873 0.07587858982814524 0.07856742013183862 0.08201782672273343 0.08333333333333334 0.09154060418188527 0.10577873744439341 0.11909966228454526 0.14627739788085845 0.15713484026367724 0.16666666666666669 0.5)
for stdnodes in "${stdnodess[@]}"
do
    # Redefine some variables
    dir=$diroriginal/stdnode_$stdnodes
    mkdir -p $dir
    cp -r $diroriginal/graphs $dir/
    source $scriptsdir/graph2clean2.sh 
    source $scriptsdir/extract_clusters.sh
    source $scriptsdir/graph2stats.sh
done

stdnodes=999 # choose 999 to remove nothing

#collapses=(2.5 2.45 2.4 2.35 2.3 2.25 2.2 2.15 2.1 2.05 2.0 1.95 1.9)
collapses=(1.0 1.072013769363167 1.1245 1.2147672552166933 1.25 1.3527874564459934 1.3934285714285715 1.454803827751196 1.5 1.6143283582089551 1.6666666666666667 1.7226666666666666 1.8 1.8780000000000001 1.9642024965325935 2.0 2.0187737961926095 2.0625 2.125 2.1666666666666665 2.203764705882353 2.25 2.2795643818065345 2.3333333333333335 2.357142857142857 2.383058823529412 2.441268115942029 2.5 3.0)
for collapse in "${collapses[@]}"
do
    # Redefine some variables
    dir=$diroriginal/collapse_$collapse
    mkdir -p $dir
    cp -r $diroriginal/graphs $dir/
    source $scriptsdir/graph2clean2.sh 
    source $scriptsdir/extract_clusters.sh
    source $scriptsdir/graph2stats.sh
done

collapse=None # None or some threshold

#clustersizemins=(1 2 3 4 5 6 7 8 9 10)
clustersizemins=(1 2 3 4 7 9 14 15 24 36 43 55 64 77 90 96 107 128 139 157 165 193 197 200)
for clustersizemin in "${clustersizemins[@]}"
do
    # Redefine some variables
    dir=$diroriginal/clustersizemin_$clustersizemin
    mkdir -p $dir
    cp -r $diroriginal/graphs $dir/
    source $scriptsdir/graph2clean2.sh 
    source $scriptsdir/extract_clusters.sh
    source $scriptsdir/graph2stats.sh
done

clustersizemin=1 # size below which clusters will be removed, choose 1 to remove nothing

#clusterconnectmins=(0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0)
clusterconnectmins=(0.03225806451612903 0.125 0.12903225806451613 0.16344086021505375 0.23064516129032248 0.25 0.2857142857142857 0.3333333333333333 0.375 0.39499999999999996 0.4166666666666667 0.5 0.5714285714285714 0.625 0.6666666666666666 0.6761904761904757 0.75 0.7555555555555552 0.8 0.8333333333333334 0.8476190476190475 0.875 0.9082949308755764 1.0)
for clusterconnectmin in "${clusterconnectmins[@]}"
do
    # Redefine some variables
    dir=$diroriginal/clusterconnectmin_$clusterconnectmin
    mkdir -p $dir
    cp -r $diroriginal/graphs $dir/
    source $scriptsdir/graph2clean2.sh 
    source $scriptsdir/extract_clusters.sh
    source $scriptsdir/graph2stats.sh
done

clusterconnectmin=0.0 # size connection percentage below which clusters will be removed, choose 0.0 to remove nothing
