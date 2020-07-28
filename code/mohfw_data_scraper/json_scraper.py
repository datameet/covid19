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

pushover_api_token =str(os.environ.get("pushover_api_token"))
pushover_user_key = str(os.environ.get("pushover_user_key"))
pushover_url = "https://api.pushover.net/1/messages.json"
covid_db_full_url = str(os.environ.get("covid_db_full_url"))
archive_folder_path = str(os.environ.get("archive_folder_path")) 

states = {}
states["Andhra Pradesh"]="AP"
states["Arunachal Pradesh"]="AR"
states["Assam"]="AS"
states["Bihar"]="BR"
states["Chattisgarh"]="CT"
states["Chhattisgarh"]="CT"
states["Goa"]="GA"
states["Gujarat"]="GJ"
states["Haryana"]="HR"
states["Himachal Pradesh"]="HP"
states["Jharkhand"]="JH"
states["Jharkhand#"]="JH"
states["Karnataka"]="KA"
states["Kerala"]="KL"
states["Madhya Pradesh"]="MP"
states["Madhya Pradesh#"]="MP"
states["Maharashtra"]="MH"
states["Manipur"]="MN"
states["Meghalaya"]="ML"
states["Mizoram"]="MZ"
states["Nagaland"]="NL"
states["Nagaland#"]="NL"
states["Odisha"]="OR"
states["Punjab"]="PB"
states["Rajasthan"]="RJ"
states["Sikkim"]="SK"
states["Tamil Nadu"]="TN"
states["Telengana"]="TG"
states["Telangana***"]="TG"
states["Tripura"]="TR"
states["Uttarakhand"]="UT"
states["Uttar Pradesh"]="UP"
states["West Bengal"]="WB"
states["Andaman and Nicobar Islands"]="AN"
states["Chandigarh"]="CH"
states["Dadra and Nagar Haveli"]="DN"
states["Dadar Nagar Haveli"]="DN"
states["Daman and Diu"]="DD"
states["Daman & Diu"]="DD"
states["Delhi"]="DL"
states["Jammu and Kashmir"]="JK"
states["Ladakh"]="LA"
states["Lakshadweep"]="LD"
states["Pondicherry"]="PY"
states["Puducherry"]="PY"
states["Dadra and Nagar Haveli and Daman and Diu"]="DN_DD"
states["Telangana"]="TG"

def getCurrentDataTimeAsString():
	now = datetime.now() 
	print("now =", now)
	#current_date_time = now.strftime("%d-%m-%YT%H-%M-%S")
	timepart = "T8:00:00.00+05:30"
	current_date_time = now.strftime("%d-%m-%Y")+timepart	
	return current_date_time


def getDataJSON():	
	url = "https://www.mohfw.gov.in/data/datanew.json?"+getCurrentDataTimeAsString()
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
	current_date_time = getCurrentDataTimeAsString()
	return current_date_time+partial_file_name



def scrape_data_now():
	load = True
	current_date_time = getCurrentDataTimeAsString()
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
	
	if load:
		couchdb_db_name = "covid19"
		couch = couchdb.Server(covid_db_full_url)
		database = couch[couchdb_db_name]
		message = ""
		json_data = json.loads(data)
		for state_data in json_data:
			print("---------------------")
			print(state_data)
			print("---------------------")
			state_name = state_data["state_name"]
			if state_name == "":
				continue
			
			state_code = states[state_name]
			_id =  current_date_time+"|"+state_code

			data = {}
			data["_id"] = _id
			data["state"] = state_code
			data["report_time"] = current_date_time
			data["cured"] = state_data["cured"]
			data["death"] = state_data["death"]
			data["confirmed"] =   state_data["positive"] 
			data["source"] ="mohfw"
			data["type"] ="cases"

			try:
				if database[_id]:
					print("***** EXISTS *****")
					#print(counter)
					print(data)
					message = message + " \n EXISTS " +str(_id) +" \n"
			except couchdb.http.ResourceNotFound:
					print("##### ADDING #####")
					#print(counter)
					message = message + " \n ADDING " +str(_id) +" \n"
					#database.save(data)	
					print(data)
			

if __name__ == "__main__":
	scrape_data_now()
