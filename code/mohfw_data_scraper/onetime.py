import requests
import re 
import os.path
from os import path
import bs4
from bs4 import BeautifulSoup
import couchdb

# I scripted this in urgency, So code quality or the logic isn't great.
# This is mostly a hack. 

# To RUN
# Clone the project
# Set up a virual environment 
# Install everything in requirements
# setup pushover_api_token, pushover_user_key and covid_db_full_url in env
# needs couchdb
# run this by calling `python3 scraper.py`
# You can also schedule it using the digdag

pushover_api_token =str(os.environ.get("pushover_api_token"))
pushover_user_key = str(os.environ.get("pushover_user_key"))
pushover_url = "https://api.pushover.net/1/messages.json"
covid_db_full_url = str(os.environ.get("covid_db_full_url"))
archive_folder_path = str(os.environ.get("archive_folder_path")) 
force_run = False

couchdb_db_name = "covid19"
couch = couchdb.Server(covid_db_full_url)
#database = couch[couchdb_db_name]

for d in database:	
	if str(d).startswith("2020-04-01T17"):
		data = database[d]
		print(d)
		#database.delete(data)
