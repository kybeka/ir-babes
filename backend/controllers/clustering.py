# Importing necessary libraries and modules
import nltk
from nltk.corpus import stopwords
import string
import os
import json
import pandas as pd
import pyterrier as pt
import numpy as np
from pymongo import MongoClient

# Downloading NLTK resources
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Importing scikit-learn modules
import sklearn
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans, DBSCAN
from sklearn.manifold import TSNE
from sklearn.mixture import GaussianMixture

# Importing matplotlib for visualization
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# Initializing PyTerrier if not already started
if not pt.started():
  pt.init()

# Creating a list of English stopwords and punctuation marks
english_stopwords = stopwords.words('english')
punctuation = string.punctuation

# Custom tokenizer function for preprocessing text
def custom_tokenizer(text):
    tokens = text.split()
    tokens = [word for word in tokens if (word not in punctuation and word.lower() not in english_stopwords)]
    return " ".join(tokens)

# Example usage of custom_tokenizer
# test = "I am myself we make ginger latte in Zimbabe !"
# print("output", custom_tokenizer(test))

mongo_db_password = os.getenv('MONGO_DB_PASSWORD')
# Construct the MongoDB connection string
mongo_uri = f'mongodb+srv://kylabkaplan:{mongo_db_password}@cluster0.zyftcau.mongodb.net/'
# Create a MongoClient instance
client = MongoClient(mongo_uri)
# client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["db_ai"]
collection_name = "list_of_topics"

def get_topic_names():
    # Open the text file in read mode
    with open('../backend/db/data.txt', 'r') as file:
        # Initialize an empty array to store the JSON objects
        array_of_lines = []
        text = []

        # Read each line from the file
        for line in file:
            # print("LINE BEFORE", line)
            linemod = {}

            # Parse each line as a JSON object
            json_line = json.loads(line)
            linemod["docno"] = json_line["docno"]
            string_text = custom_tokenizer(json_line["text"])
            linemod["docno"] = string_text

            array_of_lines.append(json_line)
            text.append(string_text)

    # Assuming you already have 'text' as a list of sentences

    # Step 1: Vectorization using CountVectorizer (Bag-of-Words representation)
    vectorizer = CountVectorizer(stop_words='english', lowercase=True)
    X = vectorizer.fit_transform(text)

    # Step 2: Apply LDA
    num_topics = 5  # Specify the number of topics
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    doc_topic_matrix = lda.fit_transform(X)

    # Step 3: Display single-word topics
    feature_names = vectorizer.get_feature_names_out()
    topic_names = [f"Topic {i}" for i in range(num_topics)]

    df_topics = pd.DataFrame(lda.components_, columns=feature_names, index=topic_names).T

    list_of_names = []

    # Display the most representative word for each topic
    for topic in topic_names:
        top_word = df_topics[topic].idxmax()
        print(f"{topic}: {top_word}")
        list_of_names.append({topic: top_word})

    print("LIST OF NAMES", list_of_names)

    # Insert the list_of_names into the MongoDB collection
    if collection_name not in db.list_collection_names():
        # If the collection doesn't exist, create it
        collection = db.create_collection(collection_name)  # Set your preferred size
        # Insert the list_of_names into the MongoDB collection
        collection.insert_many(list_of_names)

    # Call the clustering next
    clustering(doc_topic_matrix, topic_names, df_topics, text)
    return list_of_names




# Function for performing clustering on text data
def clustering(doc_topic_matrix, topic_names, df_topics, text):
    # Step 4: Assign topics to each document
    df = pd.DataFrame(doc_topic_matrix, columns=topic_names)
    df['Dominant_Topic'] = df.idxmax(axis=1)

    # Step 5: Print the DataFrame with sentences and dominant topics
    df_sentences = pd.DataFrame({'Sentences': text})
    df_final = pd.concat([df_sentences, df], axis=1)

    columns_to_drop = ['Topic 0', 'Topic 1', 'Topic 2', 'Topic 3', 'Topic 4']
    df_final = df_final.drop(columns=columns_to_drop)

    json_dict = []

    for index, row in df_final.iterrows():
        local_dict = {}
        local_dict["docno"] = "d" + str(index + 1)
        local_dict["topic"] = df_topics[row["Dominant_Topic"]].idxmax()
        # local_dict["topic_nr"] = row["Dominant_Topic"].idxmax()

        json_dict.append(local_dict)

    file_path = '../backend/db/output.json'
    # Dump the array of dictionaries into a JSON file
    with open(file_path, 'w') as json_file:
        json.dump(json_dict, json_file, indent=2)

    return json_dict


def document_by_topic(topic, clusterd_json):
    collection_name = "db"

    db_objs = None

    # Check if the collection exists
    if collection_name not in db.list_collection_names():
        # Collection doesn't exist, create it
        db.create_collection(collection_name)
        # Load the necessary files in...
        collection_name = db[collection_name]
        # Retrieve all documents from the collection
        cursor = collection_name.find()

        # Convert the cursor to a list of dictionaries
        db_objs = list(cursor)

    else:
        collection_name = db[collection_name]
        # Retrieve all documents from the collection
        cursor = collection_name.find()

        # Convert the cursor to a list of dictionaries
        db_objs = list(cursor)

    article_title,article_author,article_year, article_month = [], [], [], []
    article_text, article_img, article_url, article_tags = [], [], [], []
    article_topic = []

    clustered_df = pd.DataFrame()

    with open(clusterd_json, 'r') as file:
        # Load the JSON data
        data = json.load(file)

        # Iterate through the list of dictionaries
        for i, item in enumerate(data):

            if item["topic"] == topic:
                
                # print("ITEM", item)

                # Access individual elements in each dictionary
                docId = item["docno"]
                
                docNo = int(docId[1:]) - 1

                article_title.append(db_objs[docNo]["title"])
                article_author.append(db_objs[docNo]["author"])
                article_year.append(db_objs[docNo]["year"])
                article_month.append(db_objs[docNo]["month"])
                article_text.append(db_objs[docNo]["text"])
                article_img.append(db_objs[docNo]["img_url"])
                article_url.append(db_objs[docNo]["article_url"])
                article_topic.append(item["topic"])

        clustered_df["title"] = article_title
        clustered_df["author"] = article_author
        clustered_df["year"] = article_year
        clustered_df["month"] = article_month
        clustered_df["text"] = article_text
        clustered_df["img"] = article_img
        clustered_df["url"] = article_url
        clustered_df["topic"] = article_topic

        return clustered_df
        

# if __name__=="__main__":
#     df = document_by_topic("data", "/home/kaplank/Documents/Y3/Q1/Information_Retrieval/ir-babes/backend/db/output.json")
#     print(df.head())
    