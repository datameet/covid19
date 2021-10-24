# importing the module
import os
import couchdb
import json
covid_db_full_url = str(os.environ.get("covid_db_full_url"))
couchdb_db_name = "covid19"
couch = couchdb.Server(covid_db_full_url)
database = couch[couchdb_db_name]


# Opening JSON file
with open('../../data/mohfw_vaccination_status.json') as json_file:
    dataset = json.load(json_file)
    rows = dataset["rows"]
    for data_row in rows:
        data = data_row["value"]
        if "1stdose" in data:
            data["first_dose"] = data["1stdose"]
            del data["1stdose"]
        if "2nddose" in data:
            data["second_dose"] = data["2nddose"]
            del data["2nddose"]
        print(data)
        #database.save(data)
  
  
