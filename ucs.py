#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml import etree
import sys
import re
import os


class Ucs (object) : 

	global BLACK
	global RED
	global GREEN
		
	BLACK = '\x1b[30m' # ANSI black font color.
	RED = '\x1b[31m' # ANSI red font color.
	GREEN = '\x1b[32m' # ANSI green font color.

	def __init__(self, xml_file_name,nexus1,nexus2):
		self.tree  =etree.parse(xml_file_name)
		self.nexus1=nexus1 # nexus 1 filename
		self.nexus2=nexus2 # nexus 2 filename
		self.longSp= list() # site-pod-bl
		self.fcoe=list() # FcoE VLAN id list 
		self.vsanIds=list() # VSAN id list in the same order of the fcoe list 

		Ucs.GetVsan(self) 
		Ucs.GetServiceProfilNumber(self)

	# Chage les couples (fcoe VLAN id , vsan id) 		
	def GetVsan (self) : 

		for fcoeVlan in self.tree.xpath('/topRoot/fabricEp/fabricSanCloud/fabricFcSan/fabricVsan/@fcoeVlan'):
   
			for vsanId in self.tree.xpath('/topRoot/fabricEp/fabricSanCloud/fabricFcSan/fabricVsan[@fcoeVlan='+ fcoeVlan + ']/@id'):
				
				self.fcoe.append(fcoeVlan)
				self.vsanIds.append(vsanId)
		return [self.vsanIds,self.fcoe]

	# charge les services profiles 
	def GetServiceProfilNumber(self):
		spNames=self.tree.xpath('/topRoot/orgOrg/orgOrg/lsServer/@name')
		spNames.sort()
		for name in spNames:       
		  m=re.search("(site1|site2|site3|site4|site5)-nfv[0-9]{2}-bl[0-9]{4}", name)
		  if m is not None:
				ch=name.split("-",1)
				self.longSp.append(name) # site -nfv -bl			   
		  ch1=''
		  

	# affiche le vsan id pour une vHBA donnée  
	def GetVsanId(self,vHBA): # 
		if (vHBA=="vHBA-FIA"):
			i=0
			for i in range(len(self.vsanIds)):
			  if (re.search('^1' , self.vsanIds[i]) is not None) : 
				 return self.vsanIds[i]
		elif (vHBA=="vHBA-FIB"):
			i=0
			for i in range(len(self.vsanIds)):
			  if (re.search('^2' , self.vsanIds[i]) is not None ): 
				 return self.vsanIds[i]
		else: 
			raise ValueError ('Error  Vsan  unexpected vHBA :  '+ vHBA )

	# affiche  le bon nexus pour une vHba donnée 		
	def GetNexus(self,vHBA):  
		if (vHBA=="vHBA-FIA"):
				 return self.nexus1
		elif (vHBA=="vHBA-FIB"):
				 return self.nexus2
		else: 
			raise ValueError ('Error  Nexus  unexpected vHBA :  '+ vHBA )

	# vérifie un service profile et affiche le résultat sur stdout 		
	def CheckSp(self, longSp): 
		status=list()
		ch=longSp.split("-",1)
		sp=ch[1]  # nfv -bl
		target=list()
		vHBANames=self.tree.xpath('/topRoot/orgOrg/orgOrg/lsServer[@name="'+longSp+'"]/vnicFc/@name')
		vHBANames.sort() 
		for vHBAName in vHBANames:
			   nexus=self.GetNexus(vHBAName)
			   vsanId=self.GetVsanId(vHBAName)
			   for initiator  in self.tree.xpath('/topRoot/orgOrg/orgOrg/lsServer[@name="'+longSp+'"]/vnicFc[@name="'+vHBAName+'"]/@addr'):
				   
				   status.extend(nexus.checkInitiator(sp,vHBAName,vsanId,initiator))  
				   
				   for bootPolicyName in self.tree.xpath('/topRoot/orgOrg/orgOrg/lsServer[@name="'+longSp+'"]/@bootPolicyName'):				
						 if ( bootPolicyName == "PXE-SD"):  # amélioration : remplacer par  "si ne contient pas SAN "						 
							bootPolicyName= "PXE-SAN-svm99-01" # forçage vers bootpolicy SAN  pour la vérification postboot 
						 for wwn in self.tree.xpath('/topRoot/orgOrg/lsbootPolicy[@name="'+bootPolicyName+'"]/lsbootSan/lsbootSanCatSanImage[@vnicName="'+vHBAName+'"]/lsbootSanCatSanImagePath/@wwn'):           
							 status.extend(nexus.checkTarget(sp,vHBAName,vsanId,wwn,bootPolicyName)) 
			   status.extend( nexus.checkZone ( sp,vHBAName,vsanId))
		self.DupmSp(longSp,status)

	# affiche sur stdout  le status de la vérification d'un service profile 	
	def DupmSp(self, longSp, status):
		globalStatus="true"
		i=0
		for i in range(len(status)):
		   if (status[i][0]=="false"):
			  globalStatus="false"
			  break
		if (globalStatus=="true"):
		  print(GREEN + 'ok ' + BLACK + " >>> HW_checksan " + longSp)
		else:
		  print(RED + 'NOK '+ " >>> HW_checksan  " + longSp  + BLACK )
		  for i in range(len(status)):

		   print('  ' +status [i][1])

	# affiche sur stdout  le status de la vérification d'un  	
	def DupmVsan(self,statusVsan):
		globalStatusVsan="true"
		i=0
		for i in range(len(statusVsan)):
		   if (statusVsan[i][0]=="false"):
			  globalStatusVsan="false"
			  break
		if (globalStatusVsan=="true"):
		  print(GREEN + 'ok ' + BLACK + " >>> HW_checksan Vsan  ")
		else:
		  print(RED + 'NOK '+ " >>> HW_checksan Vsan  " + BLACK )
		  for i in range(len(statusVsan)):
		   print('  ' +statusVsan [i][1])

	# vérifie les déclarations des Vsans et l'ensemble des services profiles 
	def Check (self) :
		statusVsan=list()
		nexus=self.GetNexus("vHBA-FIA")
		statusVsan.extend(nexus.CheckVsan(self.vsanIds, self.fcoe))
		nexus=self.GetNexus("vHBA-FIB")
		statusVsan.extend(nexus.CheckVsan(self.vsanIds, self.fcoe))
		self.DupmVsan(statusVsan)
		i=0
		for i in range(len(self.longSp)):
		   self.CheckSp(self.longSp[i])

		print( 'Nombre de service profile de UCS : ' +  str(len(self.longSp)))
		  
		 

	
  
   




