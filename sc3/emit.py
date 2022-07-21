#!/usr/bin/env python
from scapy.all import *
 
recipients_mac_adress= 'ff:ff:ff:ff:ff:ff'
your_mac_adress= '02:26:12:43:37:f5'
ssid = 'Sc45y + W1F1'
channel = chr(1)
interface = 'wlan1'
 
frame= RadioTap()\
      /Dot11(type=0, subtype=4, addr1=recipients_mac_adress, addr2=your_mac_adress, addr3= recipients_mac_adress)\
      /Dot11ProbeReq()\
      /Dot11Elt(ID='SSID', info=ssid)\
      /Dot11Elt(ID='Rates', info='\x82\x84\x8b\x96\x0c\x12\x18')\
      /Dot11Elt(ID='ESRates', info='\x30\x48\x60\x6c')\
      /Dot11Elt(ID='DSset', info=channel)

answer = srp1(frame, iface=interface)