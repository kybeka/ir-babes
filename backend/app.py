# save this as app.py
#Flask
from flask import Flask, jsonify
from flask_cors import CORS

import pyterrier as pt
import pymongo
import pandas as pd
import json

from controllers.indexing import indexing, getQueryResult


# In order to re-do all the steps before launching backend:
# 1) Re-do all the steps in `index_demo.ipynb`
# 2) Change the file names accordingly and run all the steps as needed
DBPATH = '../indexing/db/make_db2.json'
PREINDEXTABLE = '../indexing/db/output.json'

# Mongo ---------------------------------------------------------------------------------

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
database_name = "db_ai"
db = client[database_name]

collection_name = "db"

# Check if the collection exists
if collection_name not in db.list_collection_names():
    # Collection doesn't exist, create it
    db.create_collection(collection_name)
    # Load the necessary files in...
else:
    collection_name = db[collection_name]
    # Retrieve all documents from the collection
    cursor = collection_name.find()

    # Convert the cursor to a list of dictionaries
    db_objs = list(cursor)



index = indexing()


# db_objs = []

# with open(DBPATH, "r") as f:
#     objects = json.load(f)
#     for obj in objects:
#         db_objs.append(obj)

# Flask --------------------------------------------------------------------------------

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

# Routes
# @app.route("/")
# def hello():
#     return "Hello, World!"

# # sanity check route
# @app.route('/ping', methods=['GET'])
# def ping_pong():
#     return jsonify('pong!')

# @app.route('/getQuery', methods=['GET'])
# def get_q():
#     query = [["q1", "data analysis"], ["q2", "gemini"]]
#     # getQueryResult(index, query, db_objs)
#     return (getQueryResult(index, query, db_objs)).to_json(orient='records', lines=True)


@app.route('/ping/<parameter>', methods=['GET'])
def example_route(parameter):
    return jsonify({'parameter': parameter}, {"just": "ok"})


@app.route('/search/<query>', methods=['GET'])
def send_q(query):
    query = [["q1", query]]
    return getQueryResult(index, query, db_objs)


    




if __name__ == '__main__':
    app.run(debug=True, port=5000)


# ------------------------------------------------------------------------------------------


# @app.route('/api/search', methods=['GET'])
# def search():
#     # Perform MongoDB query here and return results
#     results = collection.find({"your_query_here"})
#     return jsonify({"data": results})

