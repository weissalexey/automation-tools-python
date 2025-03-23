"""
Script: TJW_STAT_POD.py
Description: [ADD DESCRIPTION HERE]
Usage: python TJW_STAT_POD.py
"""

import xml.etree.ElementTree as ET
import urllib.request
import os, time, sys
import datetime
#import borb
from datetime import datetime
import time
from pathlib import Path
import pymssql
from datetime import datetime

#mypath = r"E:/Schnittstellen/TJW/OUTSTAT"
mypath = r"//srv-wss/Schnittstellen/TJW/test"
LIST_PATCH = r"//srv-wss/Schnittstellen/_Scripte/py/TJW_POD/PODAUFN_.txt"



def STATUSMAIKER (AufNr,NVE ,TIME, TYPE):
    STATpatch = "//srv-wss/Schnittstellen/TJW/IN/"
    #now = datetime.now()
    DtSt = str(TIME[:10].replace('-',''))
    DtSt = str(DtSt[-4:]+DtSt[3:4]+DtSt[:2])
    DtMt = str(TIME[-8:].replace(':',''))
    DtMt = str(DtMt[:4])
    var = f'''START|58fceae1-{NVE}|{DtSt}|||TJW|||CARSTENSEN||||||||||||
STATUS|58fceae1-{NVE}||{AufNr}||||{TYPE}||||{DtSt}|{DtMt}||||||||||||||||||||||||||||||||||||
ENDE|58fceae1-{NVE}|0|0|0|0|0|0|1|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|
31012024
'''
    with open(f'{STATpatch}{NVE}.txt', 'a') as out:
        out.write(var)

def WRITELOG(log_txt):
    path = r'//srv-wss/Schnittstellen/_Scripte/log/'
    now = datetime.now()
    DtSt = str(now.strftime("%Y %m %d")).replace(' ','')
    MiSt = str(now.strftime("%d-%m-%Y %H:%M"))
    log = open(f'{path}/{DtSt}TJW_STAT_POD.log', 'a')
    log.write(f'[{MiSt} TJW_STAT_POD] ' + log_txt +'\n')
    log.close()
        


WRITELOG('Begin')

sql_select = '''

use WinSped

select --distinct 
--top 10 
xxaArcSW.ArcDocINr, XXASLAuf.LiefNr, XXASLAuf.AufNr, xxaArcDoc.archiv,  Documents.DocumentData,XXASLAuf.EntBisDat, XXASLAuf.LiefDat,Exportiert from  XXASLAuf
left join xxaArcSW on SWort = CAST(AufNr AS VARCHAR(8))
left join xxaArcDoc on xxaArcSW.ArcDocINr = xxaArcDoc.ArcDocINr
left join WinSped_DMS..Documents on Documents.DocumentRefId = xxaArcDoc.ArcDocINr 
where Archiv in('Ablieferunterschrift Telematik','ABLIEFERFOTO TELEMATIK','Abliefernachweis' ) 
and XXASLAuf.AufgeberNr in ('11875', '9113269', '9145383')

'''

server="srv-db1"
user = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
db_name="WinSped"
db = pymssql.connect(server, user, password, db_name)
cursor = db.cursor(as_dict=True)

cursor.execute(sql_select)

for row in cursor:

        

    ArcDocINr = str(row['ArcDocINr'])
    print (ArcDocINr)
    with open(LIST_PATCH) as d:
        if str(ArcDocINr) in d.read(): 
            d.close()
        else:
            file_2 = open(LIST_PATCH, 'a')
            LiefNr = row['LiefNr']
            
            DAT_now = (row['LiefDat'].strftime("%d-%m-%Y %H:%M"))
            
            if LiefNr is None:
                LiefNr = str(row['AufNr'])
            else: 
                LiefNr = str(LiefNr)
            STR_TEXT = f'''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Shipments>
<Shipment identifier="{LiefNr}">
<Event type="420" time="{DAT_now}" PDF="https://service.carstensen.eu/DMS/ShowDocument?DocumentId={ArcDocINr}" Driver="Chr. Carstensen Logistics GmbH " />
</Shipment>
</Shipments>
'''
            file_2.write(f'{ArcDocINr}\n')
            file_2.close()
        
            print(f'{mypath}/{ArcDocINr}_{LiefNr}.xml')
            with open(f'{mypath}/{ArcDocINr}_{LiefNr}.xml', 'a') as out:
                out.write(STR_TEXT)
     

WRITELOG('END')    

