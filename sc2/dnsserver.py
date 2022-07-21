#!/usr/bin/env python3
import socket, glob, json, os, subprocess
import dns.name
import dns.resolver
import time, signal
from contextlib import contextmanager

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = "\033[97m"

port = 53
ip = '192.168.1.1'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

def signal_handler(signum, frame):
	print("rip")

def fillzone(domain, restricted):
	var = {'portail.captif-u.com.': {
	'$origin': 'portail.captif-u.com.', 
	'$ttl': 3600, 
	'soa': {'mname': 'portail.captif-u.com.', 'rname': 'admin.portail.captif-u.com.', 'serial': '1', 'refresh': 3600, 'retry': 600, 'expire': 604800, 'minimum': 86400}, 
	'ns': [{'host': 'portail.captif-u.com.'}], 
	'a': [{'name': '@', 'ttl': 400, 'value': '192.168.1.1'}]}}
	if restricted == 1:
		return var
	else:
		n = dns.name.from_text(domain)

		var = {'portail.captif-u.com.': {
			'$origin': 'portail.captif-u.com.', 
			'$ttl': 3600, 
			'soa': {'mname': 'portail.captif-u.com.', 'rname': 'admin.portail.captif-u.com.', 'serial': '1', 'refresh': 3600, 'retry': 600, 'expire': 604800, 'minimum': 86400}, 
			'ns': [{'host': 'portail.captif-u.com.'}], 
			'a': [{'name': '@', 'ttl': 400, 'value': '192.168.1.1'}]}, }
		var['test.com.'] = {'$origin' : str(n), '$ttl' : 3600}
	
		SOA = 0
		try:
			answer = dns.resolver.resolve(n,'SOA')
		except dns.resolver.NoAnswer:
			SOA = 1
			pass
		except dns.resolver.NoNameservers:
			SOA = 1
			pass
		except dns.resolver.LifetimeTimeout:
			SOA = 1
			pass
		except dns.resolver.NXDOMAIN:
			SOA = 1
			pass

		if SOA == 0:
			soa = str(answer[0])
			splited = soa.split()
			var['test.com.']['soa'] = {'mname': splited[0], 'rname': splited[1], 'serial': splited[2], 'refresh': int(splited[3]), 'retry': int(splited[4]), 'expire': int(splited[5]), 'minimum': int(splited[6])}
		
		NS = 0
		try:
			answer = dns.resolver.resolve(n,'NS')
		except dns.resolver.NoAnswer:
			NS = 1
			pass
		except dns.resolver.NoNameservers:
			NS = 1
			pass
		except dns.resolver.LifetimeTimeout:
			NS = 1
			pass
		except dns.resolver.NXDOMAIN:
			NS = 1
			pass
		
		if NS == 0:
			var['test.com.']['ns'] = []
			for data in answer:
				var['test.com.']['ns'].append({'host': str(data)})

		A = 0
		try:
			answer = dns.resolver.resolve(n,'A')
		except dns.resolver.NoAnswer:
			A = 1
			pass
		except dns.resolver.NoNameservers:
			A = 1
			pass
		except dns.resolver.LifetimeTimeout:
			A = 1
			pass
		except dns.resolver.NXDOMAIN:
			A = 1
			pass
			
		if A == 0:
			var['test.com.']['a'] = []
			for data in answer:
				var['test.com.']['a'].append({'name': '@', 'ttl': 400, 'value': str(data)})
			return var
		else:
			return 0

def getflags(flags):

	byte1 = bytes(flags[:1])
	byte2 = bytes(flags[1:2])
	rflags = ''
	QR = '1'
	OPCODE = ''
	for bit in range(1,5):
		OPCODE += str(ord(byte1)&(1<<bit))

	AA = '1'
	TC = '0'
	RD = '0'
	RA = '0'
	Z = '000'
	RCODE = '0000'

	return int(QR+OPCODE+AA+TC+RD, 2).to_bytes(1, byteorder='big')+int(RA+Z+RCODE, 2).to_bytes(1, byteorder='big')

def getquestiondomain(data):

	state = 0
	expectedlength = 0
	domainstring = ''
	domainparts = []
	x = 0
	y = 0
	for byte in data:
		if state == 1:
			if byte != 0:
				domainstring += chr(byte)
			x += 1
			if x == expectedlength:
				domainparts.append(domainstring)
				domainstring = ''
				state = 0
				x = 0
			if byte == 0:
				domainparts.append(domainstring)
				break
		else:
			state = 1
			expectedlength = byte
		y += 1
	questiontype = data[y:y+2]
	return (domainparts, questiontype)

def getzone(domain, restricted):
	global zonedata

	if restricted == 1:
		zone_name = "portail.captif-u.com."
	else:
		zone_name = "test.com."

	return zonedata[zone_name]
	
def getrecs(data, restricted):
	domain, questiontype = getquestiondomain(data)
	qt = 'a'
	zone = getzone(domain, restricted)
	return (zone[qt], qt, domain)

def buildquestion(domainname, rectype):
	qbytes = b''

	for part in domainname:
		length = len(part)
		qbytes += bytes([length])

		for char in part:
			qbytes += ord(char).to_bytes(1, byteorder='big')

	if rectype == 'a':
		qbytes += (1).to_bytes(2, byteorder='big')

	qbytes += (1).to_bytes(2, byteorder='big')

	return qbytes

