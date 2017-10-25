import mcafee
import os
import sys
import getopt

SERVER = 'epo'
USERNAME = ''
PASSWORD = ''
CHECKED_STOCK = "checked_stock.txt" #this file is used to store machines which exist in ePo

def main(argv):
	global epo, verbose
	epo = mcafee.client(SERVER, '8443', USERNAME, PASSWORD)
	check_exists = True
	delete_hosts = False
	verbose = False

#step 1. Read cli arguments 


	try:
		opts, args = getopt.getopt(argv, "hi:crv", ["filename="])
	except getopt.GetoptError:
		print("delstock.py -i <input file> -c [don't check if exists] -r [check and remove]")
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == "-h":
			print("delstock.py -i <input file>")
			print("THis script allows to remove unneeded machines from ePo")
			print("-i <file>	import file with hostnames")
			print("-c 	don't check if hosts exist")
			print("-r 	remove hostnames from ePo")
			print("-v 	verbose output")
			sys.exit()
		elif opt in ("-i", "--ifile"):
			filename = arg
		elif opt in ("-c", "--check"):
			check_exists = False
		elif opt in ("-r", "--remove"):
			delete_hosts = True
		elif opt == "-v":
			verbose = True


#step 2. Read the file to list and split new line
	stock = (line.rstrip('\n') for line in open(filename))

#step 3. Delete systems from ePo OR just check them
	if check_exists:
		open(CHECKED_STOCK, 'w').close() #clears CHECKED_STOCK file
		check(stock)
		if delete_hosts:
			hosts = (line.rstrip('\n') for line in open(CHECKED_STOCK))
	else:
		if delete_hosts:
			hosts = (line.rstrip('\n') for line in open(filename))

#step 4. Delete hosts
	delete(hosts)

def check(stock):
	for host in stock:
		if verbose:
			print('Checking ' + host)
		if epo.system.find(host):
			print(host + " exists in ePo")
			file = open(CHECKED_STOCK, "a")  # open file and append logs. write will clear the file
			file.write(host + "\n")
			file.close()

def delete(hosts):
	for host in hosts:
		epo.system.delete(host)
		print(host + ' should be deleted.')

main(sys.argv[1:])