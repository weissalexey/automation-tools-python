"""
Script: POD_inport.py
Description: [ADD DESCRIPTION HERE]
Usage: python POD_inport.py
"""

import requests
import os, time, sys
import http.client
import json 
import pymssql
import datetime
import time
from datetime import datetime
from random import randint
#from goto import goto, label

#path = r'n:\IT\script\DK'
path = r"\\srv-wss\Schnittstellen\_Scripte\py\FRAGTBREVFOLGESEDDEL"
now = time.time()
FILE_NAME = r'\\srv-wss\Schnittstellen\_Scripte\py\FRAGTBREVFOLGESEDDEL\INI.JSON'

def FILE_EXIST(path):
    """Test whether a path exists.  Returns False for broken symbolic links"""
    try:
        st = os.stat(path)
    except os.error:
        return False
    return True

def STATUSMAIKERR (CN, DTST, ID, DESCKRIP):

    WRITELOG(CN + ' ' + ' ' + DTST + ' ' + ID )
    path = r"\\srv-wss\Schnittstellen\DF\STAT\IN"
    print (f'{path}\Stat\{CN}.txt')
    WRITELOG(DATEVARI)
    var = '''@@PHSTAT512 0512  35  1 5 DE248   DF   
Q00100ELVDE248                              DF                                 DE248
Q10''' + CN + '''                           ''' + CN + '''                                                             ''' + ID +''''''+ DTST +'''                                                                          ''' + DESCKRIP + '''                          
Q110001870880
Z00000003'''+ DTST +'''33
@@PT
''' 
    file_path_Name = f'{path}\{CN}.txt'

    #label .begin

    if not FILE_EXIST(file_path_Name):
        with open(file_path_Name,"x") as out:
            out.write(var)
    else:
        file_path_Name = f'{path}\{CN}_{str(randint(0, 9000))}.txt'
        with open(file_path_Name,"x") as out:
            out.write(var)
        #goto .begin

#def STATUSMAIKER (CN):
#    print('POD')
#    WRITELOG('POD')

#    path = r"\\srv-wss\Schnittstellen\DF\STAT\IN"
#    print (f'{path}\Stat\{CN}.txt')
#    WRITELOG(DATEVARI)
#    now = datetime.now()
#    DtSt = str(now.strftime("%d %m %Y %H %M")).replace(' ','')
#    var = '''@@PHSTAT512 0512  35  1 5 DE248   DF   
#Q00100ELVDE248                              DF                                 DE248
#Q10''' + CN + '''                           ''' + CN + '''                                                              960'''+ DtSt +'''                                                                                Import in Ordnung               
#Q110001870880
#Z00000003'''+ DtSt +'''33
#@@PT
#'''
#    with open(f'{path}\{CN}.txt', 'a') as out:
#        out.write(var)
      

def TXTMACHER (STRLoader):
    file = open(r'\\srv-wss\Schnittstellen\_Scripte\py\FRAGTBREVFOLGESEDDEL\INI.JSON', 'wb')
    #file = open(r'N:\IT\script\DK\INI.JSON', 'wb')
    file.write(STRLoader)
    file.close()

def Api_json(FILE_NAME):
    import json 
    f = open(FILE_NAME)
    data = json.load(f)
    f.close()
    return data['API']
    
def DATEVARI_json(FILE_NAME):
    #import json 
    f = open(FILE_NAME)
    data = json.load(f)
    f.close()
    return data['DATEVARI']
  
