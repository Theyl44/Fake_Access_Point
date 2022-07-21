#!/usr/bin/env python

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

##### GET FILES VALUES #####
f = open("../id.txt", "r")
lines = f.readlines()
file_login = lines[0]
file_password = lines[1]

l = open("../cred.txt", "r")
line = l.readlines()
u_login = line[0]
u_password = line[1]
##### SETUP WEB ENV ######
option = Options()
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')
s = Service('/usr/bin/chromedriver')
driver = webdriver.Chrome(options=option,service=s)
driver.get('https://controller.access.network/107/portal/')
time.sleep(0.4)
########## DECONNEXION ##########
driver.find_element(By.ID, 'feedbackForm_disconnect_button').click()
#time.sleep(0.4)
####### CONNECTION VALUES #######
driver.get('https://controller.access.network/107/portal/')
time.sleep(0.4)
form = driver.find_element(By.XPATH, '//*[@id="logonForm_standard_auth_form"]')
login = form.find_element(By.NAME,'login')
login.send_keys(str(file_login))
password = form.find_element(By.NAME,'password')
password.send_keys(str(file_password))
form.find_element(By.NAME, 'policy_accept').click()
form.find_element(By.ID, 'logonForm_connect_button').click()
####### CHECK CONNECTION #######
time.sleep(0.2)
driver.get('https://controller.access.network/107/portal/#')
feedback = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[3]/div/form[3]')
back = feedback.find_elements(By.ID,"feedbackForm_login_value")

file_login = file_login.strip('\n')
if back[0].text.lower() == file_login.lower():
	print("OK")
	driver.find_element(By.ID, 'feedbackForm_disconnect_button').click()
########## RECONNEXION #########
driver.get('https://controller.access.network/107/portal/#')	
time.sleep(0.2)
form = driver.find_element(By.XPATH, '//*[@id="logonForm_standard_auth_form"]')
login = form.find_element(By.NAME,'login')
login.send_keys(str(u_login))
password = form.find_element(By.NAME,'password')
password.send_keys(str(u_password))
form.find_element(By.NAME, 'policy_accept').click()
form.find_element(By.ID, 'logonForm_connect_button').click()
driver.quit()
