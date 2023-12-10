import os
import json
import pandas as pd
import pyterrier as pt
import numpy as np


from controllers.db_clean import clean_json

# This file is responsible for building the dataframe for PyTerrier
# Then, using PyTerrier to index


def indexing():
    # print("Current working directory:", os.getcwd())
    output_file_path = '../indexing/db/output.json'

    data = clean_json()

    if not os.path.exists(output_file_path):

        docs_df = pd.DataFrame(pd.DataFrame([{'text': entry['text']} for entry in data]))
        docnumber = ["d" + str(x) for x in range(1,len(docs_df) + 1)]
        docs_df.insert(0, 'docno', docnumber)
        docs_df = docs_df.dropna(subset=['text'])
        dict_array = []

        for index, rows in docs_df.iterrows():
            row_dict = {}
            row = docs_df.iloc[index]
            row_dict["docno"] = row["docno"]
            row_dict["text"] = row["text"]
            dict_array.append(row_dict)

        with open(output_file_path, 'w') as json_file:
            json.dump(dict_array, json_file, indent=2)
        
        # print("Success")
    
    if not pt.started():
        pt.init()
    
    preIndexTable = pd.read_json(output_file_path)
    indexer = pt.DFIndexer('../indexing/index_ai', overwrite=True)
    index_ref = indexer.index(preIndexTable["text"], preIndexTable["docno"])
    index_ref.toString()
    index = pt.IndexFactory.of(index_ref)

    return index


# To collect statistics of the inverted index table
# print(index.getCollectionStatistics().toString())
# pd.DataFrame([(kv.getKey(), kv.getValue().toString()) for kv in index.getLexicon()]).tail()
# for kv in index.getLexicon():
#   print("%s  -> %s " % (kv.getKey(), kv.getValue().toString()  ))


def retrieve_info(cdf, db_objects):
    if len(cdf) <= 0:
        return pd.DataFrame().to_json()
    
    article_title,article_author,article_year, article_month = [], [], [], []
    article_text, article_img, article_url, article_tags = [], [], [], []

    threshold = thresholding(cdf, threshold=0.15)
    # print("THRESHOLD IS", threshold)

    for i in range(cdf.shape[0]):
        docId = cdf.loc[i, "docno"]
        docNo = int(docId[1:]) - 1
        article_title.append(db_objects[docNo]["title"])
        article_author.append(db_objects[docNo]["author"])
        article_year.append(db_objects[docNo]["year"])
        article_month.append(db_objects[docNo]["month"])
        article_text.append(db_objects[docNo]["text"])
        article_img.append(db_objects[docNo]["img_url"])
        article_url.append(db_objects[docNo]["article_url"])
            # article_tags.append(db_objects[docNo]["tags"])
    cdf["title"] = article_title
    cdf["author"] = article_author
    cdf["year"] = article_year
    cdf["month"] = article_month
    cdf["text"] = article_text
    cdf["img"] = article_img
    cdf["url"] = article_url
    # cdf["tags"] = article_tags

    # print("HERE NOW",len(cdf[0]))
    cdf_filterd = cdf[cdf["score"] >= threshold]
    # print("WATCH ME BITCH, HERE NOW", len(cdf[0]))
    return cdf_filterd.to_json(orient='records', lines=True)


def getQueryResult(index, query, db_objs):
    bm25 = pt.BatchRetrieve(index, num_results=10, wmodel="BM25")
    queries = pd.DataFrame(
        query,
        columns=["qid", "query"],
    )
    results = bm25.transform(queries)

    formattedResult = retrieve_info(results, db_objs)
    return formattedResult


def thresholding(cdf, threshold):
    scores = cdf["score"]
    max = np.max(np.array((scores)))
    # print("MAX ", max)
    return max - (max * threshold)









