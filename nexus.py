#!/usr/bin/python2.7
#-*- coding: utf-8 -*-
import re
import sys
import os


class Nexus (object):

		global BLACK
		global RED
		global GREEN
		
		BLACK = '\x1b[30m' # ANSI black font color.
		RED = '\x1b[31m' # ANSI red font color.
		GREEN = '\x1b[32m' # ANSI green font color.

		def __init__(self, file_name,netapp):
				self.nexus= open( file_name,"r")  
				self.netapp=netapp # instance de Netapp 
				self.listnexus= list() #  liste des lignes du fichier nexus 
				self.zones=list() # liste des lignes de la  zoneset  du fichier nexus 
				self.inTagNexus=list() # liste des lignes d'une  zone 

				Nexus.GetNexusList(self)
				
		# charge le fichier nexus dans une liste 		
		def GetNexusList(self):
			del self.listnexus [:]
			self.listnexus = self.nexus.read().splitlines()
			self.nexus.close()
		
		# chaege les lignes d'une zone 
		def GetZonesMembers(self,sp,vHBA,vsanId): 
				del self.inTagNexus[:]
				j=0
				s="false" # résultat de la recherche de la zone
				for j in range (len(self.listnexus)):					
					if re.search('^zone name '+ sp +'-'+vHBA+' vsan '+ vsanId , self.listnexus [j]) is not None:
						 u=self.listnexus.index(self.listnexus[j])
						 s="true"
						 break

				if s=="true" : # zone found 
					i=0
					for i in range(u+1, len(self.listnexus)):
						if (self.listnexus[i] != ''): 
						
							self.inTagNexus.append(self.listnexus[i]) 
							
						else : # ligne vide fin zone
							break 
				else : # zone not found 
					return "false"
				return "true"

		# vérifie la déclaration d'un VSAN
		def CheckVsan(self, vsanId, fcoe):
				j=0
				b="false"
				for j in  range(len(fcoe)): 
					i=0
					for i in range(len(self.listnexus)): 
						if (re.search( '^vlan '  + fcoe[j] , self.listnexus[i] ) ) is not None:
								 u=self.listnexus.index(self.listnexus[i])
								 if(re.search('  fcoe vsan '+ vsanId [j], self.listnexus[u+1] ) ) is not None:
										b="true"
										msg= GREEN+ "ok" + BLACK + ',' + fcoe[j] + ':' +vsanId [j]
					if (b=="false") :
						msg= RED+ "NOK"  + ',' + fcoe[j] + ':' +vsanId [j] + ' Not Found ' + BLACK 

				return [[b,msg]]

		# vérifie la configuration d'un initiator depuis ucs, nexus, netapp 
		def checkInitiator(self,sp,vHBA,vsanId,Initiator):
			# vérifie l'existance de la zone pour le service profile 
			if (Nexus.GetZonesMembers(self,sp,vHBA,vsanId)=="false") : 
					return [["false", RED + 'NOK zone Not Found ' + sp+'-'+vHBA+ BLACK ]]
			else : 
				b="false"
				status = list()
				for i in range (len(self.inTagNexus)):
					if (re.search(Initiator.lower(), self.inTagNexus [i])): 
						b="true"
						msg=GREEN+ "ok" + BLACK+ ' Ucs (Initiator) / Zone (Initiator) '+ sp +' '+vHBA
						status.append([b,msg])

						status.extend(self.netapp.CheckIgroup(sp,Initiator))
						status.extend(self.netapp.CheckLUN (sp))
						break
																		
				if(b=="false"): 
									msg=RED+ "NOK"  +' Ucs (Initiator) / Zone (Initiator) : [' + sp + ']-'+ vHBA+' vsan ]-'+Initiator.lower()+ ' *** ' + 'Not Found' + BLACK
									status.append([b,msg])
				return status

		# vérifie la configuration d'un target depuis ucs, nexus, netapp 
		def checkTarget(self,sp,vHBA,vsanId,target,bootPolicyName):
				 status=list()
				 b="false"	
				 msg=""			
				 for j in range (len(self.inTagNexus)):
							if (re.search(target.lower(), self.inTagNexus [j])): 
									b="true"
									msg =GREEN+ "ok" + BLACK+" Target / Zone                 : [" + target + "] *** " + self.inTagNexus [j] + self.inTagNexus [j+1]
									status.append([b,msg])

									status.extend(self.netapp.CheckInterface(self.inTagNexus[j],self.inTagNexus[j+1]))
									break

				 if (b=="false"):									
									msg=RED+ "NOK"  +" Target / Zone                 : [" + target + "] " + bootPolicyName + " *** " + 'Not Found'+ BLACK
									status.append([b,msg])
				 return status
		
		# charge ls lignes de la zoneset d'un vsan id donné 
		def GetZones (self,vsanId) :
				u=0
				i=0 
				del self.zones [:]
				for i in range(len(self.listnexus)):
						if (re.search( '^zoneset name nfv[0-9]{2} vsan '+vsanId, self.listnexus [i])) is not None: 
							u=self.listnexus.index(self.listnexus [i])
				i=0    
				for i in range(u,len(self.listnexus)):       
						if (re.search( "    member",self.listnexus[i])) is not None :
								self.zones.append(self.listnexus[i])
							
		# vérifie qu'une zone associée à un service profile est membre de la zoneset	
		def checkZone (self, sp,vHBA,vsanId) : 
				 self.GetZones(vsanId) # à optimiser
				 b="false"
				 for j in range(len(self.zones)):													
					 if re.search('    member '+sp+'-'+ vHBA, self.zones[j]) is not None:							
							msg=GREEN+ "ok" + BLACK +' SP / Zoneset                      : '+sp + ' ' + vHBA
							b= "true"
							break
																																			 
				 if (b=="false"): 																				
							msg= RED+ "NOK"  +' SP / Zoneset                       : '+sp + ' ' + vHBA + ' *** Zone not member of zoneset '+ BLACK
				 return[[b,msg]]
			 
															
																 
																	
																	
	
			

