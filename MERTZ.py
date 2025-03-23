"""
Script: MERTZ.py
Description: [ADD DESCRIPTION HERE]
Usage: python MERTZ.py
"""

from selenium import webdriver
import json
import os, heapq
import requests
import pymssql
import random
import datetime
import time
import random, string
import base64
from time import gmtime , strftime
from bs4 import BeautifulSoup
from http import cookiejar  
from lxml import html
import ast
    
class BlockAll(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

Zhaller = 0

LIST_PATCHD = '//srv-wss/Schnittstellen/_Scripte/py/MertZ/cookies.py'
LIST_PATCH = '//srv-wss/Schnittstellen/DansckDistribution/all_Coli.txt'
LIST_PATCH_ = '//srv-wss/Schnittstellen/DansckDistribution/all_ABF.txt'

now = strftime("%Y-%m-%d", gmtime())
vorg = strftime("%Y-%m-%d",  time.localtime(time.time() - 720*3600))

DtSt = str(now)
DtSt2 = str(vorg)
print (DtSt, DtSt2)
server="srv-db1"
user = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
db_name="WinSped"


def cookies_DEF():


    if not os.path.exists(LIST_PATCHD):
        driver = webdriver.Firefox()
        driver.get("http://t5.mertz.se/Logga-in?returnurl=%2f")
        driver.find_element("name", "dnn$ctr425$Login$Login_DNN$txtUsername").send_keys("tc@carstensen.eu")
        driver.find_element("name", "dnn$ctr425$Login$Login_DNN$txtPassword").send_keys("Winterland2022!")
        driver.find_element("id", "dnn_ctr425_Login_Login_DNN_cmdLogin").click()
        driver.get("http://t5.mertz.se/Bokningar")
        #get cookies and save as a variable
        cookies = driver.get_cookies()
        cookies_dict = {}
        
        for cookie in cookies:
            cookies_dict[cookie['name']] = cookie['value']
        
        file = open(LIST_PATCHD , 'a')
        #file.write('cookie = ' + str(cookies_dict))
        file.write(str(cookies_dict))
        file.close
        driver.quit()
        file = open(LIST_PATCHD, "r")
        content = file.read()
        print(content)
        file.close()
        return content
    else: 
        current_time = int(time.time() )
        day = int(43200)
        file_location = os.path.join(os.getcwd(), LIST_PATCHD)
        file_time = int(os.stat(file_location).st_mtime) 
        print (current_time - file_time, day)
        if(current_time - file_time  > day): 
        #if(current_time - file_time  != day): 
            print(f" Delete : {LIST_PATCHD}", file_time, current_time, day) 
            os.remove(file_location) 
        else:
            file = open(LIST_PATCHD, "r")
            content = file.read()
            print(content)
            file.close()
            return content

def SQL_TEST(AUFNR_ ):
    
    sql_select =  f'''
    select Archiv , Exportiert from xxaArcSW SW2 
    left join xxaArcDoc D on SW2.ArcDocINr = D.ArcDocINr and SW2.ArcSBINr = 1 AND NOT SW2.SWort IS NULL 
    where len(SW2.SWort) =8  and  Archiv in ('ABLIEFERFOTO', 'UNTERSCHRIFTDOKUMENT', 'ABLIEFERFOTO TELEMATIK' , 'Ablieferunterschrift Telematik', 'ABLIEFERNACHWEIS' )
    and Sw2.SWort = '{AUFNR_}'
    '''
    #print (sql_select)
    db = pymssql.connect(server, user, password, db_name)
    cursor = db.cursor(as_dict=True)
    cursor.execute(sql_select)
    for row in cursor:
        if row['Archiv'] is not None:
            #print (sql_select)
            return 1
        else:
            return None

def MA_STATUS(status):
    match status:
        case 1:
            return 'Status'
        case 2:
            return 'TRPStatus'
        case 3:
            return 'TERminStatus'
        case 4:
            return 'Resurs' 
        case 5:
            return 'FRNumer'
        case 6:
            return 'REFNR'
        case 7:
            return 'AUFNr'
        case 8:
            return 'LastDAG' 
        case 9:
            return 'BOrt'
        case 10:
            return 'Mottagare'
        case 11:
            return 'EOrt'
        case 12:
            return 'God' 
        case _:
            return ''

def POD_Maker(REFNR_ , AUFNR_, STATUS_, PK_, cookies):

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
    'Content-Type': 'application/json; charset=utf-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'http://t5.mertz.se',
    'Connection': 'keep-alive',
    'Referer': 'http://t5.mertz.se/Bokningar',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    }

    json_data = {
    'ModuleId': '439',
    'PK': PK_,
    }

    response = requests.post(
    'http://t5.mertz.se/DesktopModules/BF/T5Bokningar/Data/Services/Service.asmx/GetLeveransBekraftelse',
    cookies=cookies,
    headers=headers,
    json=json_data,
    )
    with open(f'//srv-wss/Schnittstellen/_Scripte/py/MERTZ/{AUFNR_}.json', 'wb') as filename:
        filename.write(response.content)
        filename.close
        
    with open(f'//srv-wss/Schnittstellen/_Scripte/py/MERTZ/{AUFNR_}.json', encoding="utf-8") as fff:
        json_POD = fff.read()
        dict_POD = json.loads(json_POD)
        fff.close
        Jheaders = []
        Pvalues = []
        for Jkey in dict_POD:
            Jhead = Jkey
            Jvalue = ""
            if type(dict_POD[Jkey]) == type({}):
                for JkeyJ in dict_POD[Jkey]:
                    Jhead = JkeyJ
                    if Jhead == 'Data':
                        POD_DAT = dict_POD[Jkey][JkeyJ]
                        try:
                            if len(POD_DAT)> 10:
                                with open(f'//SRV-WSS/Schnittstellen/GetMyInvoices/PDF/{AUFNR_}.pdf', 'wb') as f_name:
                                    f_name.write(base64.b64decode(POD_DAT))
                                    f_name.close
                                POD_DAT = ''
                                os.remove(f'//srv-wss/Schnittstellen/_Scripte/py/MERTZ/{AUFNR_}.json') 
                                
                        except:
                            print (STATUS_)

