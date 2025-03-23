"""
Script: SpedionNewDriver.py
Description: [ADD DESCRIPTION HERE]
Usage: python SpedionNewDriver.py
"""

import datetime
import requests
import pymssql
from datetime import datetime
#import payload from payload
url = "https://services.spedion.de/StammdatenWsExtern/2.1/StammdatenWsExtern.asmx"
LIST_PATCH = '//srv-wss/Schnittstellen/_Scripte/py/SPEDION/LIST_Driver.txt'

def WRITELOG(log_txt):
    path = r'//srv-wss/Schnittstellen/_Scripte/log/'
    now = datetime.now()
    DtSt = str(now.strftime("%Y %m %d")).replace(' ','')
    MiSt = str(now.strftime("%d-%m-%Y %H:%M"))
    log = open(f'{path}/{DtSt}DriverAdd.log', 'a')
    log.write(f'[{MiSt} DriverAdd] ' + log_txt +'\n')
    log.close()


headers = {
  'charset': 'utf-8',
  'SOAPAction': '"http://ws.spedion.de/DriverAdd"',
  'Content-Type': 'Text/XML',
  'Host': 'services.spedion.de',
  #'Content-Length': 'length'
  'Authorization': "Basic YOUR_BASE64_HERE"
}

server="srv-db1"
user = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
db_name="WinSped"
STAT_SQL = '''
use WinSped
select 
PersonNr,
PersNr,
KartenID,
Vorname,
Name,
DrivingLicenseNo,
eMail,
Tel,
MobilTel,
MobilPriv
FROM XXAPers 
where 
personart = 1 
and YEAR(ErstDat) = YEAR(GETDATE()) and MONTH(ErstDat) = MONTH(GETDATE()) and  day(ErstDat) = day(GETDATE())
order by AendDat

'''
print (STAT_SQL)
db = pymssql.connect(server, user, password, db_name)
cursor = db.cursor(as_dict=True)
cursor.execute(STAT_SQL)
srtEnden = '\n\r'
STRLoader = '<?xml version="1.0" encoding="utf-8"?> ' + srtEnden
STRLoader = STRLoader + '<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"> ' + srtEnden
STRLoader = STRLoader + '<soap12:Body> '  + srtEnden
STRLoader = STRLoader + '   <DriverAdd xmlns="http://ws.spedion.de/"> ' + srtEnden
STRLoader = STRLoader + '     <driver> '  + srtEnden




for row in cursor:
    PersonNr = row['PersonNr']
    if PersonNr is not None:
        PersonNr = str(PersonNr)
        STRLoader = STRLoader + f'       <Pin>{PersonNr}</Pin> '  + srtEnden
        KartenID = row['KartenID']
        if KartenID is not None:
            KartenID = str(KartenID)
            STRLoader = STRLoader + f'       <Din>{KartenID}</Din> '  + srtEnden
        
        Vorname = row['Vorname']
        if Vorname is not None:
            Vorname=str(Vorname)
            STRLoader = STRLoader + '       <DriverState>Active</DriverState> ' + srtEnden
            STRLoader = STRLoader + f'       <FirstName>{Vorname}</FirstName> '  + srtEnden
        Name = row['Name']
        if Name is not None:
            Name= str(Name)
            STRLoader = STRLoader + f'       <LastName>{Name}</LastName> '  + srtEnden
            
        DrivingLicenseNo = row['DrivingLicenseNo']
        if DrivingLicenseNo is not None:
            DrivingLicenseNo = str(DrivingLicenseNo)
            STRLoader = STRLoader + f'       <DrivingLicenseNumber>{DrivingLicenseNo}</DrivingLicenseNumber> '  + srtEnden
        eMail = row['eMail']
        if eMail is not None:
            eMail = str(eMail)
            STRLoader = STRLoader + f'       <E_Mail>{eMail}</E_Mail> '  + srtEnden
        STRLoader = STRLoader + '     </driver> '  + srtEnden
        STRLoader = STRLoader + '   </DriverAdd> '  + srtEnden
        STRLoader = STRLoader + ' </soap12:Body> '  + srtEnden
        STRLoader = STRLoader + '</soap12:Envelope> '  + srtEnden

        with open(LIST_PATCH) as d:
            if str(PersonNr) in d.read(): 
                d.close()
                print(PersonNr + ' ist schon Da' )
            else:
                print (PersonNr + ' ist nicht Da' )
                file_2 = open(LIST_PATCH, 'a')
                file_2.write(PersonNr + '\n')
                file_2.close()
                
                print (STRLoader)
                response = requests.request("POST", url, headers=headers, data=STRLoader)
                print (response.text)
                print (response)