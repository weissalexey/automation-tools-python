"""
Script: PODG.py
Description: [ADD DESCRIPTION HERE]
Usage: python PODG.py
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
# import third party libraries:
#from borb.pdf import Document
#
##from borb.pdf.document import Document
#from borb.pdf.page.page import Page
##from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
#from borb.pdf.canvas.layout.page_layout.multi_column_layout import MultiColumnLayout
#from borb.pdf.canvas.layout.image.image import Image
#from borb.pdf.pdf import PDF
#from borb.pdf.canvas.layout.table.flexible_column_width_table import FlexibleColumnWidthTable
#from borb.pdf import Paragraph
#from borb.pdf.canvas.layout.table.table import Table, TableCell
#from borb.pdf.canvas.color.color import HexColor

mypathIN = r"//SRV-WSS/Schnittstellen/DansckDistribution/in/Image/"
#mypathIN = r"//SRV-WSS/Schnittstellen/_Scripte/py/DD/test/image/"
mypathOUT = r"//SRV-WSS/Schnittstellen/GetMyInvoices/PDF/"
LIST_PATCH = '//srv-wss/Schnittstellen/DansckDistribution/all_POD_Files.txt'
server="srv-db1"
user = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
db_name="WinSped"
Conter = 0
sql_select = ''


def STATUSMAIKER (AufNr, fm):
    RANDOMZHAL = str(random.random()).replace(".","")
    STATpatch = "//srv-wss/Schnittstellen/DansckDistribution/out/LIS_IN_IN/"
    #STATpatch = "e:/_Scripte/py/VTL/STAT/"
    now = strftime("%Y%m%d%H%M%S", gmtime())
    Dt = strftime("%Y%m%d", gmtime())
    St = strftime("%H%M", gmtime())
    var = f'''START|646VTLSTAT-{RANDOMZHAL}|{Dt}|||DDISTR|||Carstensen||||||||||||
STATUS|646VTLSTAT-{RANDOMZHAL}||{AufNr}||||{STNUM}||||{Dt}|{St}||||||||||||||||||||||||||||||||||||
ENDE|646VTLSTAT-{RANDOMZHAL}|0|0|0|0|0|0|1|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|
'''
    with open(f'{STATpatch}{RANDOMZHAL}.txt', 'a') as out:
        print (f'{STATpatch}{RANDOMZHAL}.txt')
        out.write(var)
        
def Create_Telematic(AufNr, fm, Conter):
    
    RANDOMZHAL = str(random.random()).replace(".","")
    STATpatch = "//srv-wss/Schnittstellen/DansckDistribution/out/LIS_IN_IN/"
    #STATpatch = "e:/_Scripte/py/VTL/STAT/"
    now = strftime("%Y%m%d%H%M%S", gmtime())
    Dt = strftime("%Y%m%d", gmtime())
    St = strftime("%H%M%S", gmtime())
    TelematicMsgId = SQLAbfrage('select min(TelematicMsgId) - 1  as AUFF from XXAV_TelematicForwardMsgQ') if not None else ''
    KfzAnhID = SQLAbfrage(f'select KfzAnhID  as AUFF from XXASLAuf where aufnr = {AufNr}') if not None else '9999'
    TourNr = SQLAbfrage(f'select TourNr  as AUFF from XXASLAuf where aufnr = {AufNr}') if not None else ''
    LiefNr = SQLAbfrage(f'select LiefNr  as AUFF from XXASLAuf where aufnr = {AufNr}') if not None else ''
    KommNr = SQLAbfrage(f'select KommNr  as AUFF from XXASLAuf where aufnr = {AufNr}') if not None else ''
    msg = f"715|{Dt}|{St}|{KfzAnhID}|{TelematicMsgId}|||GeoPosDate={Dt}|GeoPosTime={St}|TourNr={TourNr}|SIGNFILE=PIX/{fm}|||||LiefNr={LiefNr}|||||||||||||||||Für Details hier klicken=Für Details hier klicken|Auftrag=Auftrag|telematik_EmpState=1|"
    try:
        print (f'//srv-wss/Schnittstellen/_Scripte/py/DD/test/TELEMATIK/msg_{now}_{RANDOMZHAL}.xml')
        
        with open(f'//srv-wss/Schnittstellen/_Scripte/py/DD/test/TELEMATIK/msg_{now}_{RANDOMZHAL}.xml', 'a') as out:
            out.write(msg)
            out.close
        
        #shutil.move(mypathIN + FileNAME,'//srv-tel/Spedion/IN/PIX/')
        print(FileNAME)
        shutil.move( mypathIN + fm,'//srv-wss/Schnittstellen/_Scripte/py/DD/test/TELEMATIK/PIX/')
        print(1)
        return 1
    except:
        print (0)
        return 0

def SQLAbfrage(FB_NR):
    #sql_select = f"select AufNr from XXASLAuf  where  LiefNr = '{FBNR}' or KommNr = '{FBNR}'"
    db1 = pymssql.connect(server, user, password, db_name)
    cursor_1 = db1.cursor(as_dict=True)
    print (FB_NR)
    cursor_1.execute(FB_NR)
    for row_1 in cursor_1:
        Auf_Nr = str(row_1['AUFF']) if not None else ''
    return Auf_Nr

def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
        case _:
            return "Something's wrong with the internet"

def dict_ins( d, key, value ):
    d[key] = (value)

def create_pdf (AufNr, FileNAME, Conter):

    print(AufNr, FileNAME, Conter)
    sql_select = "select top 1 * from XXAV_drAbliefNWSL where AufNr ='" + AufNr + "'"
    db = pymssql.connect(server, user, password, db_name)
    cursor = db.cursor(as_dict=True)
    try:
        cursor.execute(sql_select)
    except:
        print ('Fehler eingetroffen')
    for row in cursor:
        Tour_Nummer = str(row['TourNr'])
        EMPreceipt_details = {"Empfänger: ":"" }
        KunEmpSpedName1 = str(row['KunEmpName1'])
        LANDE= len(KunEmpSpedName1)
        if LANDE > 16:
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
        
        AufTatsGewSum = str(row['TatsGew'])
        AufVPEAnz = str(row['VpeAnz'])
        Inhalt = str(row['Inhalt'])
        now = (row['BelBisDat']) if row['BelBisDat'] is not None else row['BelVonDat']
        now1 =(row['BelBisZeit']) if row['BelBisZeit'] is not None else row['BelVonZeit']
        
        DtSt = str(now.strftime("%d-%m-%Y"))
        MiSt = str(now1.strftime("%H:%M"))
        print (AufNr)
    try:
        pagename = mypathOUT + AufNr + "_"  + str(Conter) +  ".PDF"
        c = canvas.Canvas(pagename, pagesize=letter)
        width, height = letter
        y = height - 100  # Starting Y position
        Hader = ImageReader('Hader.png')
        c.drawImage(Hader, 0,  y - 65 , width=650, height=200, preserveAspectRatio=True, mask='auto')
        c.setFont("Helvetica", 14)
        c.drawCentredString((width / 2) +50, y - 60 , "ABLIEFERNACWEIS")
        c.setFont("Helvetica", 11)
        c.drawCentredString((width / 2) +46, y - 75 , "Tour Nummer: " + Tour_Nummer)
        c.drawCentredString((width / 2) +50, y - 85 , "Auftrag Nummer: " + AufNr)
        c.setFont("Helvetica", 10)
        c.drawCentredString(100, y - 60, "Chr.Carstensen Logistics GmbH & Co.KG")
        c.drawCentredString(49, y - 70, 'Am Güterbanhof 2')
        c.drawCentredString(50, y - 80, 'D 24976 Handewitt')
        y = y - 200
        y1 = y 

        c.setFont("Helvetica-Bold", 11)
        for key, value in EMPreceipt_details.items():
            c.drawString(180, y, f"{key}{value}")
            c.setFont("Helvetica", 10)
            y -= 12  
        y = y1
        c.setFont("Helvetica-Bold", 11)
        for key, value in ABS_details.items():
            c.drawString(30, y, f"{key}{value}")
            c.setFont("Helvetica", 10)
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
        Footer = ImageReader('Footer.png')
        c.drawImage(Footer, -20,  -10 , width=650, height=100, preserveAspectRatio=True, mask='auto')
        c.save()
        print(f"Delivery receipt saved to {pagename}")
        return 1

    except:
        print(f"Nicht geklapt {pagename}")
        return 0

if __name__ == "__main__":
    print ('Begin')
    XXXXX = 0
    filenames = next(walk(mypathIN), (None, None, []))[2]  # [] if no file
    for fm in filenames:
        FNNVE = fm.split('_',1)[0]
        RAS= fm.split('.',1)[1]
        Conter += 1 
        sql_select = f"select top 1 AufNr from XXASLAuf where AufArt != 'D' and AufIntNr in (select AufIntNr from XXANVE Where NVE = '{FNNVE}')" if len(FNNVE)== 20 else sql_select
        sql_select = "select top 1 AufNr from XXASLAuf as SLAuf left join  XXAAufExt TT on SLAuf.AufIntNr = TT.AufIntNr where AufArt != 'D'and TrackandTraceEmail  = '" + str(FNNVE) + "'" if len(FNNVE)== 18 else sql_select
        sql_select = f"select top 1 AufNr from XXASLAuf as SLAuf left join  XXAAufExt TT on SLAuf.AufIntNr = TT.AufIntNr where AufArt != 'D'and TrackandTraceEmail  = '" + str(FNNVE)[:-4] + "'" if len(FNNVE)== 22 else sql_select
        sql_select = f"select top 1 AufNr from XXASLAuf as SLAuf left join  XXAAufExt TT on SLAuf.AufIntNr = TT.AufIntNr where AufArt != 'D'and TrackandTraceEmail  = '" + str(FNNVE)[1:-5] + "'" if len(FNNVE)== 24 else  sql_select
        db1 = pymssql.connect(server, user, password, db_name)
        cursor1 = db1.cursor(as_dict=True)
        cursor1.execute(sql_select)
        for row1 in cursor1:
            FileNAME = mypathIN + fm
            file_extension = fm[-4:]
            print (file_extension)
            AufNr = str(row1['AufNr']) if not None else ''
        
            if file_extension != '.PNG':
                FF_name = f'//SRV-WSS/Schnittstellen/GetMyInvoices/PDF/{AufNr}_{Conter}{file_extension}'
                print (FF_name)
                shutil.copy2(FileNAME , FF_name)
                XXXXX = 1
            else:
                XXXXX = create_pdf (AufNr, FileNAME, Conter)
        if XXXXX > 0:
            try:
                shutil.move(mypathIN + fm,'//srv-wss/Schnittstellen/DansckDistribution/in/BCK/')
            except:
                os.remove(mypathIN + fm)
        else: 
            try:
                shutil.move(mypathIN + fm,'//srv-wss/Schnittstellen/DansckDistribution/in/ERROR_IMG/')
            except:
                os.remove(mypathIN + fm)
            

print ('Ende')