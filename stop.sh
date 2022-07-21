#! /usr/bin/env bash 

sudo ps aux | grep dns | awk '{ print $2 }' | xargs kill  
#sudo ps aux | grep hostapd | awk '{ print $2 }' | xargs kill 
sudo killall hostapd 2>/dev/null
sudo killall tshark 2>/dev/null
sudo systemctl stop  isc-dhcp-server.service
sudo rm /var/www/cred.txt
sudo touch /var/www/cred.txt
sudo chmod 646 /var/www/cred.txt
echo "Processes stopped.."
