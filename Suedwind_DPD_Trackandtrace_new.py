"""
Script: Suedwind_DPD_Trackandtrace_new.py
Description: [ADD DESCRIPTION HERE]
Usage: python Suedwind_DPD_Trackandtrace_new.py
"""


server="srv-db1"
user = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
db_name="WinSped"
LIST_PATCH = "//srv-wss/Schnittstellen/Suedwind/Allready_Exported.txt"
LIST_PATCH_OUT = "//srv-wss/Schnittstellen/Suedwind/OutTracking/"
LIST_PATCH_ARJ = "//srv-wss/Schnittstellen/Suedwind/OutTrackingSave/"
import pyodbc
from datetime import datetime
noww = datetime.now()
DDtSt = str(noww.strftime("%Y-%m-%d")).replace(' ','-')
print (DDtSt)
cnxn = pyodbc.connect("Driver={SQL Server};"

                      f"Server={server};"
                      f"Database={db_name};"
                      f"User={db_name};"
                      f"fuid={user};pwd={password}")
cursor = cnxn.cursor()
cursor.execute('select sHilf2, AufNr, Gewicht from WinLager..XXALAvisPo where sHilf2 is not null and Kunde = 50267  and year(LiefDatVon) = YEAR(getdate()) and Month(LiefDatVon) > Month(GETDATE()) -2 order by shilf2 DESC')
for row in cursor:
    AufIntNr =str(row[0]) if row[0] is not None else ''
    AufNr = str(row[1]) if row[1] is not None else ''
    Gewicht = str(row[2]) if row[2] is not None else ''
    AUF = f"{AufIntNr};{AufNr};"
    with open(LIST_PATCH) as d:
        if str(AUF) in d.read():
            d.close()
            #print(AUF + ' ist schon Da' )
            AufName =''
            SRTR= ''
        else:
            AufName = f"{LIST_PATCH_OUT}{AufNr}_{DDtSt}_{AufIntNr}.csv"
            AufNameARJ = f"{LIST_PATCH_ARJ}{AufNr}_{DDtSt}_{AufIntNr}.csv"
            SRTR = f"{AufIntNr};{AufNr};{Gewicht};"
            print (AUF + ' ist nicht Da' )
            file_2 = open(LIST_PATCH , 'a') # ich schribe alle auftrage die ich geschick wurde
            file_2.write(AUF + '\n')
            file_1 = open(AufName  , 'a') # ich schribe alle auftrage die ich geschick wurde
            file_1.write(SRTR)
            file_0 = open(AufNameARJ , 'a')
            file_0.write(SRTR)
            d.close()
            
