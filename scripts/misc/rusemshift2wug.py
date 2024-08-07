
import requests
import pandas as pd
import io
import numpy as np
import os
import warnings

#!pip install fuzzywuzzy
import fuzzywuzzy
from fuzzywuzzy import fuzz
import re

warnings.filterwarnings("ignore")

URL = "https://raw.githubusercontent.com/juliarodina/RuSemShift/master/rusemshift_2/raw_annotations.tsv"
download = requests.get(URL).content
df = pd.read_csv(io.StringIO(download.decode('utf-8')),sep = '\t')

def remove_inverted_comma(sentence):
    if(sentence.count('"')%2!=0) and sentence[0] == '"' and sentence[-1]!='"':
        return sentence[1:]
    return sentence

df["sent1"] = df["sent1"].apply(remove_inverted_comma)
df["sent2"] = df["sent2"].apply(remove_inverted_comma)

df.loc[df["group"] == "EARLIER", "group1"] = "EARLIER"
df.loc[df["group"] == "EARLIER", "group2"] = "EARLIER"

df.loc[df["group"] == "LATER", "group1"] = "LATER"
df.loc[df["group"] == "LATER", "group2"] = "LATER"

df.loc[df["group"] == "COMPARE", "group1"] = "EARLIER"
df.loc[df["group"] == "COMPARE", "group2"] = "LATER"

df_dash = df[['word', 'sent1', 'sent2', "group1", "group2"]]

df1 = df_dash[['word', 'sent1', 'group1']]
df1.columns =  ['word', 'sent', 'group']
df1["index"] = df1.groupby("word").cumcount()*2

df2 =  df_dash[['word', 'sent2', 'group2']]
df2.columns =  ['word', 'sent', 'group']
df2["index"] = df2.groupby("word").cumcount()*2+1

df_final = pd.concat([df1, df2])
df_final = df_final.sort_values(by = ['word', 'index'], ascending = [True, True])

df_final["identifier"] = df_final["word"]+"-"+df_final["index"].astype(str)

df_odd = df_final[1::2]
df_odd.columns = ["word2", "sent2", 'group2', "index2", "identifier2"]
df_even = df_final[::2]
df_even.columns = ["word1", "sent1", "group1", "index1", "identifier1"]
df_final = pd.concat([df_even, df_odd], axis=1)

df_final = df_final[["word2", "sent2", "identifier2", 'group2', "sent1", "identifier1", 'group1', 'index1', 'index2']]
df_final_next_stage = df_final.rename(columns={"word2":"lemma"})

df_final = df_final_next_stage

df_second_dash = df[["annotator1","annotator2","annotator3","annotator4","annotator5"]]

df_final = pd.concat([df_final, df_second_dash], axis=1)

df_final["judgment"] = df_final[['annotator1', 'annotator2', 'annotator3', 'annotator4', 'annotator5']].values.tolist()

df_final = df_final[['lemma', 'identifier2', 'identifier1', 'judgment']]

df_final = df_final.explode("judgment")

df_final.reset_index(drop=True, inplace=True)

annotators = ["annotator1", "annotator2", "annotator3", "annotator4", "annotator5"]

df_final["annotator"] = df_final.index.map(lambda idx: annotators[idx%len(annotators)])
df_final["comment"] = np.nan
df_final = df_final[["identifier1", "identifier2", "annotator", "judgment", "comment", "lemma"]]
df_final.fillna('', inplace=True)
for i in list(df_final["lemma"].value_counts().index):
    df_temp = df_final[df_final["lemma"]==i]
    numpy_df = df_temp.to_numpy()
    header = list(df_temp.columns)
    numpy_df = np.vstack([header, numpy_df])
    if not os.path.exists(i):
        os.mkdir(i)
    np.savetxt(i+"/judgments.csv", numpy_df,fmt='%s', delimiter='\t')

URL = "https://raw.githubusercontent.com/juliarodina/RuSemShift/master/rusemshift_2/binary.csv"

download = requests.get(URL).content

df_binary = pd.read_csv(io.StringIO(download.decode('utf-8')))

