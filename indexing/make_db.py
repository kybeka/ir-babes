import json

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
            combined_data.append(json_data)

# Write the combined_data list to a new JSON file
output_file_path = './db/make_db.json'
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(combined_data, output_file, indent=2)

print(f'Combined data saved to {output_file_path}')


#TODO: Make a flattened version with 'date'
