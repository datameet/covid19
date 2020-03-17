import requests
import re 
import os.path
from os import path
import bs4
from bs4 import BeautifulSoup
import couchdb

pushover_api_token =str(os.environ.get("pushover_api_token"))
pushover_user_key = str(os.environ.get("pushover_user_key"))
pushover_url = "https://api.pushover.net/1/messages.json"
covid_db_full_url = str(os.environ.get("covid_db_full_url"))
archive_folder_path = "../mohfw-backup/{0}"

states = {}
states["Andhra Pradesh"]="AP"
states["Arunachal Pradesh"]="AR"
states["Assam"]="AS"
states["Bihar"]="BR"
states["Chhattisgarh"]="CT"
states["Goa"]="GA"
states["Gujarat"]="GJ"
states["Haryana"]="HR"
states["Himachal Pradesh"]="HP"
states["Jharkhand"]="JH"
states["Karnataka"]="KA"
states["Kerala"]="KL"
states["Madhya Pradesh"]="MP"
states["Maharashtra"]="MH"
states["Manipur"]="MN"
states["Meghalaya"]="ML"
states["Mizoram"]="MZ"
states["Nagaland"]="NL"
states["Odisha"]="OR"
states["Punjab"]="PB"
states["Rajasthan"]="RJ"
states["Sikkim"]="SK"
states["Tamil Nadu"]="TN"
states["Telengana"]="TG"
states["Tripura"]="TR"
states["Uttarakhand"]="UT"
states["Uttar Pradesh"]="UP"
states["West Bengal"]="WB"
states["Andaman and Nicobar Islands"]="AN"
states["Chandigarh"]="CH"
states["Dadra and Nagar Haveli"]="DN"
states["Daman and Diu"]="DD"
states["Delhi"]="DL"
states["Jammu and Kashmir"]="JK"
states["Ladakh"]="LA"
states["Lakshadweep"]="LD"
states["Puducherry"]="PY"


def getFileName(t):
	t = t.replace("as on ","")
	t = t.replace(".","-")
	t = t.replace(" ","-")
	t = t.replace(":","-")
	t = t+".html"
	return t

# This is not great way of doing. This is just a hack
# I foculd have used standard date formatter!! 
def getFormattedDate(t):
	x = t.replace("as on ","", 1)
	parts = x.split(" at ")

	date_parts = (parts[0]).split(".")
	day = date_parts[0]
	if len(day) == 1:
		day = "0"+day

	month = date_parts[1]
	if len(month) == 1:
		month = "0"+month

	year = date_parts[2]
	time_parts = (parts[1]).split(" ")
	am_pm = time_parts[1]
	hour = ((time_parts[0]).split(":"))[0]

	if am_pm == "PM":
		hour = str(int(hour)+12)
	if len(hour) == 1:
		hour = "0"+hour

	minute = ((time_parts[0]).split(":"))[1]
	if len(minute) == 1:
		minute = "0"+minute

	std_format = "2020-{0}-{1}T{2}:{3}:00.00+05:30".format(month, day,hour,minute)
	return str(std_format)

def getContents():
	url = "https://www.mohfw.gov.in/"
	r = requests.get(url)	
	txt = ""
	if r.status_code == 200:
		txt = r.text
		return txt

def sendMessage(title, message):
	myobj = {}
	myobj["user"] = pushover_user_key
	myobj["token"] = pushover_api_token
	myobj["message"] = message
	x = requests.post(pushover_url, data = myobj)

def scrape_now():
	title = "Started"
	message = "started \n"
	couchdb_db_name = "covid19"
	couch = couchdb.Server(covid_db_full_url)
	database = couch[couchdb_db_name]

	txt = getContents()

	date_pattern = "as on \d\d.\d\d.2020 at \d\d:\d\d [A,P]M"
	x = re.findall(date_pattern, txt)
	extracted_date_text = x[0]

	full_date_text =  getFormattedDate(extracted_date_text)
	full_file_name =  archive_folder_path.format(getFileName(extracted_date_text))

	print(extracted_date_text)
	print(full_file_name)
	print(full_date_text)


	title = title +"extracted_date_text "+str(extracted_date_text)						
	message = message + "full_file_name ="+ full_file_name +" \n"
	message = message +  "full_date_text ="+ full_date_text +" \n"

	if path.exists(full_file_name):
		message = message +  " FILE EXISTS NOTHING TO BE DONE \n"
		print("FILE Exists and nothing to be done")
		sendMessage(title, message)
		return 0
	else:
		#Backup first
		message = message +  " WRITING THE FILE \n"
		print("Writing to a file")
		f = open(full_file_name, "a")
		f.write(txt)
		message = message +  " WRITING COMPLETE \n"

	#get to parsing
	soup = BeautifulSoup(txt, 'html.parser')
	tables = soup.find_all('table')
	if len(tables) > 0:
		table = tables[0]
		#print(table)
		first_row = True
		for tr in list(table.children):
			if isinstance(tr, bs4.element.Tag): 
				if first_row:
					print("FIRST ROW")
					first_row = False
					continue

				tds = list(tr.children)

				if "Total number of confirmed cases in India" == tds[1].get_text():
					continue


				report_time = full_date_text
				state = (tds[3]).get_text()
				state = state.replace("Union Territory of ","")
				state = state.strip()
				state_code = ""
				if state in states :
					state_code = (states[state]).lower()
				else:
					sendMessage("ERROR WRONG STATE",  "Not found: {0}".format(state))
					print("------> Wrong state {0}".format(state))
					return 0

				_id =  report_time+"|"+state_code

				data = {}
				data["_id"] = _id
				data["state"] = state_code
				data["report_time"] = report_time
				data["confirmed_india"] =  int( (tds[5]).get_text() )
				data["confirmed_foreign"] = int( (tds[7]).get_text() )
				data["cured"] = int( (tds[9]).get_text() )
				data["death"] = int( (tds[11]).get_text() )

				try:
					if database[_id]:
						print("***** EXISTS *****")
						print(data)
						message = message + " \n EXISTS " +str(_id) +" \n"
				except couchdb.http.ResourceNotFound:
						print("##### ADDING #####")
						message = message + " \n ADDING " +str(_id) +" \n"
						database.save(data)	
						print(data)
		print("SENDING message")
		print(title)
		print(message)
		sendMessage(title, message)						
	else:
		message = message +  " ERROR: No Table found \n"
		sendMessage(title, message)
		print("No Table found")



if __name__ == "__main__":
	scrape_now()