df_binary["pos"] = df_binary["WORD"].apply(lambda x: x.split("_")[1])
df_binary["WORD"] = df_binary["WORD"].apply(lambda x: x.split("_")[0])
df_binary.columns = ["word", "ground_truth", "pos"]

df_binary.drop("ground_truth", axis=1, inplace=True)
df1 = df_final_next_stage[['lemma', 'sent1', 'group1', 'identifier1', 'index1']]
df1.columns =  ['word', 'sent', 'group', 'identifier', 'index']
df2 = df_final_next_stage[['lemma', 'sent2', 'group2', 'identifier2', 'index2']]
df2.columns =  ['word', 'sent', 'group', 'identifier', 'index']

df_final = pd.concat([df1, df2])
df_final = pd.merge(df_final, df_binary, on="word", how="left")

def clean_target_word_with_tags(sentence):
    if sentence.find("<b>")!=-1:
        start_str = sentence[:sentence.find("<b>")+6]
        end_str = sentence[sentence.find("</i>"):]
        word = sentence[sentence.find("<b>")+6:sentence.find("</i>")]
        word = re.sub('\W+', '', word)
        sentence = start_str + word + end_str
    return sentence

df_final["senten"] = df_final["sent"].apply(clean_target_word_with_tags)

df_final.head()

def clean_target_word_for_missing_tags(sentence, tag):
    start = sentence.find(tag)
    end = sentence.find(tag)+len(tag)
    start_str = sentence[:start]
    end_str = sentence[end:]
    word = sentence[start:end]
    word = re.sub('\W+', '', word)
    sentence = start_str + word + end_str
    return sentence

def get_indices_of_tags(sentence, word):
    if sentence.find("<b>")!=-1:
        return str(sentence.find("<b>"))+":"+str(sentence.find("</i>")-6)
    else:
        max_score_partial = 0
        max_score_sort = 0
        tag = ''
        for i in sentence.split(" "):
            if fuzz.token_sort_ratio(i, word)>max_score_sort and fuzz.partial_ratio(i, word)>max_score_partial:
                max_score_sort = fuzz.token_sort_ratio(i, word)
                max_score_partial = fuzz.partial_ratio(i, word)
                tag = i
        tag = re.sub('\W+', '', tag)
        sentence = clean_target_word_for_missing_tags(sentence, tag)
        return str(sentence.find(tag))+":"+str(sentence.find(tag)+len(tag))

df_final["indexes_target_token"] = df_final.apply(lambda x: get_indices_of_tags(x.senten, x.word), axis=1)

df_final.head()

def clean_text(sentence):
    return sentence.replace("<b>","").replace("<i>","").replace("</b>","").replace("</i>","")

df_final["sent"] = df_final["sent"].apply(clean_text)

def get_indices_of_sent(sentence):
    return "0:"+str(len(sentence))

df_final["indexes_target_sentence"] = df_final["sent"].apply(get_indices_of_sent)

df_final = df_final.rename(columns = {"sent":"context", "word":"lemma"})

df_final.loc[df_final["group"] == "EARLIER", "date"] = "1918-1990"
df_final.loc[df_final["group"] == "LATER", "date"] = "1991-2017"

df_final["grouping"] = df_final["group"]
df_final.loc[df_final["grouping"] == "EARLIER", "grouping"] = 1
df_final.loc[df_final["grouping"] == "LATER", "grouping"] = 2
df_final["description"] = np.nan
df_final = df_final[['lemma', 'pos', 'date', 'grouping', 'identifier', 'description', 'context', 'indexes_target_token', 'indexes_target_sentence', 'index']]

df_final.fillna('', inplace=True)

df_final = df_final.sort_values(by = ['lemma', 'index'], ascending = [True, True]).drop("index", axis=1)

df_final

for i in list(df_final["lemma"].value_counts().index):
    df_temp = df_final[df_final["lemma"]==i]
    numpy_df = df_temp.to_numpy()
    header = list(df_temp.columns)
    numpy_df = np.vstack([header, numpy_df])
    if not os.path.exists(i):
        os.mkdir(i)
    np.savetxt(i+"/uses.csv", numpy_df,fmt='%s', delimiter='\t')

