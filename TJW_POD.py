"""
Script: TJW_POD.py
Description: [ADD DESCRIPTION HERE]
Usage: python TJW_POD.py
"""

import xml.etree.ElementTree as ET
import urllib.request
import os, time, sys
import datetime
import time
import pymssql
from datetime import datetime
from decimal import Decimal  
from fpdf import FPDF, HTMLMixin

class HTML2PDF(FPDF, HTMLMixin):
    pass
    
mypath = r"//srv-wss/Schnittstellen/TJW/INBCK"
LIST_PATCH = r"//srv-wss/Schnittstellen/_Scripte/py/TJW_POD/PODAUFN.txt"
from os import walk

def STATUSMAIKER (AufNr,NVE ,TIME, TYPE):
    STATpatch = "//srv-wss/Schnittstellen/TJW/IN/"
    #now = datetime.now()
    DtSt = str(TIME[:10].replace('-',''))
    print (DtSt) 
    DtSt = str(DtSt[-4:]+DtSt[2:4]+DtSt[:2])
    DtMt = str(TIME[-8:].replace(':',''))
    DtMt = str(DtMt[:4])
    var = f'''START|38fceae1-{NVE}|{DtSt}|||TJW|||CARSTENSEN||||||||||||
STATUS|38fceae1-{NVE}||{AufNr}||||{TYPE}||||{DtSt}|{DtMt}||||||||||||||||||||||||||||||||||||
ENDE|38fceae1-{NVE}|0|0|0|0|0|0|1|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|
'''
    with open(f'{STATpatch}{NVE}.txt', 'a') as out:
        out.write(var)
        

def WRITELOG(log_txt):
    path = r'//srv-wss/Schnittstellen/_Scripte/log/'
    now = datetime.now()
    DtSt = str(now.strftime("%Y %m %d")).replace(' ','')
    MiSt = str(now.strftime("%d-%m-%Y %H:%M"))
    log = open(f'{path}/{DtSt}TJW_POD.log', 'a')
    log.write(f'[{MiSt} TJW_POD] ' + log_txt +'\n')
    log.close()

filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file

WRITELOG('Begin')

for fm in filenames:
    with open(LIST_PATCH) as d:
        if str(fm) in d.read(): 
            d.close()
        else:
            file_2 = open(LIST_PATCH, 'a')
            xml_path = (mypath +'\\'+ fm)
            try:
                mytree = ET.parse(xml_path)
                myroot = mytree.getroot()
                for x in myroot:
            
                    NVE = x.attrib['identifier']
                    for y in x:
                        
                        TYPE = y.attrib['type']
                        TIME = y.attrib[ 'time']
                        
                        try:
                            IMAGE = y.attrib['IMAGE']
                            file_path_Name = mypath + "\\Image\\" + NVE +'_IMAGE'+ ".JPG"
                            urllib.request.urlretrieve(POD, file_path_Name)
                        except:
                            IMAGE = ''         
                        try:     
                            POD = y.attrib['POD']
                            file_path_Name = mypath + "\\Image\\" + NVE +'_SIGN'+ ".PNG"
                            urllib.request.urlretrieve(POD, file_path_Name)
                        except:
                            POD = ''
                        try: 
                            PODName = y.attrib['PODName']
                        except:
                            PODName = ''
                        try:     
                            DRIVER = y.attrib[ 'Driver']
                        except:
                            DRIVER = ''
                        
                        print (NVE, TYPE , TIME ,  PODName, DRIVER, POD, IMAGE )
                        #***********************************************************************************************************************
                        if len(NVE) > 8:
                            sql_select = "use winsped select *  from XXAV_drLabelGenSL_941 where NVE= '" + NVE + "'"
                        else:
                            sql_select = "use winsped select * from XXAV_drLabelGenSL_941 where AufNr ='" + NVE + "'"
                        if len(POD) > 0 or len(IMAGE) >0:
                            print( sql_select)
                            server="srv-db1"
                            user = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
                            password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
                            db_name="WinSped"
                            db = pymssql.connect(server, user, password, db_name)
                            cursor = db.cursor(as_dict=True)
                            cursor.execute(sql_select)
                            for row in cursor:
                                TourNr = str(row['TourNr'])
                                BordNr = str(row['BordNr'])
                                KunEmpSpedName1 = str(row['KunEmpSpedName1'])
                                KunEmpSpedStrasse = str(row['KunEmpSpedStrasse'])
                                KunEmpSpedLKZ = str(row['KunEmpSpedLKZ'])
                                KunEmpSpedPLZ = str(row['KunEmpSpedPLZ'])
                                KunEmpSpedOrt = str(row['KunEmpSpedOrt'])
                                AufNr = str(row['AufNr'])
                                RefNr = str(row['RefNr'])
                                KfzZugID = str(row['KfzZugID'])
                                NVE = str(row['NVE'])
                                KunAbsName1 = str(row['KunAbsName1'])
                                KunAbsStrasse = str(row['KunAbsStrasse'])
                                KunAbsLKZ = str(row['KunAbsLkz'])
                                KunAbsPLZ = str(row['KunAbsPlz'])
                                KunAbsOrt = str(row['KunAbsOrt'])
                                LiefNr = str(row['LiefNr'])
                                KunFFDlINr = str(row['KunFFDlINr'])
                                AufNVEAnz = str(row['AufNVEAnz'])
                                AufTatsGewSum = str(row['AufTatsGewSum'])
                                AufVPEAnz = str(row['AufVPEAnz'])
                                AufSollVPEAnz = str(row['AufSollVPEAnz'])
                                now = datetime.now()
                                table = f'''<table border="0" align="center" width="50%">
                                <thead><tr><th width="30%">Header 1</th><th width="70%">header 2</th></tr></thead>
                                <tbody>
                                <tr><td>{AufNr}</td><td>cell 2</td></tr>
                                <tr><td>{AufNr}</td><td>cell 3</td></tr>
                                </tbody>
                                </table>'''
                                print (tabele)



#************************************************************************************************************************************************                          
                        else:
                            print (NVE, TYPE , TIME ,  PODName, DRIVER, POD, IMAGE )
#*************************************************************************************************************************   
            except:
                continue
            #file_2.write(fm + '\n')
            file_2.close()
WRITELOG('END')    
