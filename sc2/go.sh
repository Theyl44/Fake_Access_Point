#! /usr/bin/env bash 

echo "[*] Create AP"
sudo hostapd hostapd.conf -B 

echo "[*] Start dhcp server"
sudo service isc-dhcp-server start

echo "[*] start listening traffic"
sudo tshark -i wlan1 -w ../saves_pcap/test.pcap -q &
