import requests
import re 
import os.path
from os import path
import bs4
from bs4 import BeautifulSoup
import couchdb
from datetime import datetime
import hashlib 
import json
import pandas as pd

# I scripted this in urgency, So code quality or the logic isn't great.
# This is mostly a hack. 

#covid_db_full_url = str(os.environ.get("covid_db_full_url"))
archive_folder_path = str(os.environ.get("archive_folder_path")) 

for filename in sorted(os.listdir(archive_folder_path.format("district_wise_positivity_rates"))):
    if filename.endswith(".xlsx"):
        print(filename)
        df = pd.read_excel(archive_folder_path.format("district_wise_positivity_rates")+"/"+filename, engine = 'openpyxl')
        print(df.loc[5])
        break

