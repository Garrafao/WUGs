import sys
import shutil
import unicodedata
import os

[_, uses, judgments, outfolder, lemma] = sys.argv

lemma = unicodedata.normalize('NFC', lemma)

if not os.path.isdir(outfolder + '/' + lemma):
    os.makedirs(outfolder + '/' + lemma)
shutil.copyfile(uses, outfolder + '/' + lemma + '/' + 'uses.csv')
shutil.copyfile(judgments, outfolder + '/' + lemma + '/' + 'judgments.csv')
