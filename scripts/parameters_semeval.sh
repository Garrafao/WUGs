map_identifiers=true
annotators=$dir/annotators.csv
excluded=$dir/annotators_excluded.csv
modus=full
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
lowerrangemin=2
lowerrangemax=2
upperrangemin=5
upperrangemax=5
lowerprob=0.0
upperprob=1.0
# system variables
echo timestamp && date +%F_%T
