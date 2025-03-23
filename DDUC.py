"""
Script: DDUC.py
Description: [ADD DESCRIPTION HERE]
Usage: python DDUC.py
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
from time import gmtime , strftime
from bs4 import BeautifulSoup
from http import cookiejar  
class BlockAll(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False


LIST_PATCH = '//srv-wss/Schnittstellen/DansckDistribution/all_Coli.txt'
LIST_PATCH_ = '//srv-wss/Schnittstellen/DansckDistribution/all_ABF.txt'
#today = datetime.date.today()

now = strftime("%d-%m-%Y", gmtime())
vorg = strftime("%d-%m-%Y",  time.localtime(time.time() - 72*3600))

DtSt = str(now)
DtSt2 = str(vorg)
#DtSt = '01-10-2024'
#DtSt2 = '14-10-2024'
print (DtSt, DtSt2)
server="srv-db1"
user = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
db_name="WinSped"

def htmlMAIKER (var):
    with open(f'//srv-wss/Schnittstellen/DansckDistribution/qwery.html', 'w') as out:
        out.write(var)
    return 1

def STATUSMAIKER (AufNr, STNUM):
    RANDOMZHAL = str(random.random()).replace(".","")
    STATpatch = "//srv-wss/Schnittstellen/DansckDistribution/out/LIS_IN_IN/"
    now = strftime("%Y%m%d%H%M%S", gmtime())
    Dt = strftime("%Y%m%d", gmtime())
    St = strftime("%H%M", gmtime())
    var = f'''START|646999-{RANDOMZHAL}|{Dt}|||DDISTR|||Carstensen||||||||||||
STATUS|646999-{RANDOMZHAL}||{AufNr}||||{STNUM}||||{Dt}|{St}||||||||||||||||||||||||||||||||||||
ENDE|646999-{RANDOMZHAL}|0|0|0|0|0|0|1|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|
'''
    with open(f'{STATpatch}{RANDOMZHAL}.txt', 'a') as out:
        print (f'{STATpatch}{RANDOMZHAL}.txt')
        out.write(var)
        
def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))
   

def html_table_to_list(DtSt, DtSt2, CC_DeF ):
    
    session = requests.Session()
    CC_DeF = CC_DeF.split(";")
    #print (CC_DeF)
    #cookies = {"ASPSESSIONIDCUTCQRTC": "GJCJFONCHJALECPCOHNBBGCB"}
    cookies = {CC_DeF[0]:CC_DeF[1]}
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        #'cookie': CC_DeF,
        'origin': 'https://cc.online-book.dk',
        'priority': 'u=0, i',
        'referer': 'https://cc.online-book.dk/adm/',
        'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    }
    
    data = {
        'T1': 'tn',
        'T2': 'carstensen',
        'B1': 'Login',
    }
    
    response = session.post('https://cc.online-book.dk/adm/login.asp', headers=headers, data=data , cookies = cookies )
    print (response)
    #print (self.cookies.update( requests.utils.dict_from_cookiejar(response.cookies)))
    
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://cc.online-book.dk',
    'Connection': 'keep-alive',
    'Referer': 'https://cc.online-book.dk/sites/arkiv/start_ny_arkiv.asp',
    #'Cookie': CC_DeF,
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'frame',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=4',
    }
    
    data = f'T4=&T1=&T15=&T2=&T16=&T3=&T7=&T14=&T8=&T11=&T21=&T12=&T20=&T13=&T19=&T5={DtSt2}&T18=&T9={DtSt}&T17=&T6=&T10=&T22=&T23=&T24=&T25=&T26=&T27=&T28=&T29=&T30=&T31=&T32=&T33=&T34=&sort=modtagetDato&B1=S%F8g'
    
    response = session.post('https://cc.online-book.dk/sites/arkiv/vis_ny_liste.asp', cookies= cookies , headers=headers, data=data)
    #print (response.cookies)


    print(response)
    XX = response.text
    with open(f'//srv-wss/Schnittstellen/DansckDistribution/qwery.html', 'wb') as out:
        out.write(response.content)
    return XX

def SQLAbfrage(FBNR):
    sql_select = f"select AufNr from XXASLAuf  as SLAuf left join  XXAAufExt TT on SLAuf.AufIntNr = TT.AufIntNr  where  TrackandTraceEmail like '{FBNR}%'"
    db = pymssql.connect(server, user, password, db_name)
    cursor = db.cursor(as_dict=True)
    cursor.execute(sql_select)
    AufNr = ''
    for row in cursor:
        AufNr = str(row['AufNr'])
        print (AufNr)
    return AufNr
    
def cookies_DEF():
    #LIST_PATCHD = '//srv-wss/Schnittstellen/_Scripte/py/DD/cookies.py'
    LIST_PATCHD = '//srv-wss/Schnittstellen/DansckDistribution/cookies.py'
    if not os.path.exists(LIST_PATCHD):
        driver = webdriver.Firefox()
        driver.get("https://cc.online-book.dk/adm/")
        driver.find_element("name", "T1").send_keys("tn")
        driver.find_element("name", "T2").send_keys("carstensen")
        driver.find_element("name", "B1").click()
        #get cookies and save as a variable
        cookies = driver.get_cookies()
        cookies_dict = {}
        
        for cookie in cookies:
            #cookies_dict[cookie['name']] = cookie['value']
            cookies_dict = cookie['name'] + ";" + cookie['value']
        #print(cookies_dict)
        
        file = open(LIST_PATCHD , 'a')
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
   
if __name__ == "__main__":
    CC_DeF = cookies_DEF() 
    #CC_DeF = 'ASPSESSIONIDSUTARSDT;FCAAELHDFHLIDJDPEGDKHDBE'
    FBNR = ''
    Fragtnr = ''
    Fragtnr_CON = 0
    AufNr = ''
    OMEX = ''
    soup = BeautifulSoup(html_table_to_list(DtSt, DtSt2, CC_DeF) , 'html.parser')
    
    
    
    table_rows = soup.find_all('tr')
    table_data = []
    for row in table_rows:
        row_data = []
        for cell in row.find_all('td'):
            FBNR = cell.get_text().strip()
            if len(FBNR) == 8:
                try :
                    int(FBNR)
                    match len(FBNR):
                        case 8:  # 
                            if Fragtnr_CON == 0:
                                Fragtnr = FBNR 
                                Fragtnr_CON = 1
                            if Fragtnr[:3] == '645':
                                with open(LIST_PATCH) as d:
                                    if str(Fragtnr) in d.read(): 
                                        d.close()
                                        #if FBNR == '66471472':
                                        print(FBNR + ' ist schon Da' )
                                    else:
                                        print (Fragtnr + ' ist nicht Da' )
                                        file_2 = open(LIST_PATCH , 'a')
                                        AufNr = SQLAbfrage(Fragtnr)
                                        if len(AufNr)> 0:
                                            XX = STATUSMAIKER (AufNr, '6999')
                                            file_2.write(Fragtnr + '\n')
                                            file_2.close

                except ValueError : 
                    continue
            else:
                for CCel in cell.find_all('img', attrs={"src":"/images/pl_2.gif"}):
                    with open(LIST_PATCH_) as d:
                        if str(Fragtnr) in d.read(): 
                            d.close()
                        else:
                            AufNr = SQLAbfrage(Fragtnr)
                            
                            if len(AufNr) > 0:
                                XX = STATUSMAIKER (AufNr, '6998')
                                print (Fragtnr_CON, Fragtnr, AufNr )
                                file_2 = open(LIST_PATCH_ , 'a')
                                file_2.write(Fragtnr + '\n')
                                file_2.close
               
        Fragtnr = ''
        AufNr = ''                    
        Fragtnr_CON = 0
