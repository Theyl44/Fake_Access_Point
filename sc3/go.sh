#! /usr/bin/env bash

sudo ifconfig wlan1 down
sudo iwconfig wlan1 mode monitor
sudo ifconfig wlan1  up

sudo iwconfig wlan1 channel 1 
ip link show wlan1
