
import json
import re
import calendar
import locale

# This file is responsible for "cleansing" our mini-jumbo-database in order to prepare it for indexing

def clean_json():
    # Path to the JSON file
    data_file_path = "../indexing/db/make_db2.json"

    # Load the data from the JSON file
    with open(data_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    # !!! This creates the `data` variable thanks to which we do some "JSON-cleansing" !!!

    locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')

    for entry in data:
        entry["text"] = entry["text"].strip('“”')  # Eliminar comillas al inicio y al final
        
        if entry["tags"]:
            concat = ""
            for elem in entry["tags"]:
                concat += elem + " "
            entry["tags"] = concat

        if 1 <= entry["month"] <= 12:
            month_name = calendar.month_name[entry["month"]]
            entry["month"] = month_name + " " + str(entry["month"])

    for entry in data:
        text = "{} {} {} {} {} {}".format(
            entry["text"], 
            entry["title"],
            entry["author"], 
            entry["tags"],
            entry["year"],
            entry["month"])
        text = re.sub(r'[^a-zA-Z0-9]', ' ',text.replace("None", " "))
        text = re.sub(r'\s{2,}', ' ', text)
        entry["text"] = text

    return data

