"""
Script: 123.py
Description: [ADD DESCRIPTION HERE]
Usage: python 123.py
"""

import xml.etree.ElementTree as ET
import urllib.request
import os, time, sys
import shutil
import datetime
import time
from pathlib import Path
import pymssql
from datetime import datetime
import urllib.request 
from time import gmtime, strftime


server="srv-db1"
user = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
db_name="WinSped"

mypath = r"//srv-wss/Schnittstellen/DansckDistribution/in/scan/"
mypath_pod = r"//srv-wss/Schnittstellen/DansckDistribution/in/POD/"
LIST_PATCH = r"//srv-wss/Schnittstellen/DansckDistribution/PODAUFN_.txt"

def download_photo(img_url, filename):
    try:
        image_on_web = urllib.urlopen(img_url)
        if image_on_web.headers.maintype == 'image':
            buf = image_on_web.read()
            path = os.getcwd() + DOWNLOADED_IMAGE_PATH
            file_path = "%s%s" % (mypath_pod , filename)
            downloaded_image = file(file_path, "wb")
            downloaded_image.write(buf)
            downloaded_image.close()
            image_on_web.close()
        else:
            return False    
    except:
        return False
    return True

def STATUSMAIKER (AufNr,NVE1 ,TIME, TYPE, AufPosNr):
    STATpatch = "//srv-wss/Schnittstellen/DansckDistribution/out/LIS_IN_IN/"
    now = strftime("%Y%m%d%H%M%S", gmtime())
    DtSt = str(TIME[:10].replace('-',''))
    print (DtSt) 
    DtSt = str(DtSt[-4:]+DtSt[2:4]+DtSt[:2])
    DtMt = str(TIME[-8:].replace(':',''))
    DtMt = str(DtMt[:4])
    var = f'''START|64{DtSt}-{DtMt}-{NVE1}|{DtSt}|||DDISTR|||Carstensen||||||||||||
STATUS|64{DtSt}-{DtMt}-{NVE1}||{AufNr}|{AufPosNr}|||{TYPE}||||{DtSt}|{DtMt}||||||||||||||||||||||||||||||||||||
ENDE|64{DtSt}-{DtMt}-{NVE1}|0|0|0|0|0|0|1|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|
'''
    with open(f'{STATpatch}{now}{DtMt}-{NVE}{TYPE}.txt', 'a') as out:
        out.write(var)


from os import walk

filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file

for fm in filenames:
    with open(LIST_PATCH) as d:
        if str(fm) in d.read(): 
            d.close()
            #print (mypath + fm)
            shutil.copy2(mypath + fm, '//srv-wss/Schnittstellen/DansckDistribution/in/BCK')
            os.remove(mypath + fm)
        else:
            counter = 0
            xml_path = (mypath +'\\'+ fm)
            try:
                #print (mypath +'\\'+ fm)
                mytree = ET.parse(xml_path)
                myroot = mytree.getroot()
                EEE = 2
                #file_2.write(fm + '\n')
                file_2.close()
                shutil.copy2(mypath + fm, '//srv-wss/Schnittstellen/DansckDistribution/in/STAT_ERR')
                os.remove(mypath + fm)
            
            except:
                file_2 = open(LIST_PATCH, 'a')
                file_2.write(fm + '\n')
                file_2.close()
                shutil.copy2(mypath + fm, '//srv-wss/Schnittstellen/DansckDistribution/in/BCK')
                EEE = 1
                print(EEE)
#               continue
            if EEE == 1:
                for x in myroot:
                    NVE = x.attrib['identifier']
                    print(NVE)
                    for y in x:
                       counter += 1
                       TYPE = y.attrib['type']
                       TIME = y.attrib[ 'time']
                       #Print (1)
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
                       
                       try:     
                           TERMINAL = y.attrib[ 'Terminal']
                       except:
                           TERMINAL = ''
                       
                       try:     
                           ArriveETA = y.attrib[ 'ArriveETA']
                       except:
                           ArriveETA = ''
                       try:     
                           TEXT_ = y.attrib[ 'Text']
                       except:
                           TEXT_ = ''
                       if NVE[:2] == '00':
                       #if len(NVE) == 18:
                           print ('NVE')
                           sql_select = "use winsped select AufNr,LiefNr,NVE,AufPosNr from XXAV_drLabelGenSL_941 where NVE ='" + NVE + "' group by AufNr,LiefNr,NVE,AufPosNr "
                           print( sql_select)
                           
                       else:
                           #sql_select = "select *  from XXAV_drLabelGenSL_941 where LiefNr = '" + NVE + "'"
                           sql_select = f"select AufNr,LiefNr,NVE,AufPosNr   from XXAV_drLabelGenSL_941 where LiefNr = '{NVE[:18]}' group by AufNr,LiefNr,NVE,AufPosNr "
                           print( sql_select)
           
                       db = pymssql.connect(server, user, password, db_name)
                       cursor = db.cursor(as_dict=True)
                       cursor.execute(sql_select)
                       AufNr = ''
                       for row in cursor:
                           print(2)
                           AufNr = str(row['AufNr'])
                           NVE1 = str(row['NVE'])
                           LiefNr = str(row['LiefNr'])
                           AufPosNr = str(row['AufPosNr'])
                           print (AufNr, LiefNr , NVE1, TYPE , TIME ,  PODName, DRIVER, POD, IMAGE, TERMINAL, ArriveETA, TEXT_ )
                           
                       if len(AufNr) == 0:
                            #shutil.copy2(mypath + fm, '//srv-wss/Schnittstellen/DansckDistribution/in/BCK')
                            #os.remove(mypath + fm)
                            print (f'UDALIL NACHUI')
                       else:        
                            STATUSMAIKER (AufNr, NVE1 ,TIME, TYPE, AufPosNr )
    