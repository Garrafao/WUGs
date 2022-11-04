from bs4 import BeautifulSoup
import requests
import pandas as pd
import io
import numpy as np
import os
import sys

def main():
    directory = sys.argv[1]

    if directory not in ["rushifteval1", "rushifteval2", "rushifteval3"]:
        print("Check Directory")
        sys.exit()
    if not os.path.exists(directory):
        os.mkdir(directory)
    URL = 'https://github.com/akutuzov/rushifteval_public/tree/main/durel/'+directory+'/data'
    page = requests.get(URL)

    soup = BeautifulSoup( page.content , 'html.parser')
    find_by_class = soup.find_all('a', class_="Link--primary")[3:]

    judgements = []
    uses = []
    for i in find_by_class:
        judgements.append("https://raw.githubusercontent.com/"+i['href']+"/judgments.csv")
        uses.append("https://raw.githubusercontent.com/"+i['href']+"/uses.csv")

    judgements_df = pd.DataFrame()
    for i in judgements:
        judgements_df = pd.concat([judgements_df, pd.read_csv(io.StringIO(requests.get(i.replace("/tree","")).content.decode('utf-8')), delimiter='\t')])

    judgements_df["comment"].value_counts()

    uses_df = pd.DataFrame()
    for i in uses:
        uses_df = pd.concat([uses_df, pd.read_csv(io.StringIO(requests.get(i.replace("/tree","")).content.decode('utf-8')), delimiter='\t')])

    judgements_grouped_df_with_comment = judgements_df.groupby(['identifier1', 'identifier2', 'annotator', 'comment', 'lemma'])['judgment'].apply(list).reset_index(name='judgments')
    # judgements_df['median_judgment'] = judgements_df['judgments'].apply(lambda x: np.nanmedian(list(x)))

    # Remove pairs with nan median
    # judgements_df = judgements_df[~judgements_df['median_judgment'].isnull()]
    print(judgements_grouped_df_with_comment)

    # Aggregate use pairs and extract median column
    judgements_grouped_df = judgements_df.groupby(['identifier1', 'identifier2', 'annotator', 'lemma'])['judgment'].apply(list).reset_index(name='judgment')
    # judgements_df['median_judgment'] = judgements_df['judgments'].apply(lambda x: np.nanmedian(list(x)))

    # Remove pairs with nan median
    # judgements_df = judgements_df[~judgements_df['median_judgment'].isnull()]
    print(judgements_grouped_df)

    judgements_grouped_df["comment"] = np.nan
    judgements_grouped_df = judgements_grouped_df[["identifier1", "identifier2", "annotator", "judgment", "comment", "lemma"]]

    print(judgements_grouped_df)

    judgements_grouped_df.fillna('', inplace=True)
    for i in list(judgements_grouped_df["lemma"].value_counts().index):
        df = judgements_grouped_df[judgements_grouped_df["lemma"]==i]
        numpy_df = df.to_numpy()
        header = list(df.columns)
        numpy_df = np.vstack([header, numpy_df])
        if not os.path.exists(directory+"/"+i):
            os.mkdir(directory+"/"+i)
        np.savetxt(directory+"/"+i+"/judgements_grouped.csv", numpy_df,fmt='%s', delimiter='\t')

    judgements_df.fillna('', inplace=True)
    for i in list(judgements_df["lemma"].value_counts().index):
        df = judgements_df[judgements_df["lemma"]==i]
        numpy_df = df.to_numpy()
        header = list(df.columns)
        numpy_df = np.vstack([header, numpy_df])
        if not os.path.exists(directory+"/"+i):
            os.mkdir(directory+"/"+i)
        np.savetxt(directory+"/"+i+"/judgements.csv", numpy_df,fmt='%s', delimiter='\t')

    uses_df.fillna('', inplace=True)
    for i in list(uses_df["lemma"].value_counts().index):
        df = uses_df[uses_df["lemma"]==i]
        numpy_df = df.to_numpy()
        header = list(df.columns)
        numpy_df = np.vstack([header, numpy_df])
        if not os.path.exists(directory+"/"+i):
            os.mkdir(directory+"/"+i)
        np.savetxt(directory+"/"+i+"/uses.csv", numpy_df,fmt='%s', delimiter='\t')

if __name__=="__main__":
    main()