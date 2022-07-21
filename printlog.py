import os, subprocess
import sys

f = open("/var/www/log.txt", "r")
total = ""
search=""

if len(sys.argv) == 2:
	search=sys.argv[1]
	
print(f"{'Date' : <20}{'IP' : ^20}{'MAC' : ^20}{'Login' : ^20}{'Password' : ^20}{'User Agent' : >20}")
date=[]
ip=[]
mac=[]
login=[]
pwd=[]
ua=[]

if search == "":
	for i in f.readlines() : 
		tab = i.split("|")

		value = tab[0].split(" : ")
		value[0] = value[0].replace(" ","")
		date.append(value[0])

		value = tab[1].split(" : ")
		value[1] = value[1].replace(" ","")
		ip.append(value[1])

		value = tab[2].split(" : ")
		value[1] = value[1].replace(" ","")
		mac.append(value[1])

		value = tab[3].split(" : ")
		value[1] = value[1].replace(" ","")
		login.append(value[1])

		value = tab[4].split(" : ")
		pwd.append(value[1])

		value = tab[5].split(" : ")
		value[1] = value[1].replace("\n","")
		ua.append(value[1])
			
	for i in range(0, len(date)):
		print(f"{date[i] : <20}{ip[i] : ^20}{mac[i] : ^20}{login[i] : ^20}{pwd[i] : ^20}{ua[i] : >20}")
else:
	found = 0
	list_trouve = []

	for i in f.readlines() : 
		if search.lower() in i.lower() : 
			list_trouve.append(i)
			found += 1

	if found != 0 :
		for i in list_trouve : 
			tab = i.split("|")
			
			value = tab[0].split(" : ")
			value[0] = value[0].replace(" ","")
			date.append(value[0])

			value = tab[1].split(" : ")
			value[1] = value[1].replace(" ","")
			ip.append(value[1])

			value = tab[2].split(" : ")
			value[1] = value[1].replace(" ","")
			mac.append(value[1])

			value = tab[3].split(" : ")
			value[1] = value[1].replace(" ","")
			login.append(value[1])

			value = tab[4].split(" : ")
			pwd.append(value[1])

			value = tab[5].split(" : ")
			value[1] = value[1].replace("\n","")
			ua.append(value[1])
			
		for i in range(0, len(date)):
			print(f"{date[i] : <20}{ip[i] : ^20}{mac[i] : ^20}{login[i] : ^20}{pwd[i] : ^20}{ua[i] : >20}")
	else: 
		print("Pas de résultat pour votre recherche...")

#if "g" not in arg:
#	for i in f.readlines() : 
#		tab = i.split("|")
#		if "d" in arg or "a" in arg:
#			value = tab[0].split(" : ")
#			value[0] = value[0].replace(" ","")
#			total+="\t"
#		if "i" in arg or "a" in arg:
#			value = tab[1].split(" : ")
#			value[1] = value[1].replace(" ","")
#			total+="\t"
#		if "m" in arg or "a" in arg:
#			value = tab[2].split(" : ")
#			value[1] = value[1].replace(" ","")
#			total+="\t"
#		if "l" in arg or "a" in arg:
#			value = tab[3].split(" : ")
#			value[1] = value[1].replace(" ","")
#			total+="\t"
#		if "p" in arg or "a" in arg:
#			value = tab[4].split(" : ")
#			total+=value[1]
#			total+="\t"
#		if "u" in arg or "a" in arg:
#			value = tab[5].split(" : ")
#			value[1] = value[1].replace("\n","")
#			total+=value[1]
#			total+="\t"
#		print(total)
#		total=""
#else:
#	found = 0
#	list_trouve = []
#
#	for i in f.readlines() : 
#		if sys.argv[2].lower() in i.lower() : 
#			list_trouve.append(i)
#			found += 1
#
#	if found != 0 :
#		for i in list_trouve : 
#			tab = i.split("|")
#			if "d" in arg or "a" in arg:
#				value = tab[0].split(" : ")
#				value[0] = value[0].replace(" ","")
#				total+=value[0]
#				total+="\t"
#			if "i" in arg or "a" in arg:
#				value = tab[1].split(" : ")
#				value[1] = value[1].replace(" ","")
#				total+=value[1]
#				total+="\t"
#			if "m" in arg or "a" in arg:
#				value = tab[2].split(" : ")
#				value[1] = value[1].replace(" ","")
#				total+=value[1]
#				total+="\t"
#			if "l" in arg or "a" in arg:
#				value = tab[3].split(" : ")
#				value[1] = value[1].replace(" ","")
#				total+=value[1]
#				total+="\t"
#			if "p" in arg or "a" in arg:
#				value = tab[4].split(" : ")
#				total+=value[1]
#				total+="\t"
#			if "u" in arg or "a" in arg:
#				value = tab[5].split(" : ")
#				value[1] = value[1].replace("\n","")
#				total+=value[1]
#				total+="\t"
#			print(total)    
#			total=""
#	else: 
#		print("pas de résultat")
f.close()



