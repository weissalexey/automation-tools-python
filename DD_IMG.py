"""
Script: DD_IMG.py
Description: [ADD DESCRIPTION HERE]
Usage: python DD_IMG.py
"""

#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.keys import Keys
from os import walk
import os
import csv
import pymssql
import random
import datetime
import time
import random, string
from time import gmtime , strftime

LIST_PATCH = r'//srv-wss/Schnittstellen/DansckDistribution/in/Image/'
#LIST_PATCH1 = '//srv-wss/Schnittstellen/_Scripte/py/VTL/all_NOC.txt'
#LIST_PATCH2 = '//srv-wss/Schnittstellen/_Scripte/py/VTL/all_STU.txt'
#vorg = strftime("%d%m%Y",  time.localtime(time.time() - 72*3600))

server="srv-db1"
user = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
db_name="WinSped"

def STATUSMAIKER (AufNr, STNUM):
    RANDOMZHAL = str(random.random()).replace(".","")
    STATpatch = "//srv-wss/Schnittstellen/DansckDistribution/out/LIS_IN_IN/"
    #STATpatch = "e:/_Scripte/py/VTL/STAT/"
    now = strftime("%Y%m%d%H%M%S", gmtime())
    Dt = strftime("%Y%m%d", gmtime())
    St = strftime("%H%M", gmtime())
    var = f'''START|646VTLSTAT-{RANDOMZHAL}|{Dt}|||DDISTR|||Carstensen||||||||||||
STATUS|646VTLSTAT-{RANDOMZHAL}||{AufNr}||||{STNUM}||||{Dt}|{St}||||||||||||||||||||||||||||||||||||
ENDE|646VTLSTAT-{RANDOMZHAL}|0|0|0|0|0|0|1|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|
'''
    with open(f'{STATpatch}{RANDOMZHAL}.txt', 'a') as out:
        print (f'{STATpatch}{RANDOMZHAL}.txt')
        out.write(var)

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def html_table_to_list():
    driver = webdriver.Firefox()
    driver.get("https://my.vtl.de/portal/login.aspx")
    driver.find_element("name", "ctl00$CPHMain$tbLoginDepotID").send_keys("04245")
    driver.find_element("name", "ctl00$CPHMain$tbLoginUser").send_keys("aw")
    driver.find_element("name", "ctl00$CPHMain$tbLoginKennwort").send_keys("Gksa960036!!")
    driver.find_element("name", "ctl00$CPHMain$btnLogin").click()
    driver.get("https://my.vtl.de/portal/Sendungscenter/AuftragRecherche.aspx?AuftArt=1")
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ctl00_CPHMainB_M_dpFrom_rdpDate_dateInput"))).send_keys(vorg)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ctl00_CPHMainB_M_cblDepotArt_1"))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ctl00_CPHMainB_M_cblDepotArt_2"))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ctl00_CPHMainB_M_rbSuch"))).click()
    time.sleep(1.5)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ctl00_CPHMainB_M_rv_ctl09_ctl04_ctl00_ButtonImgDown"))).click()
    button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[3]/div[2]/div/div/table/tbody/tr[3]/td/div[1]/div/div[3]/table/tbody/tr/td/div[2]/div[7]")))#.click()
    driver.execute_script("$find('ctl00_CPHMainB_M_rv').exportReport('CSV');", button)
    time.sleep(1.5)
    driver.close()
    driver.quit()

def SQLAbfrage(FBNR):
    sql_select = f"select AufNr from XXASLAuf  where  LiefNr = '{FBNR}' or KommNr = '{FBNR}'"
    db = pymssql.connect(server, user, password, db_name)
    cursor = db.cursor(as_dict=True)
    cursor.execute(sql_select)
    AufNr = ''
    for row in cursor:
        AufNr = str(row['AufNr'])
        #print (AufNr)
    return AufNr

if __name__ == "__main__":
    #html_table_to_list()
    filenames = next(walk(LIST_PATCH), (None, None, []))[2]  # [] if no file
    for fm in filenames:
        print (fm)
        if fm[:9] == 'Recherche':
            with open(LIST_PATCH + fm, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=",")
                for row in spamreader:
                    AUF = ''
                    try :
                        if row[1][:6]== 'N04245'  :
                            AUF = row[1].replace('N04245.', '')
                        else:
                            AUF = SQLAbfrage(row[1])
                        if   row[12] == 'POD':
                            with open(LIST_PATCH1) as d:
                                if str(AUF) in d.read():
                                    d.close()
                                else:
                                    file_2 = open(LIST_PATCH1, 'a') # ich schribe alle auftrage die ich geschick wurde
                                    file_2.write(AUF + '\n')
                                    file_2.close
                                    STATUSMAIKER(AUF , '384')
                                    print (AUF + ','+ row[11])
                        else:
                            print (AUF + ','+ row[11])
                            file_2 = open(LIST_PATCH2, 'a') # ich schribe alle auftrage die ich geschick wurde
                            file_2.write(AUF + ','+ row[11] + '\n')
                            file_2.close
                    except:
                        next
            os.remove(LIST_PATCH + fm)