def API_MACHER ():
    now = datetime.now()
    conn = http.client.HTTPSConnection("sts.fragt.dk")
    payload = 'client_id=062fa0a7-e55f-4f49-ae50-f6346d96c8ea&grant_type=password&username=fragt%5Capi_p_134639829&password=XeguauSx9k5kdtrb&resource=https%3A%2F%2Fapi.fragt.dk'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    conn.request("POST", "/adfs/oauth2/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    all_data = json.loads(data.decode("utf-8"))
    
    API_GET = all_data["access_token"]
    #DATEVARI= str(datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc))[0:10]
    #DATEVARI= str(datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc))[0:10]
    DATEVARI = str(now.strftime("%Y-%m-%d"))
    print (DATEVARI)
    WRITELOG(DATEVARI)
    Texter = '{"API":"bearer ' + API_GET + '","DATEVARI": "' + DATEVARI + '"}'
    TXTMACHER (Texter.encode())

def api_stat_anfr(CN,NPOD):
    print ('STATUS')
    url = "https://api.fragt.dk/v1/TrackAndTrace?consignmentNumber="+NPOD 
    ApI = Api_json(FILE_NAME)
    payload = {}
    headers = {
    'accept': 'application/json',
    'Authorization': ApI
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    STATJDATA = (response.content.decode("utf-8"))
    print(STATJDATA)
    #STATJDATA = STATJDATA.replace('}', '"}')
    #STATJDATA = STATJDATA.replace('":', '":"')
    #STATJDATA = STATJDATA.replace(':"', '":"')
    #STATJDATA = STATJDATA.replace(',', '",')
    #STATJDATA = STATJDATA.replace('}",{', '},{"')
    #STATJDATA = STATJDATA.replace('"["', '"')
    #STATJDATA = STATJDATA.replace('"]"', '"')
    #STATJDATA = STATJDATA.replace('""', '"')
    print(STATJDATA)

    STJSONDAT = json.loads(STATJDATA)
    CONT_I=0
    for ST_DATE in STJSONDAT:
        ST_DATE = STJSONDAT[CONT_I]['Date'][:16]
        ST_EventCode = STJSONDAT[CONT_I]['EventCode']
        CONT_I=CONT_I+1
        ST_DATE = datetime.strptime(ST_DATE, "%Y-%m-%dT%H:%M")
        ST_DATE = str(ST_DATE.strftime("%d %m %Y %H %M")).replace(' ','')

        print (ST_DATE + " " + ST_EventCode)
        
        server="srv-db1"
        user = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
        password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
        db_name="WinSped"
        STAT_SQL = "use winsped Declare @JSON varchar(max) Declare @Records varchar(max) SELECT @JSON=BulkColumn FROM OPENROWSET (BULK 'E:\status.json', SINGLE_CLOB) import SELECT * FROM OPENJSON (@JSON) WITH ([Id] int,[EnglishDescription] varchar(250),[EventCode] varchar(250)) where  id in (2125,2126,2127,2128) and EnglishDescription not in (select StatuHinweis from XXAV__AufStatusHistorie  where StatuHinweis is not null and aufnr = " + CN +") and EventCode ='" + ST_EventCode + "'"
        #STAT_SQL = "Declare @JSON varchar(max) Declare @Records varchar(max) SELECT @JSON=BulkColumn FROM OPENROWSET (BULK 'E:\status.json', SINGLE_CLOB) import SELECT * FROM OPENJSON (@JSON) WITH ([Id] int, [EnglishDescription] varchar(250), [EventCode] varchar(250)) where id in (2125,2126,2127,2128) and EventCode ='" + ST_EventCode + "'"
        WRITELOG (STAT_SQL)
        db1 = pymssql.connect(server, user, password, db_name)
        cursor = db.cursor(as_dict=True)
        cursor.execute(STAT_SQL)
        #path = r'n:\IT\script\DK\POD'
        for row in cursor:
            Stadt_id = str(row['Id'])
            DESCKRIP = str(row['EnglishDescription'])
            STATUSMAIKERR( CN ,ST_DATE , Stadt_id, DESCKRIP)        
            print (Stadt_id + ' '+ DESCKRIP)
            
        
        #with open(f'{path}\json_{NPOD}_{CN}.json', 'wb') as f:
        #    f.write(response.content)
    
def api_anfrager(CN,NPOD):
    url = "https://api.fragt.dk/v1/Archive/GetPOD?consignmentNumber="+NPOD 
    ApI = Api_json(FILE_NAME)
    payload = {}
    headers = {
    'accept': 'application/pdf',
    'Authorization': ApI
    }
    path = r'C:\Temp\JPG'
    print (f'{path}\pod_{NPOD}_{CN}.pdf') 
    WRITELOG(f'{path}\pod_{NPOD}_{CN}.pdf') 
    #path = r'\\srv-wss\Schnittstellen\GetMyInvoices\PDF'
    response = requests.request("GET", url, headers=headers, data=payload)
    with open(f'{path}\pod_{NPOD}_{CN}.pdf', 'wb') as f:
        f.write(response.content)
    DATGR = os.path.getsize(f'{path}\pod_{NPOD}_{CN}.pdf')
        
    if  DATGR > 0 :
        #STATUSMAIKER(CN) 
        file_2 = open(r'\\srv-wss\Schnittstellen\_Scripte\py\FRAGTBREVFOLGESEDDEL\PODAUFN.txt', 'a')
        file_2.write(CN + '\n')
        file_2.close()

    else:
        os.remove(os.path.join(path,f'pod_{NPOD}_{CN}.pdf'))

def WRITELOG(log_txt):
    now = datetime.now()
    DtSt = str(now.strftime("%Y %m %d")).replace(' ','')
    MiSt = str(now.strftime("%d-%m-%Y %H:%M"))
    path = r"\\srv-wss\Schnittstellen\_Scripte\log"
    log = open(f'{path}\{DtSt}DF_PIODIS.log', 'a')
    log.write(f'[{MiSt} DF_PIODIS] ' + log_txt +'\n')
    log.close()
    
server="srv-db1"
user = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
db_name="WinSped"
sql_select = "Declare @JSON varchar(max)Declare @Records varchar(max)SELECT @JSON=BulkColumn FROM OPENROWSET (BULK 'F:\_Scripte\Json\ADLIST.JSON', SINGLE_CLOB) import SELECT ISNULL(SenderReference, ConsignmentNumber) as SenderReference, ConsignmentNumber FROM OPENJSON (@JSON,N'$.ConsignmentNotes')WITH([ConsignmentNumber] varchar(50),[SenderReference] varchar(50))"

#path = r'n:\IT\script\DK'
#path = r"\\srv-wss\Schnittstellen\_Scripte\py\FRAGTBREVFOLGESEDDEL"

if not os.path.isfile(FILE_NAME):
    API_MACHER()
else:
    if os.stat(FILE_NAME).st_mtime < now - 3600:
        WRITELOG ('API ist Alt muss man erneuern')
        os.remove(os.path.join(path, FILE_NAME))
        API_MACHER()
        
ApI = Api_json(FILE_NAME)
DATEVARI = DATEVARI_json(FILE_NAME)
#print (ApI)
#print (DATEVARI)


url = f"https://api.fragt.dk/v1/Consignments/ByDate?sinceDateTime={DATEVARI}T00%3A00%3A00.291Z&suggestedMax=2000"
print (url)
WRITELOG(url)
payload = {}
headers = {
'accept': 'application/json',
'Authorization': ApI
}
response = requests.request("GET", url, headers=headers, data=payload)

with open(r'\\srv-db1\Json\ADLIST.JSON', 'wb') as f:
    f.write(response.content)
    

db = pymssql.connect(server, user, password, db_name)
cursor = db.cursor(as_dict=True)

cursor.execute(sql_select)
#path = r'n:\IT\script\DK\POD'

for row in cursor:
   NPOD = str(row['ConsignmentNumber'])
   CN = str(row['SenderReference'])
   
   with open(r'\\srv-wss\Schnittstellen\_Scripte\py\FRAGTBREVFOLGESEDDEL\PODAUFN.txt') as d:
        if str(CN) in d.read(): 
            d.close()
            print (CN + '.pdf ist schon Da' )
            WRITELOG(CN + '.pdf ist schon Da' )
        else:
            print (CN + '.pdf ist nicht Da' )
            WRITELOG (CN + '.pdf ist nicht Da' )
            api_anfrager(CN,NPOD) 
            api_stat_anfr(CN,NPOD)
            