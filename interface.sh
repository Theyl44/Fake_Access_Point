#! /usr/bin/env bash
path=/home/thomas/Desktop/Fake_Access_Point
input=$1
alfa=""
start=$SECONDS
while [[ $alfa = "" ]]
do
	ARRAY=(`ip a |awk '/state/{print $2}' | sed 's/.$//' | grep -v "eth0\|lo"`)
        for i in "${ARRAY[@]}"; do
                mac=$(ip link show dev $i |awk '/link/{print $2}')
#		echo $mac >> /home/pi/Desktop/date.txt
                if [[ $mac = $input ]];then
                        alfa=$i
#			echo "j'ai trouvé wola" >> /home/pi/Desktop/date.txt
                fi
        done
	duration=$(( SECONDS - start ))
	if [[ $duration -ge 5 ]];then
		echo -e "\033[1;31m\033[1mTenter de débrancher et rebrancher votre antenne wifi\033[0m"
		start=$SECONDS
	fi
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
 #       echo "if2 $alfa" >> /home/pi/Desktop/date.txt
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
#echo -e "\033[1;32m\033[1mCarte trouvée !\033[0m"
sed -i -r "s/Int_Alfa=.*/Int_Alfa=$alfa/g" $path/setup.sh
sed -i -r "s/Int_Wifi=.*/Int_Wifi=$internet/g" $path/setup.sh
sed -i -r "s/mac=.*/mac=\"$1\"/g" $path/setup.sh
sed -i -r "s/Int_Af=.*/Int_Af=$alfa/g" $path/restart.sh
sed -i -r "s/Int_Wf=.*/Int_Wf=$internet/g" $path/restart.sh
sed -i -r "s/mac=.*/mac=\"$1\"/g" $path/restart.sh
sed -i -r "s/^mac=.*/mac=\"$1\"/g" $path/scriptgraphic.sh
sudo sed -i -r "s/interface.sh.*/interface.sh $input/g" '/etc/rc.local'
#echo "alfa : "$alfa
#echo "inter : "$internet
