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

    try:
        opts, args = getopt.getopt(argv, "hi:", ["filename="])
    except getopt.GetoptError:
        print("delstock.py -i <input file>")
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == "-h":
            print("delstock.py -i <input file>")
            print("This script will remove unneeded machines from ePo")
            print("-i <file>    import file with hostnames")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            filename = arg
    stock = (line.rstrip('\n') for line in open(filename))
    for host in stock:
        if epo.system.find(host):
            epo.system.delete(host)
            print(host + ' is deleted')

if __name__ == "__main__":
    main(sys.argv[1:])