#!/usr/bin/env python

# this script will run ePo query and output data to file
# 06.12.2018 Artem Ageev

import os, requests
import sys
import getopt
import json
import datetime

# supress self-signed certificate warning 
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

SERVER = 'epo'
QUERYID = '242'
USERNAME = ''
PASSWORD = ''

# check OS and set path accordingly. Needed only for easy development 
if os.path.exists('C:/Windows'):
    CSVFILENAME = "/logs_ENS/" + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + ".csv"
    REPORTFILENAME = "data_ENS.csv"
else:
    CSVFILENAME = "/media/logs_ENS/" + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + ".csv"
    REPORTFILENAME = "/media/data_ENS.csv"

'''
EXAMPLE:
curl: https://<ip>:8443/remote/core.executeQuery?queryId=777:output=json
curl: https://<ip>:8443/remote/core.help?command=core.executeQuery
'''

def main():
    url = 'https://' + SERVER + ":8443/remote/core.executeQuery?queryId=" + QUERYID + "&:output=json"
    r = requests.get(url, auth=(USERNAME, PASSWORD), verify=False)
    d = json.loads(r.text[5:]) #skip first non-json text

    compliant = 0
    incompliant = 0
    total = 0
    compliance = 0

    for i in d:
        if i['AM_CustomProps.AVCMGRbComplianceStatus'] == 1:
            compliant = i['count']
        if i['AM_CustomProps.AVCMGRbComplianceStatus'] == 0:
            incompliant = i['count']
    total = compliant + incompliant
    compliance = round((compliant * 100 ) / total)

    with open(REPORTFILENAME, 'a') as f:
        f.write(datetime.datetime.now().strftime("%Y-%m-%d") + ";" + str(compliance) + ";" + str(total) + ";" + str(compliant) + ";" + str(incompliant) + ";" + "\n")

if __name__ == '__main__':  
    main()
