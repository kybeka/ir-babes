# save this as app.py
#Flask
from flask import Flask, jsonify
from flask_cors import CORS

import pyterrier as pt
import pymongo
import pandas as pd
import json

from controllers.making_db import make_db
from controllers.indexing import indexing, getQueryResult
from controllers.clustering import get_topic_names, document_by_topic


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
    make_db()
    # Load the necessary files in...
else:
    collection_name = db[collection_name]
    # Retrieve all documents from the collection
    cursor = collection_name.find()

    # Convert the cursor to a list of dictionaries
    db_objs = list(cursor)

#Called upom initial launch of program
index = indexing()

# Flask --------------------------------------------------------------------------------

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/search/<query>', methods=['GET'])
def send_q(query):
    if not (query):
        return "[]"
    query = [["q1", query]]
    return getQueryResult(index, query, db_objs)


@app.route('/menus', methods=['GET'])
def get_topics():
    tn = get_topic_names()
    return tn


@app.route('/topic/<query>', methods=["GET"])
def get_articles(query):
    df = document_by_topic(str(query), '../backend/db/output.json')
    return df.to_json(orient='records', lines=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