def JSON_Maker( cookies ):


    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
    'Content-Type': 'application/json; charset=utf-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'http://t5.mertz.se',
    'Connection': 'keep-alive',
    'Referer': 'http://t5.mertz.se/Bokningar',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    }

    json_data = {
    'ModuleId': '439',
    'UserId': '1141',
    'kundPK': '12397',
    'franDatum': f'{DtSt2}T23:00:00.000Z',
    'tillDatum': f'{DtSt}T23:00:00.000Z',
    'endastBifogad': False,
    'sokItem': 'Ert ordernummer',
    'fraktsedelnr': '',
    'datumInterval': True,
    'ControlPath': '/DesktopModules/BF/T5Bokningar/',
    'DisableNewEditBooking': False,
    'statusOk': True,
    'statusEjOk': True,
    'statusEjVald': True,
    'status': '',
    'visaMakuleradOrder': False,
    'defaultSearchIsNone': False,
    'VerksamhetFilterOrder': False,
    'VerksamhetPK': '',
    }

    response = requests.post(
    'http://t5.mertz.se/DesktopModules/BF/T5Bokningar/Data/Services/Service.asmx/GetOrders',
    cookies=cookies,
    headers=headers,
    json=json_data,
    )

    XX = response.content
    with open(f'//srv-wss/Schnittstellen/_Scripte/py/MERTZ/qwery.json', 'wb') as out:
        out.write(XX)
        out.close
    
if __name__ == "__main__":
    try:
        CC_DeF = cookies_DEF() 
        STATUS_ = ''
        with open(LIST_PATCHD,'r') as d:
            cookie = ast.literal_eval(d.read().replace('cookie =', ''))
            d.close()
        print(type(cookie))
        
        JSON_Maker( cookie )
        with open(f'//srv-wss/Schnittstellen/_Scripte/py/MERTZ/qwery.json', encoding="utf-8") as f:
            json_string = f.read()
            dictionary = json.loads(json_string)
            f.close
            headers = []
            values = []
            for key in dictionary:
                head = key
                value = ""
                if type(dictionary[key]) == type({}):
                    for key2 in dictionary[key]:
                        head = key2
                        if head == 'Data':
                            soup = BeautifulSoup(dictionary[key][key2] , 'html.parser')
                            table_rows = soup.find_all('tr')
                            table_data = []
                            for row in table_rows:
                                row_data = []
                                for cell in row.find_all('td'):
                                    Feld_Daten = cell.get_text().strip()
                                    TXT = str(cell.input)
                                    if len(TXT)> 5:
                                        PK = TXT.split(' ')
                                        PK_ = PK[3].replace('"',"").replace('pk=', '')
                                    if len(Feld_Daten) > 0:
                                        Zhaller += 1
                                        if MA_STATUS(Zhaller) == 'TRPStatus':
                                            STATUS_ = Feld_Daten
                                        if MA_STATUS(Zhaller) == 'REFNR':
                                            REFNR_ = Feld_Daten
                                        if MA_STATUS(Zhaller) == 'AUFNr':
                                            if len(Feld_Daten) > 2 :
                                                AUFNR_ = Feld_Daten
                                            else: 
                                                AUFNR_ = REFNR_
                                            #print (AUFNR_,STATUS_, SQL_TEST(AUFNR_))
                                            if SQL_TEST(AUFNR_) is None and STATUS_ == 'Utförd':
                                                if len(AUFNR_) == 8:
                                                    POD_Maker(REFNR_ , AUFNR_, STATUS_, PK_, cookie)
                                                    print (AUFNR_)
                                            STATUS_ = ''
                                            REFNR_ = ''
                                            AUFNR_ = ''
                                    else:
                                        if Zhaller > 12:
                                            Zhaller = 0
                                        else:
                                            if Zhaller == 0:
                                                Zhaller = 0
                                            else:
                                                Zhaller += 1
                                                if MA_STATUS(Zhaller) == 'Status':
                                                    STATUS_ = Feld_Daten
                                                if MA_STATUS(Zhaller) == 'REFNR':
                                                    REFNR_ = Feld_Daten
                                                if MA_STATUS(Zhaller) == 'AUFNr':
                                                    if len(Feld_Daten) > 2 :
                                                        AUFNR_ = Feld_Daten
                                                    else: 
                                                        AUFNR_ = REFNR_
                                                        
                                                    #print (AUFNR_, STATUS_ , SQL_TEST(AUFNR_))
                                                    if SQL_TEST(AUFNR_) is None and STATUS_ == 'Utförd':
                                                        if len(AUFNR_) == 8:
                                                            POD_Maker(REFNR_ , AUFNR_, STATUS_, PK_, cookie)
                                                            print (AUFNR_)
                                                    STATUS_ = ''
                                                    REFNR_ = ''
                                                    AUFNR_ = ''
    
                else:
                    value = dictionary[key]
    except:
        print(f" Delete : {LIST_PATCHD}", file_time, current_time, day) 
        os.remove(LIST_PATCHD) 
