echo $(tput bold)$BASH_SOURCE$(tput sgr0)
scriptsdir=${0%/*}
dir=.
mkdir -p $dir/source
wget https://www.clarin.si/repository/xmlui/handle/11356/1308/allzip -nc -P $dir/source/
mv $dir/source/allzip $dir/source/allzip.zip
tar xvzf $dir/source/allzip.zip -C $dir/source/

for lang in 'en' 'fi' 'hr'
for lang in 'en'
do
  datadir=$dir/wugformat/$lang
  mkdir -p $datadir
  python3 $dir/semeval2wug.py $dir/source/cosimlex_$lang.csv $datadir $lang
done
rm -r $dir/source
