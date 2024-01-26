import json
import os
from pymongo import MongoClient

# This file is responsible for creating a "jumbo" database of all our scraped files
# The outputted file is not properly yet formatted for indexing however
# That is dealt in `db_clean.py` within the controllers folder

def make_db():
    # The difference between `make_db` and `make_db2` is that `make_db2` has the JSON object of date pre-flattened
    # output_file_path = '../../indexing/db/make_db2.json'
    output_file_path = '../../indexing/db/make_db2.json'


    # if it doesn't already exist it will make it, otherwise it won't, and skip it
    if not os.path.exists(output_file_path):
        # List to store combined JSON objects
        combined_data = []

        # List of file paths
        file_paths = ['../crawler/ir/crawled/content/content_aitimes.jsonl', 
                    '../crawler/ir/crawled/content/content_mit.jsonl', 
                    '../crawler/ir/crawled/content/content_vidhya.jsonl']

        # Read each file and append its JSON objects to the combined_data list
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    json_data = json.loads(line.strip())

                    # Flatten the "date" field
                    if "date" in json_data:
                        json_data["year"] = json_data["date"]["year"]
                        json_data["month"] = json_data["date"]["month"]
                        del json_data["date"]

                    combined_data.append(json_data)

        # Write the combined_data list to a new JSON file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(combined_data, output_file, indent=2)

    # Establish a connection to MongoDB
    # client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB connection string

    mongo_db_password = os.getenv('MONGO_DB_PASSWORD')
    # Construct the MongoDB connection string
    mongo_uri = f'mongodb+srv://kylabkaplan:{mongo_db_password}@cluster0.zyftcau.mongodb.net/'
    # Create a MongoClient instance
    client = MongoClient(mongo_uri)

    database = client['db_ai']  # Replace 'your_database_name' with the actual database name
    collection_name = 'db'

    # Check if the collection exists
    if not collection_exists(database, collection_name):
        # Create the collection if it doesn't exist
        database.create_collection(collection_name)
        collection = database[collection_name]
        # Insert each document into the MongoDB collection
        for json_data in combined_data:
            collection.insert_one(json_data)

    # print(f'Combined data saved to {output_file_path}')

def collection_exists(db, collection_name):
    return collection_name in db.list_collection_names()
