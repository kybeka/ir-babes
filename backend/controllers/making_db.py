import json
import os

# This file is responsible for creating a "jumbo" database of all our scraped files
# The outputted file is not properly yet formatted for indexing however
# That is dealt in `db_clean.py` within the controllers folder

def make_db():
    # The difference between `make_db` and `make_db2` is that `make_db2` has the JSON object of date pre-flattened
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

        # print(f'Combined data saved to {output_file_path}')
