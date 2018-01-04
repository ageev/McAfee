
# https://epo.network.canon-europe.com:8443/remote/core.help

import mcafee
import os
import sys
import getopt

SERVER = 'epo'
USERNAME = ''
PASSWORD = ''

TAG_NAME = "Scanning disabled"

def main(argv):
    global epo, verbose
    epo = mcafee.client(SERVER, '8443', USERNAME, PASSWORD)
    filename = ""
    remove_tag = False
    verbose = False
    wake_up_agent = False

#step 1. Read cli arguments 
    try:
        opts, args = getopt.getopt(argv, "hi:rwv", ["filename="])
    except getopt.GetoptError:
        print("mcafee_apply_tag.py -i <input file> [-r, remove tag]")
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == "-h":
            print("mcafee_apply_tag.py -i <input file>")
            print("This script allows to assign/remove tags")
            print("-i <file>    import file with hostnames")
            print("-r   remove tag instead")
            print("-v   verbose output")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            filename = arg
        elif opt in ("-r", "--remove"):
            remove_tag = True
        elif opt == "-v":
            verbose = True
        elif opt == "-w":
            wake_up_agent = True

    cis = (line.rstrip('\n') for line in open(filename))

    if remove_tag:
        for ci in cis:
            epo.system.clearTag(ci, TAG_NAME)
            print("Tag /"+TAG_NAME+"/ removed from "+ci)
    else:
        for ci in cis:
            epo.system.applyTag(ci, TAG_NAME)
            print("Tag /"+TAG_NAME+"/ assigned to "+ci)

    # wake up agents
    if wake_up_agent:
        for ci in cis:
            epo.system.wakeupAgent(ci, '', '', '', 'True')
        print("Wake-up call sent")

main(sys.argv[1:])