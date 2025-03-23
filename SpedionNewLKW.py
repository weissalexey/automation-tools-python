"""
Script: SpedionNewLKW.py
Description: [ADD DESCRIPTION HERE]
Usage: python SpedionNewLKW.py
"""

import requests
import pymssql
#import payload from payload
url = "https://services.spedion.de/StammdatenWsExtern/2.1/StammdatenWsExtern.asmx"
LIST_PATCH = '//srv-wss/Schnittstellen/_Scripte/py/SPEDION/LIST_PATCH.txt'

def TextMAIKER (STRLoader ,NNAME ):
    with open(f'{NNAME}.txt', 'a') as out:
        out.write(STRLoader)
        out.close()



headers = {
  'charset': 'utf-8',
  'SOAPAction': '"http://ws.spedion.de/VehicleAdd"',
  'Content-Type': 'Text/XML',
  'Host': 'services.spedion.de',
  'Authorization': "Basic YOUR_BASE64_HERE"
}

server="srv-db1"
user = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
db_name="WinSped"
STAT_SQL = "SELECT b.LKW , a.LKWINr,a.Hersteller,a.Modell,a.FahrgNr,a.Handy,a.AbmeldDat,a.AendDat,a.ModelShort, b.LKw, b.polKz FROM XXALKWZU as a left join XXALKW as b on  a.lKWinr = b.lKWinr where YEAR(b.ErstDat) = YEAR(GETDATE()) and MONTH(b.ErstDat) = MONTH(GETDATE()) and  day(b.ErstDat) = day(GETDATE())"
print (STAT_SQL)
db = pymssql.connect(server, user, password, db_name)
cursor = db.cursor(as_dict=True)
cursor.execute(STAT_SQL)

for row in cursor:
    #LKWINr = str(row['LKWINr'])
    LKWINr = str(row['LKW'])
    #print (LKWINr)
    Hersteller = str(row['Hersteller'])
    Modell = str(row['Modell'])
    FahrgNr = str(row['FahrgNr'])
    Handy = str(row['Handy'])
    ModelShort = str(row['ModelShort'])
    LKw = str(row['LKw'])
    polKz = str(row['polKz'])
    with open(LIST_PATCH) as d:
        if str(LKWINr) in d.read(): 
            d.close()
            print(LKWINr + ' ist schon Da' )
        else:
            print (LKWINr + ' ist nicht Da' )
            file_2 = open(LIST_PATCH, 'a')
            file_2.write(LKWINr + '\n')
            file_2.close()
            STRLoader = f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\r\n<soap12:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap12=\"http://www.w3.org/2003/05/soap-envelope\">\r\n  <soap12:Body>\r\n    <VehicleAdd xmlns=\"http://ws.spedion.de/\">\r\n      <vehicle>\r\n        <Name>{LKw}</Name>\r\n        <NumberPlate>{polKz}</NumberPlate>\r\n        <VehicleState>Active</VehicleState>\r\n        <HasAndroid>true</HasAndroid>\r\n        <TankCapacity>0</TankCapacity>\r\n        <InfoField>{ModelShort}</InfoField>\r\n        <TelephoneNumber>{Handy}</TelephoneNumber>\r\n        <VehicleIdentificationNumber>{FahrgNr}</VehicleIdentificationNumber>\r\n        <BranchLocation>Chr. Carstensen</BranchLocation>\r\n      </vehicle>\r\n    </VehicleAdd>\r\n  </soap12:Body>\r\n</soap12:Envelope>"
            NNAME = str(LKw)
            print (STRLoader)
            #TextMAIKER ( STRLoader, NNAME)  
            #STRLoader, NNAME
            response = requests.request("POST", url, headers=headers, data=STRLoader)




#print(response.text)
