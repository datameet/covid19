# importing the module
import os
import couchdb
import json
covid_db_full_url = str(os.environ.get("covid_db_full_url"))
couchdb_db_name = "covid19"
couch = couchdb.Server(covid_db_full_url)
database = couch[couchdb_db_name]

## FIX 1 - Rename attributes for better support
# with open('../../data/mohfw_vaccination_status.json') as json_file:
#     dataset = json.load(json_file)
#     rows = dataset["rows"]
#     for data_row in rows:
#         data = data_row["value"]
#         if "1stdose" in data:
#             data["first_dose"] = data["1stdose"]
#             del data["1stdose"]
#         if "2nddose" in data:
#             data["second_dose"] = data["2nddose"]
#             del data["2nddose"]
#         print(data)
#         #database.save(data)
  
  
## FIX 2 - 2022-01-09, first_dose_15_18 = null when it doesnt exist
# with open('../../data/mohfw_vaccination_status.json') as json_file:
#     dataset = json.load(json_file)
#     rows = dataset["rows"]
#     for data_row in rows:
#         data = data_row["value"]
#         if "first_dose_15_18" in data:
#             pass
#         else:
#             data["first_dose_15_18"] = None
            
#         print(data)
#         #database.save(data)


# # FIX 3 - 2022-01-11, precaution_dose = null when it doesnt exist
# with open('../../data/mohfw_vaccination_status.json') as json_file:
#     dataset = json.load(json_file)
#     rows = dataset["rows"]
#     for data_row in rows:
#         data = data_row["value"]
#         if "precaution_dose" in data:
#             pass
#         else:
#             data["precaution_dose"] = None
            
#         print(data)
#         database.save(data)


# # FIX 4 - 2022-02-02, second_dose_15_18 = null when it doesnt exist
# with open('../../data/mohfw_vaccination_status.json') as json_file:
#     dataset = json.load(json_file)
#     rows = dataset["rows"]
#     for data_row in rows:
#         data = data_row["value"]
#         if "second_dose_15_18" in data:
#             pass
#         else:
#             data["second_dose_15_18"] = None
            
#         print(data)
#         database.save(data)
