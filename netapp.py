#!/usr/bin/python2.7
#-*- coding: utf-8 -*-
import re
import sys
import os

class Netapp (object) :

	global BLACK
	global RED
	global GREEN

	BLACK = '\x1b[30m' # ANSI black font color.
	RED = '\x1b[31m' # ANSI red font color.
	GREEN = '\x1b[32m' # ANSI green font color.

	def __init__(self, file_name):
		self.netapp  =open( file_name,"r")  
		self.listnetapp= list() # liste des lignes du fichier netapp 
		self.listnetappInterface=list() # liste des lignes interfaces du netapp 
		self.listnetappIgroup=list() # liste des lignes Igroup 
		self.listnetappLUN=list() # liste des lignes  LUN 

		Netapp.GetNetappList(self) 
		Netapp.GetNetappInterfaces(self)
		Netapp.GetIgroup(self)
		Netapp.GetLUN(self)	
    
    # charge la liste des lignes du fichier 
	def GetNetappList (self):
		del self.listnetapp [:]
		self.listnetapp = self.netapp.read().splitlines()
		self.netapp.close()

    # charge la liste des lignes des interfaces 
	def GetNetappInterfaces (self):
		i=0
		for i in range(len(self.listnetapp)):
		  if (re.search( ' network interface show -data-protocol fcp -fields wwpn' , self.listnetapp[i] ) ) is not None:
			 u=self.listnetapp.index(self.listnetapp[i])
		i=0
		for i in range(u+3, len(self.listnetapp)):
			if (self.listnetapp[i] != ''):
				self.listnetappInterface.append(self.listnetapp[i]) 
			else :
			  break 

    # charge la liste des lignes Igroup
	def GetIgroup (self):
		  i=0
		  u=0
		  for i in range(len(self.listnetapp)):

			  if (re.search( 'lun igroup show -fields initiator' , self.listnetapp[i] ) ) is not None:
				 u=self.listnetapp.index(self.listnetapp[i])

		  i=0
		  for i in range(u+3, len(self.listnetapp)):
				if (self.listnetapp[i] != ''):
					
					self.listnetappIgroup.append(self.listnetapp[i])
					
				else :
				  break

    # charge la liste des lignes LUN 
	def GetLUN (self):
		i=0
		u=0
		for i in range(len(self.listnetapp)):
		  if (re.search( 'lun mapping show -fields igroup' , self.listnetapp[i] )) is not None: 
			 u=self.listnetapp.index(self.listnetapp[i])

		i=0
		for i in range(u+3, len(self.listnetapp)):
			
			if (self.listnetapp[i] != ''):
				self.listnetappLUN.append(self.listnetapp[i]) 
			else :
			  break
    
    # vérifie la configuration d'un initiator dans le Igroup associé à un service profile 
	def CheckIgroup(self,sp,initiator): 
		ch= str(sp)
		ch=ch.replace('-','_',1)					  
		b="false"
		i=0
		for i in range(len(self.listnetappIgroup)):
			e1=re.search(ch,self.listnetappIgroup[i])
			e2=re.search( initiator.lower(),self.listnetappIgroup[i]) 
			if  (e1 is not None )  and (e2  is not None):
				msg=GREEN+'ok'+BLACK+' Zone (initiator) / Igroup     : '+ ch +' ' + initiator.lower() +  '   *** ' + self.listnetappIgroup[i]
				b="true"
				break
		if b=="false": 
				msg=RED+'NOK'+' Zone (initiator) / Igroup     : '+ ch +' '+ initiator.lower() +   '   *** ' + ' Not found '+BLACK
		return [[b,msg]]

    # vérifie la configuration d'un initator dans le LUN associé à un service profile 
	def CheckLUN (self,sp):
		ch= str(sp)
		ch=ch.replace('-','_',1) 
		r=0
		b="false"
		for r in range(len(self.listnetappLUN)): 
			e1=re.search('lun_'+ch,self.listnetappLUN[r])
			e2=re.search('ig_'+ch,self.listnetappLUN[r])
			if  (e1  is not None)  and (e2 is not None) :
				msg=GREEN+'ok'+BLACK+' Zone / LUN mapping            : ' + ch + '              *** ' + self.listnetappLUN[r]
				b="true"
				break		   
		if (b=="false"):
				msg= RED+'NOK'+' Zone / LUN mapping             : ' + ch + '              *** ' + self.listnetappLUN[r] +BLACK
		return [[b,msg]]

    # vérifie la configuration d'un target dans les interfaces [wwpn + device-alias : interface ]  
    # lif :  device-alias name exemple  "nfv05-svm99-FCoE-lif1" 
	def CheckInterface (self,target,lif): 
		# construction de "svm99-FCoE_lif01" à partir de [nfv05-svm99-FCoE-lif1] 
		ch= str(lif)
		ch=ch.replace('!','')
		ch=ch.replace('[','')
		ch=ch.replace(']','')
		ch= ch.split('-',1)
		chaine = ch[1]
		chaine=chaine.replace('-','_',2)
		chaine=chaine.replace('_','-',1)
		chaine= chaine[:14]+ '0'+ chaine[14:]
		
		tag=str(target)
		tag=tag.split(' ')
		
		i=0
		b="false"
		for i in range(len(self.listnetappInterface)):
		   m1= re.search( tag[len(tag)-1], self.listnetappInterface[i])
		   m2= re.search( chaine, self.listnetappInterface[i])
		   if (m1 is not None )  and (m2 is not None) : 
			  msg= '  \_'+GREEN+'ok'+BLACK+" Zone (target) / Interface : [" + target + "]-" + lif + " *** " + self.listnetappInterface[i]
			  b="true"
			  break
		if (b=="false"):
			msg= '  \_'+RED+'NOK'+" Zone (target) / Interface : [" + target + "]-" + lif + " *** " + 'Not found'+BLACK
		return [[b,msg]]




		
							
