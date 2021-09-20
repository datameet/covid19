import requests
import re 
import os
from os import path
from os import listdir
from os.path import isfile, join

import bs4
from bs4 import BeautifulSoup
import couchdb
import subprocess
import csv

archive_folder_path = str(os.environ.get("archive_folder_path")).format("cumulative_vaccination_coverage/") 

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

country_datarow_exceptions = {
    "2021-08-09-at-07-00-AM.pdf" :{"skip":"yes"}
}

def get_datetime(file_name):
    date_time = file_name.replace("-at-07-00-AM.pdf","")
    date_time = date_time + "T07:00:00.00+05:30"
    return date_time

def get_country_data(file_name):
    data_file = archive_folder_path + file_name
    csv_file_name = file_name +"_vaccine_country.csv"
    #print(data_file)
    s = subprocess.call(["tabula-java","-a", "72.542,11.904,145.457,575.131", "-p", "1", data_file ,">",csv_file_name])
    file = open(csv_file_name)    
    csvreader = csv.reader(file)
    report_time = get_datetime(file_name)
    data = {}
    data["_id"] = report_time +"|vaccinations"
    data["report_time"] = report_time

    if file_name in country_datarow_exceptions :
        return data
    else:
        pass

    rows = []
    row_num = 1
    data_row = []
    for row in csvreader:
        print(row)
        rows.append(row)
    file.close()

    data_row = None
    print(len(rows))    
    if "2021-02-25" in report_time or "2021-02-28" in report_time :
        data_row = rows[0]
    elif "2021-02-26" in report_time or "2021-02-27" in report_time :
        data_row = rows[1]
    elif report_time in country_datarow_exceptions:
        data_row = rows[country_datarow_exceptions[report_time]]
    elif report_time > "2021-07-03":
        data_row = rows[2]
    elif len(rows) == 3:
        data_row = rows[2]
    elif len(rows) > 3:
        data_row = rows[3]
     
    print("data_row", data_row)   



    start = 1

    if "2021-02-25" in report_time:
        start = 3
    elif "2021-02-26" in report_time or "2021-02-27" in report_time or "2021-02-28" in report_time:
        start = 2
    elif len(data_row) > 3:
        start = 1
    else:
        start = 0
    
    print("Starting at", start)

    data["1stdose"] = int(data_row[start].replace(",",""))
    data["2nddose"] = int(data_row[start+1].replace(",",""))
    data["total"] = int(data_row[start+2].replace(",",""))
    data["source"] = "mohfw"
    data["type"] = "vaccinations"
    return data


# def get_state_data(file_name):
#     print(s) 



def parse_data(file_name):
    print(get_country_data(file_name))

def parse_all_again():
    only_files = ([f for f in listdir(archive_folder_path) if isfile(join(archive_folder_path, f))])
    only_files.sort()
    for file_name in only_files:
        report_time = get_datetime(file_name)
        print(report_time)
        parse_data(file_name)


if __name__ == "__main__":
    #parse_all_again()
    parse_data(file_name="2021-09-20-at-07-00-AM.pdf")
