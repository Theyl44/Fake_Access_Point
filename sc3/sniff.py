#!/usr/bin/env python
from scapy.all import *

def print_probe_req(): 
    nb = 0 
    print("\n----------PROBE REQ------------\n")
    print("num ssid : destination address -> source address")
    for i in tab :
        print(str(nb)+ " "+ i)
        nb +=1 
    print("\n-----------------------------------\n")



mac_AP = "b6:7d:47:52:47:d9" #CAPTIVE PORTAL 
mac_iphone = "80:b0:3d:45:25:a4"
mac_wlan0 = "dc:a6:32:41:3f:63" 
mac_wlan1 = "00:c0:ca:aa:e0:b3" #ALFA
test = "ff:ff:ff:ff:ff:ff"


recipients_mac_adress= mac_AP
your_mac_adress= mac_iphone



interface = 'wlan1'
tab = []
channel = chr(1)

def send_probe_request(ssid):
    frame= RadioTap()\
           /Dot11(type=0, subtype=4, addr1=recipients_mac_adress, addr2=your_mac_adress, addr3= recipients_mac_adress)\
           /Dot11ProbeReq()\
           /Dot11Elt(ID='SSID', info=ssid)\
           /Dot11Elt(ID='Rates', info='\x82\x84\x8b\x96\x0c\x12\x18')\
           /Dot11Elt(ID='ESRates', info='\x30\x48\x60\x6c')\
           /Dot11Elt(ID='DSset', info=channel)
    answer = sendp(frame, iface=interface,verbose=False)
    
def send_probe_response(ssid):
    frame= RadioTap()\
           /Dot11(type=0, subtype=5, addr1=recipients_mac_adress, addr2=your_mac_adress, addr3= recipients_mac_adress)\
           /Dot11ProbeResp()\
           /Dot11Elt(ID='SSID', info=ssid)\
           /Dot11Elt(ID='Rates', info='\x82\x84\x8b\x96\x0c\x12\x18')\
           /Dot11Elt(ID='ESRates', info='\x30\x48\x60\x6c')\
           /Dot11Elt(ID='DSset', info=channel)
    answer = sendp(frame, iface=interface, verbose=False)
    
def connection_to_ap(ssid):
    ALGO_OPEN_AUTH = 0  # open authentication mode
    START_SEQNUM = 1  # sequence number
     
    #authentication
    frame1 = RadioTap()\
          /Dot11(type=0, subtype=11, addr1=recipients_mac_adress, addr2=your_mac_adress, addr3=recipients_mac_adress)\
          /Dot11Auth(algo=ALGO_OPEN_AUTH, seqnum=START_SEQNUM)
    answer = sendp(frame1, iface=interface, verbose=False)
     
    #association
    frame2 = RadioTap()\
          /Dot11(type=0, subtype=0, addr1=recipients_mac_adress, addr2=your_mac_adress, addr3=recipients_mac_adress)\
          /Dot11AssoReq()\
          /Dot11Elt(ID='SSID', info=ssid)\
          /Dot11Elt(ID='Rates', info='\x82\x84\x8b\x96\x0c\x12\x18')\
          /Dot11Elt(ID='ESRates', info='\x30\x48\x60\x6c')
    answer = sendp(frame2, iface=interface, verbose=False)
    
    
def find_probe_req(packet):
    ssid = packet.info.decode('utf-8')
    string = ssid+ " : \t" + str(packet.addr1) + " -> \t" + str(packet.addr2)
    if packet.info:
        print(ssid)
        if string not in tab :
            tab.append(string)
            #print(ssid)
        #send_probe_response(ssid+"LOPEZ")
#        if ssid == "Captive_Portal":
#            print("try to connect to captive_portal : " + str(packet.addr2))
#            send_probe_response(ssid)
#            connection_to_ap(ssid)

sniff(iface=interface, count=1000, lfilter=lambda p: Dot11ProbeReq in p, prn=find_probe_req)
print_probe_req()
# sniff(iface="wlan0", lfilter=lambda p: Dot11ProbeResp in p, prn=find_probe_resp)

#test probe_request
#for i in range(200):
#    send_probe_request("LOPEZ")
    
#test sniff packet réseaux
#sniff(iface="wlan1", lfilter=lambda p: Dot11Elt in p, prn=lambda x: x.show)





