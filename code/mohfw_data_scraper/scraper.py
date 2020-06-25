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
force_run = True
#date_pattern = "as on : \d\d June 2020, \d\d:\d\d "
date_pattern = "as on : \d\d	June 2020, \d\d:\d\d "
month_formatted = "06"


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




def getFileName(t):
	t = t.replace("as on ","")
	t = t.replace(".","-")
	t = t.replace(" ","-")
	t = t.replace(":","-")
	t = t+".html"
	return t

# This is not a great way of doing this. This is just a hack
# I foculd have used standard date formatter!! 
def getFormattedDate(t):
	x = t.replace("as on : ","", 1)
	parts = x.split(", ")
	print(parts)
	date_parts = (parts[0]).split(" ")
	day = date_parts[0]
	if len(day) == 1:
		day = "0"+day

		print("day=", day)
	# month = date_parts[1]
	# if len(month) == 1:
	# 	month = "0"+month
	month = month_formatted

	# year = date_parts[2]
	year = "2020"

	time_parts = (parts[1]).split(" ")
	am_pm = time_parts[1]
	hour = ((time_parts[0]).split(":"))[0]

	# if am_pm == "PM":
	# 	hour = str(int(hour)+12)
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
	try:
		x = requests.post(pushover_url, data = myobj)
	except:
		print(pushover_url)
		print("ERROR IN SENDING MESSAGE TO PUSHOVER")

def scrape_now():
	title = "Started"
	message = "started \n"
	couchdb_db_name = "covid19"
	couch = couchdb.Server(covid_db_full_url)
	database = couch[couchdb_db_name]

	txt = getContents()
	#print(txt)

	x = re.findall(date_pattern, txt)
	extracted_date_text = x[0]
	print("before",extracted_date_text)
	extracted_date_text = extracted_date_text.replace("\t", " ")
	print("after",extracted_date_text)

	full_date_text =  getFormattedDate(extracted_date_text)
	#for force run specific file or date
	#full_date_text = "2020-05-01T08:00:00.00+05:30"
	full_file_name =  archive_folder_path.format(getFileName(full_date_text))

	print(full_file_name)
	print(full_date_text)
	counter = 1

	title = title +"extracted_date_text "+str(extracted_date_text)						
	message = message + "full_file_name ="+ full_file_name +" \n"
	message = message +  "full_date_text ="+ full_date_text +" \n"

	if path.exists(full_file_name):
		message = message +  " FILE EXISTS NOTHING TO BE DONE \n"
		print("FILE Exists and nothing to be done")
		if(force_run):
			with open(full_file_name, "r") as f:
				txt = str(f.read())
		else:
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
	tables = soup.find_all('tbody')
	if len(tables) > 0:
		table = tables[0]
		#print(table)
		first_row = False
		for tr in list(table.children):
			if isinstance(tr, bs4.element.Tag): 
				if first_row:
					print("FIRST ROW")
					first_row = False
					continue

				tds = list(tr.children)

				if len(tds) > 1:
					pass
				else:
					continue

				if "Total number of" in str(tds[1].get_text()):
					break


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
				data["confirmed"] =  int( (tds[11]).get_text() )
				#data["confirmed_india"] =  int( (tds[5]).get_text() )
				#data["confirmed_foreign"] = int( (tds[7]).get_text() )
				data["cured"] = int( (tds[7]).get_text() )
				data["death"] = int( (tds[9]).get_text().replace("#","") )
				data["source"] ="mohfw"
				data["type"] ="cases"

				try:
					if database[_id]:
						print("***** EXISTS *****")
						print(counter)
						print(data)
						message = message + " \n EXISTS " +str(_id) +" \n"
				except couchdb.http.ResourceNotFound:
						print("##### ADDING #####")
						print(counter)
						message = message + " \n ADDING " +str(_id) +" \n"
						database.save(data)	
						print(data)
				counter = counter + 1
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
