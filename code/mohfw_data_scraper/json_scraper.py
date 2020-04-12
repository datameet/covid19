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

# I scripted this in urgency, So code quality or the logic isn't great.
# This is mostly a hack. 

archive_folder_path = str(os.environ.get("archive_folder_path")) 

def getCurrentDataTimeAsString():
	now = datetime.now() 
	print("now =", now)
	return now.strftime("%d-%m-%YT%H-%M-%S")	


def getDataJSON():	
	url = "https://www.mohfw.gov.in/dashboard/data/data.json?"+getCurrentDataTimeAsString()
	r = requests.get(url)	
	txt = ""
	if r.status_code == 200:
		txt = r.text
		return txt

def checkIfThisFileExists(partial_file_name):
	for filename in os.listdir(archive_folder_path.format("data_json")):
		if filename.endswith(partial_file_name):
			just_file_name = (filename.split("/"))[0]
			#12-04-2020T22-49-55_md5_6eb1457605b8dada8ffd89b8fbb6ffa0.json
			just_file_name = just_file_name.replace(partial_file_name, "")
			just_file_names = just_file_name.split("T")
			day_part = just_file_names[1]
			time_part = just_file_names[0]
			time_part = time_part.replace("-",":")
			report_time = day_part+"T"+time_part+":00.00+05:30"
			return True, filename, report_time
	return False, "", ""

def getDataJSONFileName(partial_file_name):
	now = datetime.now()
	return now.strftime("%Y-%m-%dT%H-%M-%S-00")+partial_file_name



def scrape_data_now():
	
	data = getDataJSON()	
	h = hashlib.md5(data.encode()).hexdigest()
	print("hash:",h)
	partial_file_name = "_md5_{0}.json".format(h)
	print("partial_file_name:",partial_file_name)

	exists, filename, report_time = checkIfThisFileExists(partial_file_name)

	if exists:
		print("Exists:", filename)
		pass
	else:
		json_full_file_name = archive_folder_path.format("data_json")+"/"+getDataJSONFileName(partial_file_name)
		print("creating:", json_full_file_name)
		f = open(json_full_file_name, "a")
		f.write(data)

if __name__ == "__main__":
	scrape_data_now()
