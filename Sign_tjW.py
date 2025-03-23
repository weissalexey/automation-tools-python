"""
Script: Sign_tjW.py
Description: [ADD DESCRIPTION HERE]
Usage: python Sign_tjW.py
"""

import xml.etree.ElementTree as ET
import urllib.request
import os, time, sys
import datetime
import time
import shutil
from pathlib import Path
import pymssql
from datetime import datetime
from os import walk



def WRITELOG(log_txt):
    path = r'//srv-wss/Schnittstellen/_Scripte/log/'
    now = datetime.now()
    DtSt = str(now.strftime("%Y %m %d")).replace(' ','')
    MiSt = str(now.strftime("%d-%m-%Y %H:%M"))
    log = open(f'{path}/{DtSt}TJW_POD.log', 'a')
    log.write(f'[{MiSt} Sign_TJW] ' + log_txt +'\n')
    log.close()


WRITELOG('Begin')

sql_select = """

SELECT CASE 
 WHEN NVE.NVE is null 
  then  CONVERT(varchar(10), SLAuf.AufNr) 
  else 
  NVE.NVE
  END as 'Auf'
FROM dbo.XXASLAuf AS SLAuf 
left JOIN dbo.XXANVE AS NVE ON SLAuf.AufIntNr = NVE.AufIntNr 
where SLAuf.FZNr in ('11875', '9113269', '9145383')

"""                  

print( sql_select)
server="srv-db1"
user = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
db_name="WinSped"
db = pymssql.connect(server, user, password, db_name)
cursor = db.cursor(as_dict=True)
cursor.execute(sql_select)

WRITELOG('Begin')
LIST_PATCH = r"//srv-wss/Schnittstellen/_Scripte/py/TJW_POD/SigN.txt"
#mypath = r"//srv-wss/Schnittstellen/TJW/test"
mypath = r"//srv-wss/Schnittstellen/TJW/Home/STATOUT"

for row in cursor:
    Auf = str(row['Auf'])
    
    with open(LIST_PATCH) as d:
        if str(Auf) in d.read(): 
            d.close()
        else:
            print (Auf )
            file_2 = open(LIST_PATCH, 'a')
            FNAME = Path(f"//SRV-tel/Spedion/Unterschriften/{Auf}.GIF")
            #FNAME = Path(f"c:/temp/sign/{Auf}.GIF")
            if FNAME.is_file():
                f_dest = f"//srv-wss/Schnittstellen/TJW/Home/SIGNOUT/{Auf}.GIF"
                shutil.copyfile(FNAME, f_dest)  
                now = datetime.now()
                DAT_now = str(now.strftime("%d-%m-%Y %H:%M"))
                STR_TEXT = f'''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Shipments>
        <Shipment identifier="{Auf}">
            <Event type="420" time="{DAT_now}" PDF="ftp://carstensen.eu/SIGNOUT/{Auf}.gif" Driver="Chr. Carstensen Logistics GmbH " />
        </Shipment>
</Shipments>
'''
                with open(f'{mypath}/{Auf}.xml', 'a') as out:
                    out.write(STR_TEXT)
#*********************************************************************************************
                file_2.write(Auf + '\n')
                FNAME = ''
            file_2.close()
WRITELOG('END')  


#***********************************************************************************************************************   



file_2.close()
WRITELOG('END')    
