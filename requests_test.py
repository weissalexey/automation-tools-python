"""
Script: requests_test.py
Description: [ADD DESCRIPTION HERE]
Usage: python requests_test.py
"""

#from selenium import webdriver
import json
import os, heapq
import time 

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# Github credentials


# initialize the Chrome driver






def cookies_DEF():
    username = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
    password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
    LIST_PATCHD = '//srv-wss/Schnittstellen/_Scripte/py/DD/cookies.py'
    current_time = time.time() 
    day = 43.200
    file_location = os.path.join(os.getcwd(), LIST_PATCHD)
    file_time = os.stat(file_location).st_mtime 
    #if(file_time - current_time  > day): 
    print(f" Delete : {LIST_PATCHD}", file_time, current_time, day) 
    os.remove(file_location) 
    driver = webdriver.Firefox()
    driver.get("https://cc.online-book.dk/adm/")
    driver.find_element("name", "T1").send_keys(username)
    driver.find_element("name", "T2").send_keys(password)
    driver.find_element("name", "B1").click()
    #get cookies and save as a variable
    cookies = driver.get_cookies()
    cookies_dict = {}
    
    for cookie in cookies:
        cookies_dict[cookie['name']] = cookie['value']
        OUT_str = cookie['name'] + ";" + cookie['value']
    #print(cookies_dict)
    
    file = open(LIST_PATCHD , 'a')
    file.write(str(OUT_str))
    file.close
    #driver.quit()
    file = open(LIST_PATCHD, "r")
    content = file.read()
    print(content)
    file.close()
    return content


XXX = cookies_DEF()