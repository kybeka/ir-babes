# save this as app.py
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})


@app.route("/")
def hello():
    return "Hello, World!"



# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')




if __name__ == '__main__':
    app.run()










# from pyterrier import Indexer
# import pymongo
# from flask import Flask, jsonify
# from flask_cors import CORS
# import pandas as pd


# # Connect to MongoDB
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# database_name = "db_ai"
# db = client[database_name]


# # Index your data using PyTerrier
# indexer = Indexer([your_data_source])
# index = indexer.index()

# # Store the index in MongoDB
# for document in index.getCollection().getDocuments():
#     collection.insert_one(document.to_dict())



# app = Flask(__name__)



# @app.route('/api/search', methods=['GET'])
# def search():
#     # Perform MongoDB query here and return results
#     results = collection.find({"your_query_here"})
#     return jsonify({"data": results})

# if __name__ == '__main__':
#     app.run(port=5000)



# # After initializing Flask app
# CORS(app)


# #INPUT THE FUNCTIONS NEEDED FROM THE .IPYNB
# # 1) get the query from server.js
# # 2) decompose it here
# # 3) get it and decompose it



# def retrieve_info(cdf, db_objects):
#     article_title = []
#     article_author = []
#     article_year = []
#     for i in range(cdf.shape[0]):
#         docId = cdf.loc[i, "docno"]
#         docNo = int(docId[1:]) - 1
#         article_title.append(db_objects[docNo]["title"])
#         article_author.append(db_objects[docNo]["author"])
#         article_year.append(db_objects)[docNo]["year"]
#     cdf["title"] = article_title
#     cdf["author"] = article_author
#     cdf["year"] = article_year
    
#     return cdf



# def getQueryResult(index, query, db_objs):
#     bm25 = pt.BatchRetrieve(index, num_results=10, wmodel="BM25")

#     queries = pd.DataFrame(
#         query,
#         columns=["qid", "query"],
#     )

#     results = bm25.transform(queries)
#     formatedResult = retrieve_info(results, db_objs)
#     print(formatedResult)

# db_objs = []



# with open('../indexing/db/make_db2.json', "r") as f:
#     objects = json.load(f)
#     for obj in objects:
#         db_objs.append(obj)


# preIndexTable = pd.read_json('../indexing/db/output.json')
# indexer = pt.DFIndexer('./index_ai', overwrite=True)
# index_ref = indexer.index(preIndexTable["text"], preIndexTable["docno"])
# index_ref.toString()


# query = [["q1", "data analysis"], ["q2", "gemini"]]
# getQueryResult(index, query, db_objs)


# query1 = [["q1", "bard"], ["q2", "openai"]]
# getQueryResult(index, query1, db_objs)