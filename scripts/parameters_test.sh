map_identifiers=true
annotators=$dir/annotators.csv
excluded=$dir/annotators_excluded.csv
modus=test
graphtype=uug
isanonymize=True
# clustering
iters=1
min=1
threshold=2.5
max=4
# plotting
position=spring
colors=(colorful)
periods=(full)
modes=(full)
styles=(interactive)
edgestyles=(weight)
thresholdplot=2.5
# change scores
lowerrangemin=1
lowerrangemax=3
upperrangemin=3
upperrangemax=5
lowerprob=0.01
upperprob=0.1
# system variables
echo timestamp && date +%F_%T
