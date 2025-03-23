"""
Script: TESTER.py
Description: [ADD DESCRIPTION HERE]
Usage: python TESTER.py
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import shutil
from os import walk
from pathlib import Path
from decimal import Decimal
import pymssql
import random
import datetime
import time
import random, string
from time import gmtime , strftime

mypathIN = r"c:/Users/aw/Desktop/PY/"
#mypathIN = r"//SRV-WSS/Schnittstellen/_Scripte/py/DD/test/image/"
mypathOUT = r"c:/Users/aw/Desktop/PY/"
LIST_PATCH = '//srv-wss/Schnittstellen/DansckDistribution/all_POD_Files.txt'
server="srv-db1"
user = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
db_name="WinSped"
Conter = 0
sql_select = ''

def dict_ins( d, key, value ):
    d[key] = (value)

def create_pdf (AufNr, FileNAME, Conter):


    sql_select = "select top 1 * from XXAV_drAbliefNWSL where AufNr ='" + AufNr + "'"
    db = pymssql.connect(server, user, password, db_name)
    cursor = db.cursor(as_dict=True)
    try:
        print(sql_select)
        cursor.execute(sql_select)
    except:
        print ('Xe-XE')
    
    for row in cursor:
        
        Tour_Nummer = str(row['TourNr'])


        #EMPreceipt_details = {"Empfänger: ", ""}
        EMPreceipt_details = {"Empfänger: ":"" }
        
        KunEmpSpedName1 = str(row['KunEmpName1'])
        LANDE= len(KunEmpSpedName1)
        if LANDE > 16:
            #print(KunEmpSpedName1[:16])
            dict_ins(EMPreceipt_details, KunEmpSpedName1[:16], '')
            dict_ins(EMPreceipt_details,KunEmpSpedName1[-LANDE + 16:], '')
        else : 
            dict_ins(EMPreceipt_details, KunEmpSpedName1, '')
            
            
        KunEmpSpedStrasse = str(row['KunEmpStrasse'])
        LANDE= len(KunEmpSpedStrasse)
        if LANDE > 16:
            dict_ins(EMPreceipt_details,KunEmpSpedStrasse[:16],"")
            dict_ins(EMPreceipt_details,KunEmpSpedStrasse[-LANDE + 16:],"")
        else : 
            dict_ins(EMPreceipt_details, KunEmpSpedStrasse, "")
        
        KunEmpSpedLKZ = str(row['EmgLKZ'])
        KunEmpSpedPLZ = str(row['EmgPLZ'])
        KunEmpSpedOrt = str(row['EmgOrt'])
        
        LPO = KunEmpSpedLKZ + " " +  KunEmpSpedPLZ + " " + KunEmpSpedOrt
        LANDE= len(LPO) 
        
        if LANDE > 16:
            dict_ins( EMPreceipt_details,LPO[:16], "")
            dict_ins( EMPreceipt_details,LPO[-LANDE + 16:],"")
        else:
            dict_ins( EMPreceipt_details, LPO, "")
        #NAM = {"Empfänger: ": "" }
        #EMPreceipt_details = NAM, KunEmpSpedName1 , KunEmpSpedStrasse,LPO
        
        ABS_details = {"Absender: ":"" }
        
        KunAbsName1 = str(row['KunAbsName1'])
        
        LANDE= len(KunAbsName1)
        if LANDE > 27:
            dict_ins(ABS_details,KunAbsName1[:27], "")
            dict_ins(ABS_details,KunAbsName1[-LANDE + 27:],"")
        else : 
            dict_ins(ABS_details,KunAbsName1, "")
        
        
        KunAbsStrasse = str(row['KunAbsStrasse'])
        
        LANDE= len(KunAbsStrasse)
        if LANDE > 27:
            dict_ins(  ABS_details,KunAbsStrasse[:27], "")
            dict_ins( ABS_details,KunAbsStrasse[-LANDE + 27:],"")
        else : 
            dict_ins( ABS_details,KunAbsStrasse, "")
            
        KunAbsLKZ = str(row['AbgLKZ'])
        KunAbsPLZ = str(row['AbgPLZ'])
        KunAbsOrt = str(row['AbgOrt'])
        LPO = KunAbsLKZ + " " +  KunAbsPLZ + " " + KunAbsOrt
        LANDE= len(LPO)

        if LANDE > 27:
            dict_ins(  ABS_details,LPO[:27], "")
            dict_ins(  ABS_details,LPO[-LANDE + 27:],"")
        else : 
            dict_ins(  ABS_details,LPO, "")
        
        RefNr = str(row['RefNr'])
        LiefNr = str(row['LiefNr'])
        FRACT = "Chr.Carstensen Logistics GmbH & Co.KG"
        KfzZugID = str(row['KfzZugID'])
        
        AUF_details = {"Referenz Nummer":RefNr , 'Lieferschein-NR.': LiefNr, 'Frachtfürer' : FRACT ,'LKW Nummer': KfzZugID }
        
#         KunFFDlINr = str(row['KunFFDlINr'])
#         AufNVEAnz = str(row['NVEAnz'])
        AufTatsGewSum = str(row['TatsGew'])
        AufVPEAnz = str(row['VpeAnz'])
#         AufSollVPEAnz = str(row['AufSollVPEAnz'])
        Inhalt = str(row['Inhalt'])
        now = (row['BelBisDat'])
        now1 =(row['BelBisZeit'])
        
        DtSt = str(now.strftime("%d-%m-%Y"))
        MiSt = str(now1.strftime("%H:%M"))
        print (AufNr)
    pagename = mypathOUT + AufNr + "_"  + str(Conter) +  ".PDF"
    
    c = canvas.Canvas(pagename, pagesize=letter)
    width, height = letter
    y = height - 100  # Starting Y position
    Hader = ImageReader('Hader.png')
    c.drawImage(Hader, 0,  y - 65 , width=650, height=200, preserveAspectRatio=True, mask='auto')
    # Title
    #c.setFont("Helvetica-Bold", 14)
    c.setFont("Helvetica", 14)
    c.drawCentredString((width / 2) +50, y - 60 , "ABLIEFERNACWEIS")
    c.setFont("Helvetica", 11)
    c.drawCentredString((width / 2) +46, y - 75 , "Tour Nummer: " + Tour_Nummer)
    c.drawCentredString((width / 2) +50, y - 85 , "Auftrag Nummer: " + AufNr)
    c.setFont("Helvetica", 10)
    c.drawCentredString(100, y - 60, "Chr.Carstensen Logistics GmbH & Co.KG")
    #c.setFont("Helvetica", 10)
    c.drawCentredString(49, y - 70, 'Am Güterbanhof 2')
    #c.setFont("Helvetica", 10)
    c.drawCentredString(50, y - 80, 'D 24976 Handewitt')
    y = y - 200
    y1 = y 
    c.setFont("Helvetica-Bold", 11)
    for key, value in EMPreceipt_details.items():
        c.drawString(180, y, f"{key}{value}")
        c.setFont("Helvetica", 11)
        y -= 12  
    y = y1
    c.setFont("Helvetica-Bold", 11)
    for key, value in ABS_details.items():
        c.drawString(30, y, f"{key}{value}")
        c.setFont("Helvetica", 11)
        y -= 12  
    y = y1
    for key, value in AUF_details.items():
        c.drawString(290, y, f"{key}: {value}")
        y -= 12  
    y = y - 50
    y1 = y 
    
    c.drawString(30, y, f'Ablieferdatum/-zeit      {DtSt} {MiSt} Uhr')
    y -= 12
    c.drawString(30, y, f'Menge VPE                 {AufVPEAnz.replace('00','0')}')
    y -= 12
    c.drawString(30, y, f'Inhalt                           {Inhalt}')
    y -= 12
    c.drawString(30, y, f'Gew.in kg                    {AufTatsGewSum.replace('00','0')}')
    y -= 250
    signature = ImageReader(FileNAME)

    c.drawImage(signature, 350, y , width=200, height=200, preserveAspectRatio=True, mask='auto')
    print  (y)
    Footer = ImageReader('Footer.png')
    c.drawImage(Footer, -20,  -10 , width=650, height=100, preserveAspectRatio=True, mask='auto')

    c.save()
    print(f"Delivery receipt saved to {pagename}")

    return 1

if __name__ == "__main__":
    
    create_pdf ('10084285', 'c:/Users/aw/Desktop/PY/A0010084285.JPG', 1)