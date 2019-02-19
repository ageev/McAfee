import mcafee
import os
import sys
import getopt

SERVER = 'epo'
USERNAME = ''
PASSWORD = ''
input_filename = "win10pcs.csv" #this file is used to store existing machines in ePo
output_filename = "not_in_epo.csv"

def main():
    global epo
    epo = mcafee.client(SERVER, '8443', USERNAME, PASSWORD)
    systems = (line.rstrip('\n') for line in open(input_filename))
    for host in systems:
        if not epo.system.find(host):
            print(host + " doesn't exist in ePo")
            file = open(output_filename, "a")  # open file and append logs. write will clear the file
            file.write(host + "\n")
        else:
            print(host + " is in ePo")
main()