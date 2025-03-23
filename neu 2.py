"""
Script: neu 2.py
Description: [ADD DESCRIPTION HERE]
Usage: python neu 2.py
"""

import requests
import pymssql
import random
import datetime
from time import gmtime, strftime
from bs4 import BeautifulSoup
LIST_PATCH = '//srv-wss/Schnittstellen/DansckDistribution/all_Coli.txt'
now = strftime("%d-%m-%Y", gmtime())
DtSt = str(now)
server="srv-db1"
user = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
db_name="WinSped"
AufNr = ''
def STATUSMAIKER (AufNr):
    RANDOMZHAL = str(random.random()).replace(".","")
    STATpatch = "//srv-wss/Schnittstellen/DansckDistribution/out/LIS_IN_IN/"
    now = strftime("%Y%m%d%H%M%S", gmtime())
    Dt = strftime("%Y%m%d", gmtime())
    St = strftime("%H%M", gmtime())
    var = f'''START|646999-{RANDOMZHAL}|{Dt}|||DDISTR|||Carstensen||||||||||||
STATUS|646999-{RANDOMZHAL}||{AufNr}||||6999||||{Dt}|{St}||||||||||||||||||||||||||||||||||||
ENDE|646999-{RANDOMZHAL}|0|0|0|0|0|0|1|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|
'''
    with open(f'{STATpatch}{RANDOMZHAL}.txt', 'a') as out:
        print (f'{STATpatch}{RANDOMZHAL}.txt')
        out.write(var)


def html_table_to_list(DtSt):

    cookies = {
        'ASPSESSIONIDQWTSDDAB': 'OKNPGMFCKKEFOELDEHHEKDAA',
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://cc.online-book.dk',
        'Connection': 'keep-alive',
        'Referer': 'https://cc.online-book.dk/sites/arkiv/start_ny_arkiv.asp',
        # 'Cookie': 'ASPSESSIONIDQWTSDDAB=OKNPGMFCKKEFOELDEHHEKDAA',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'frame',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=4',
    }
    
    data = {
        'T1': 'tn',
        'T2': 'carstensen',
        'B1': 'Login',
    }
    
    response = requests.post('https://cc.online-book.dk/adm/login.asp', cookies=cookies, headers=headers, data=data)
    
    data = f'T4=&T1=&T15=&T2=&T16=&T3=&T7=&T14=&T8=&T11=&T21=&T12=&T20=&T13=&T19=&T5=&T18=&T9=&T17=&T6=&T10=&T22=&T23=&T24=&T25=&T26=&T27=&T28=&T29=&T30=&T31=&T32={DtSt}&T33=&T34=&sort=modtagetDato&B1=S^%^F8g'
    
    response = requests.post('https://cc.online-book.dk/sites/arkiv/vis_ny_liste.asp', cookies=cookies, headers=headers, data=data)
    print(response)
    
    return response.text

if __name__ == "__main__":
    html = html_table_to_list(DtSt) 
    soup = BeautifulSoup(html, 'html.parser')
    table_rows = soup.find_all('tr')
    table_data = []
    for row in table_rows:
        row_data = []
        #print (row_data)
        for cell in row.find_all('td'):
            FBNR = cell.get_text().strip()
            try :
                int(FBNR)
                match len(FBNR):
                    case 8:  # 
                        if FBNR[:3] == '645':
                            print (FBNR)
                            with open(LIST_PATCH) as d:
                                if str(FBNR) in d.read(): 
                                    d.close()
                                    print(FBNR + ' ist schon Da' )
                                else:
                                    print (FBNR + ' ist nicht Da' )
                                    file_2 = open(LIST_PATCH , 'a')
                                    
                                    sql_select = f"select AufNr from XXASLAuf  as SLAuf left join  XXAAufExt TT on SLAuf.AufIntNr = TT.AufIntNr  where  TrackandTraceEmail like '{FBNR}%'"
                                    print( sql_select)
                                    db = pymssql.connect(server, user, password, db_name)
                                    cursor = db.cursor(as_dict=True)
                                    cursor.execute(sql_select)
                                    AufNr = ''
                                    for row in cursor:
                                        AufNr = str(row['AufNr'])
                                        if len(AufNr)> 0:
                                            XX = STATUSMAIKER (AufNr)
                                            file_2.write(FBNR + '\n')
            except ValueError : 
                XX = ''
