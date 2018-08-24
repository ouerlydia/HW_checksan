#!/usr/bin/python2.7
#-*- coding: utf-8 -*-*
import sys
import re
import os
import getopt
sys.path.append("..")
from HW_checksan.ucs import Ucs
from HW_checksan.nexus import Nexus
from HW_checksan.netapp import Netapp

global BLACK
global RED
global GREEN
		
BLACK = '\x1b[30m' # ANSI black font color.
RED = '\x1b[31m' # ANSI red font color.
GREEN = '\x1b[32m' # ANSI green font color.

def usage():
	print("""Usage:  HW_checksan.py [-h] netapp nexsus1 nexsus2 ucs...

Check FCoE SAN configuration consistency between UCS, Nexus, and NetApp 

  -h: display this help and exit
  netapp: netapp data  filename; contains the following tree commands outputs 
	clust01::> network interface show -data-protocol fcp -fields wwpn
	clust01::> lun igroup show -fields initiator
	clust01::> lun mapping show -fields igroup
  nexus1: Nexus 1 configuration filename; "show running-config" output 
  nexus2: Nexus 2 configuration filename; "show running-config" output 
  ucs: Ucs all configuration backup file (XML)

  Must outputs lines use the following format : 
   Status  Source 1 / Source 2 : data Source 1 *** data Source 2 """)


def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h")
	except getopt.GetoptError as err:
		print str(err)  
		usage()
		sys.exit(2)
	for o, a in opts:
		if o == "-h":
			usage()
			sys.exit()

	if len(args) < 4 :  # (1 NetApp + 2 Nexus + 1 UCS au moins)
		print ("Error  Invalid number of arguments " + str(len(args)) + ", expected 4 or more " ) 
		usage()
		sys.exit(2)

	netAppFileName = args[0]
	nexus1FileName = args[1]
	nexus2FileName = args[2]
	for ucsFileName in args[3:]:
		netapp= Netapp(netAppFileName)
		nexus1= Nexus(nexus1FileName,netapp)
		nexus2= Nexus(nexus2FileName,netapp)
		ucs= Ucs(ucsFileName,nexus1,nexus2)
		ucs.Check()
		
		
if __name__ == "__main__":
	main()
	 

   
   
