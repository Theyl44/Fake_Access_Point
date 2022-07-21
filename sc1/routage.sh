#! /usr/bin/env bash 
sudo ifconfig wlan1 down 
sudo iwconfig wlan1 mode monitor
sudo ifconfig wlan1 up

ifconfig wlan1 up 192.168.1.1 netmask 255.255.255.0
route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1

sudo iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE
sudo iptables --append FORWARD --in-interface wlan1 -j ACCEPT
#sudo iptables -P FORWARD ACCEPT #pour les regles dockers

sudo bash -c "echo 1 > /proc/sys/net/ipv4/ip_forward" 
