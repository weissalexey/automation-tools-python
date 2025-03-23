"""
Script: TJW_POD_.py
Description: [ADD DESCRIPTION HERE]
Usage: python TJW_POD_.py
"""

import xml.etree.ElementTree as ET
import urllib.request
import os, time, sys
import datetime
import time
from pathlib import Path
import pymssql
from datetime import datetime
from decimal import Decimal  

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
            #WRITELOG(fm + ' ist schon Da' )
        else:
            #WRITELOG (fm + ' ist nicht Da' )
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
                            PDF_DAT = y.attrib['PDF']
                            print (1)
                            file_path_Name = mypath + "/Image/" + NVE +'_PDF'+ ".pdf"
                            print (file_path_Name)
                            urllib.request.urlretrieve(PDF_DAT, file_path_Name)
                        except:
                            PDF_DAT = ''         
                        try:     
                            POD = y.attrib['POD']
                            file_path_Name = mypath + "\\Image\\" + NVE +'_SIGN'+ ".PNG"
                            urllib.request.urlretrieve(POD, file_path_Name)
                        except:
                            POD = ''
                        try:
                            IMAGE = y.attrib['IMAGE']
                            file_path_Name = mypath + "\\Image\\" + NVE +'_IMAGE'+ ".JPG"
                            urllib.request.urlretrieve(IMAGE, file_path_Name)
                        except:
                            IMAGE = ''         
                            
                        try: 
                            PODName = y.attrib['PODName']
                        except:
                            PODName = ''
                        try:     
                            DRIVER = y.attrib[ 'Driver']
                        except:
                            DRIVER = ''
                        file_2.write(fm + '\n')
                        print (PDF_DAT, NVE, TYPE , TIME ,  PODName, DRIVER, POD, IMAGE)
                        #***********************************************************************************************************************
                        #************************************************************************************************************************************************                          
            except:
                continue
            file_2.close()
WRITELOG('END')    