def rectobytes(domainname, rectype, recttl, recval):

	rbytes = b'\xc0\x0c'

	if rectype == 'a':
		rbytes = rbytes + bytes([0]) + bytes([1])

	rbytes = rbytes + bytes([0]) + bytes([1])
	rbytes += int(recttl).to_bytes(4, byteorder='big')

	if rectype == 'a':
		rbytes = rbytes + bytes([0]) + bytes([4])

		for part in recval.split('.'):
			rbytes += bytes([int(part)])
	return rbytes

def buildresponse(data, restricted):

	TransactionID = data[:2]
	Flags = getflags(data[2:4])
	QDCOUNT = b'\x00\x01'
	ANCOUNT = len(getrecs(data[12:], restricted)[0]).to_bytes(2, byteorder='big')
	NSCOUNT = (0).to_bytes(2, byteorder='big')
	ARCOUNT = (0).to_bytes(2, byteorder='big')
	dnsheader = TransactionID+Flags+QDCOUNT+ANCOUNT+NSCOUNT+ARCOUNT
	dnsbody = b''
	records, rectype, domainname = getrecs(data[12:], restricted)

	dnsquestion = buildquestion(domainname, rectype)
	for record in records:
		dnsbody += rectobytes(domainname, rectype, record["ttl"], record["value"])

	return dnsheader + dnsquestion + dnsbody

def refresh(tab):
	subprocess.run("clear", shell=True)
	print("\n")
	print(bcolors.OKCYAN +"██   ██ ██    ██  ████  ██   █ █████  █████ █████ █████  ██   ██ █████ █████  ")
	print(bcolors.OKCYAN +"███ ███  ██  ██   █   █ ███  █ █      █     █     █   ██ ██   ██ █     █   ██ ")
	print(bcolors.OKCYAN +"█ ███ █   ████    █   █ █ ██ █ █████  █████ ████  █████  ██   ██ ████  █████  ")
	print(bcolors.OKCYAN +"█  █  █    ██     █   █ █  ███     █      █ █     █   ██  ██ ██  █     █   ██ ")
	print(bcolors.OKCYAN +"█     █    ██     ████  █   ██ █████  █████ █████ █   ██   ███   █████ █   ██ ")
	print(bcolors.WHITE + bcolors.BOLD+"Personnes connectées ["+str(len(tab))+"]\n")

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
       
i = 0
good = []
refresh(good)
visited=[]

while 1:
	width, height = os.get_terminal_size()
	height = height - 11
	goback = "\033[A" * height
	try:
		with time_limit(2):
			data, addr = sock.recvfrom(512)
			timedout = 0
	except TimeoutException as e:
		timedout = 1

	if timedout == 0:
		name, temp = getquestiondomain(data[12:])
		if addr[0] not in good:
			ip3 = addr[0].split(".")
			final = "."+ip3[3]+"\n"
			with open('/var/www/html/.htaccess') as f:
				if final in f.read():
					good.append(addr[0])
					visited.append([])    
		if addr[0]!="192.168.1.1" and "zscaler" not in name and "sentinelone" not in name and "zscloud" not in name:		
			final =""
			tot = len(name)
			count = 1
			#concaténation du nom de domaine complet
			for single in name:
				final += single
				if count < tot - 1:
					final += "."
				count += 1
			#check si l'IP qui envoie une query s'est connectée au Portail Captif
			if addr[0] in good:
				zonedata = fillzone(final,0)
				if final != "portail.captif-u.com":
					if zonedata != 0:
						if i != height:
							if "controller" not in name and "arpa" not in name:
								print(bcolors.OKGREEN + addr[0]+" : "+final)
								i += 1
								index = good.index(addr[0])
								if name[-3] not in visited[index]:
									visited[index].append(name[-3])
						else:
							refresh(good)
							file = open("logz.txt", "w+")
							file.write(str(good))
							file.write("\n")
							file.write(str(visited))
							file.close()
							i = 1
							if "controller" not in name and "arpa" not in name:
								print(bcolors.OKGREEN + addr[0]+" : "+final)
								index = good.index(addr[0])
								if name[-3] not in visited[index]:
									visited[index].append(name[-3])
						r = buildresponse(data, 0)
						sock.sendto(r, addr)
					else:
						if i != height:
							print((bcolors.OKGREEN+addr[0]+" : "),(bcolors.FAIL+final))
							i += 1
						else:
							refresh(good)
							print(bcolors.OKGREEN+addr[0]+" : " + bcolors.FAIL+final)
							i = 1
				else:
					if zonedata != 0:
						r = buildresponse(data, 1)
						sock.sendto(r, addr)
			else:
				if i != height:
					print(bcolors.WARNING + addr[0]+" : Not connected, redirected")
					i += 1
				else:
					refresh(good)
					print(bcolors.WARNING + addr[0]+" : Not connected, redirected")
					i = 1
				zonedata = fillzone(final,1)
				if zonedata != 0:
					r = buildresponse(data, 1)
					sock.sendto(r, addr)
