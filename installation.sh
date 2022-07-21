#! /usr/bin/env bash


path=$(pwd)
#va ecrire dans les fichiers le chemin d'ou se situe le projet
sed -i -r "s@path=.*@path=$path@g" $path/sc2/conf/rc.local
sed -i -r "s@path=.*@path=$path@g" $path/interface.sh
sed -i -r "s@path=.*@path=$path@g" $path/restart.sh
sed -i -r "s@file =.*@file = open(\"$path\/sc2\/logz.txt\", \"w+\")@g" $path/sc2/dnsserveropti.py
#outils necessaires
#sudo apt-get install network-manager -y

sudo cp $path/sc2/conf/NetworkManager.conf /etc/NetworkManager/NetworkManager.conf
#sleep 20
sudo apt-get install dnsmasq -y
sudo apt-get install hostapd -y
sudo apt-get install gnome-terminal -y
sudo apt-get install apache2 -y
sudo apt-get install tshark -y
sudo apt-get install php -y
sudo apt-get install chromium-chromedriver -y
sudo apt-get install isc-dhcp-server -y
sudo apt-get install iptables -y
#sudo apt-get install network-manager -y
#sleep 20
#sleep 30
sudo apt autoremove -y
#driver carte alfa
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo apt-get install dkms -y
sudo make dkms_install
sudo make && sudo make install
sudo apt-get install raspberrypi-kernel-headers -y
sleep 20
sed -i 's/CONFIG_PLATFORM_I386_PC = y/CONFIG_PLATFORM_I386_PC = n/g' Makefile
sed -i 's/CONFIG_PLATFORM_ARM64_RPI = n/CONFIG_PLATFORM_ARM64_RPI = y/g' Makefile
export ARCH=arm
sed -i 's/^MAKE="/MAKE="ARCH=arm\ /' dkms.conf
cd ..
sudo rm -rf rtl8812au
#dependances server dns python
sudo pip install selenium
sudo pip install webdriver_manager
sudo pip install dnspython
python3 -m pip install wxpython
#serveur apache
sudo a2enmod rewrite && sudo service apache2 restart
#config dhcpd
sudo cp sc2/conf/dhcpd.conf /etc/dhcp/dhcpd.conf
#creation + droit aux fichiers necessaires
#pour eviter le changements de mac sur les interfaces reseau
sudo cp $path/sc2/conf/NetworkManager.conf /etc/NetworkManager/NetworkManager.conf
sudo touch /var/www/log.txt
chmod 646 /var/www/log.txt
sudo touch /var/www/id.txt
chmod 646 /var/www/id.txt
sudo touch /var/www/cred.txt
chmod 646 /var/www/cred.txt
chmod 747 saves_pcap/test.pcap
chmod 747 sc2/logz.txt
#fichier de redémarrage
sudo cp $path/sc2/conf/rc.local /etc/rc.local
#Configuration des interfaces Alfa et internet
echo -e "\033[1;31m\033[1mRentrer l'adresse Mac de la carte Alfa : (aa:bb:cc:dd:ee:ff) lettres en minuscules\033[0m"
read input
while [[ ! $input =~ ^([a-f0-9]{2}:){5}[a-f0-9]{2}$ ]]
do
	echo "Mauvais format d'adresse Mac"
	read input
done
alfa=""
while [[ $alfa = "" ]]
do
	ARRAY=(`ip a |awk '/state/{print $2}' | sed 's/.$//' | grep -v "eth0\|lo"`)
        for i in "${ARRAY[@]}"; do
                mac=$(ip link show dev $i |awk '/link/{print $2}')
                if [[ $mac = $input ]];then
                        alfa=$i
                fi
        done
done

if [[ $alfa = "wlan1" ]];then
        internet="wlan0"
	file=/etc/wpa_supplicant/wpa_supplicant-wlan0.conf
	if [[ -f "$file" ]];then
		sudo rm /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
        fi
	sudo cp $path/sc2/conf/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant-wlan1.conf
fi
if [[ $alfa = "wlan0" ]];then
#	echo "if2 $alfa" >> /home/pi/Desktop/date.txt
	internet="wlan1"
	file=/etc/wpa_supplicant/wpa_supplicant-wlan1.conf
        if [[ -f "$file" ]];then
                sudo rm /etc/wpa_supplicant/wpa_supplicant-wlan1.conf
        fi
        sudo cp $path/sc2/conf/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
fi

if [[ $alfa = "" ]];then
        echo "Carte alfa introuvable vérifier l'adresse Mac"
        echo "Mac disponibles :"
        for i in "${ARRAY[@]}"; do
                mac=$(ip link show dev $i |awk '/link/{print $2}')
                echo $mac " : "$i
        done
        exit 0
fi
if [[ $internet = "" ]];then
        echo "Vous n'êtes pas connecté à internet, vérifier votre connexion ou réessayer"
        exit 0
fi


echo -e "\033[1;32m\033[1mCarte trouvée !\033[0m"
sed -i -r "s/Int_Alfa=.*/Int_Alfa=$alfa/g" setup.sh
sed -i -r "s/Int_Wifi=.*/Int_Wifi=$internet/g" setup.sh
sed -i -r "s/mac=.*/mac=\"$input\"/g" setup.sh
sed -i -r "s/mac=.*/mac=\"$input\"/g" scriptgraphic.sh
sudo sed -i -r "s/interface.sh.*/interface.sh $input/g" '/etc/rc.local'

### test bug sc2 après l'install
sudo cp $path/sc2/conf/000-default.conf /etc/apache2/sites-enabled/000-default.conf
sudo rm -r /var/www/html/*
sudo cp -r $path/sc2/portail_captif_sc2.1/* /var/www/html/
sudo cp $path/sc2/conf/.htaccess /var/www/html/
sudo chmod 666 /var/www/html/.htaccess
sudo hostapd $path/sc2/hostapd.conf -B
sudo $path/sc2/gorb.sh
sudo $path/sc2/dnsserveropti.py &
sleep 10
sudo $path/stop.sh
###############################

echo -e "\n\n\033[1;31mInstallation terminée, nous vous invitons à reboot :)\n \033[0m"
