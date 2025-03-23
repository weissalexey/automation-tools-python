"""
Script: newXML_.py
Description: [ADD DESCRIPTION HERE]
Usage: python newXML_.py
"""

import xml.etree.ElementTree as ET
import urllib.request
import os, time, sys
import datetime
#import borb
from datetime import datetime
import time
from pathlib import Path
import pymssql
from datetime import datetime
from borb.pdf import Document
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf import Paragraph
#from borb.pdf.document.document import Document
from borb.pdf import PDF
from borb.pdf.canvas.layout.table.flexible_column_width_table import FlexibleColumnWidthTable
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.table.table import TableCell  
#from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.pdf.canvas.color.color import HexColor  
from decimal import Decimal  

mypath = r"//srv-wss/Schnittstellen/TJW/INBCK"
LIST_PATCH = r"//srv-wss/Schnittstellen/_Scripte/py/TJW_POD/PODAUFN_.txt"
from os import walk

def STATUSMAIKER (AufNr,NVE ,TIME, TYPE):
    STATpatch = "//srv-wss/Schnittstellen/TJW/IN/"
    #now = datetime.now()
    DtSt = str(TIME[:10].replace('-',''))
    DtSt = str(DtSt[-4:]+DtSt[3:4]+DtSt[:2])
    DtMt = str(TIME[-8:].replace(':',''))
    DtMt = str(DtMt[:4])
    var = f'''START|58fceae1-{NVE}|{DtSt}|||TJW|||CARSTENSEN||||||||||||
STATUS|58fceae1-{NVE}||{AufNr}||||{TYPE}||||{DtSt}|{DtMt}||||||||||||||||||||||||||||||||||||
ENDE|58fceae1-{NVE}|0|0|0|0|0|0|1|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|
31012024
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
            WRITELOG(fm + ' ist schon Da' )
        else:
            WRITELOG (fm + ' ist nicht Da' )
            file_2 = open(LIST_PATCH, 'a')
            #file_2.write(fm + '\n')
            file_2.close()
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
                        except:
                            IMAGE = ''         
                        try:     
                            POD = y.attrib['POD']
                            file_path_Name = mypath + "\\Image\\" + NVE +'_SIGN'+ ".PNG"
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
                            sql_select = "select *  from XXAV_drLabelGenSL_941 where NVE= '" + NVE + "'"
                        else:
                            sql_select = "select * from XXAV_drLabelGenSL_941 where AufNr ='" + NVE + "'"
                                                
                        if len(POD) > 0 or len(IMAGE) >0:
#************************************************************************************************************************************************                            
                            #print( sql_select)
                            pdf = Document()
                            page = Page()
                            pdf.add_page(page)
                            layout = SingleColumnLayout(page)
#************************************************************************************************
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
                            
                                tetxtstr = f""" Tour Nummer:\t{TourNr} 
                                                Bordero Nummer:\t{BordNr}
                                                Auftrags Nummer:\t{AufNr}
                                                REferenz Nummer:\t{RefNr}
                                                LKW Nummer:\t{KfzZugID}
                                                NVE Nummer:\t{NVE}
                                            """
                            #*********************************************************************************************************
                            layout.add(
                                FlexibleColumnWidthTable(number_of_columns=1, number_of_rows=1, )
                            
                                .add(
                                    Paragraph(
                                        tetxtstr ,
                                        padding_top=Decimal(12),
                                        respect_newlines_in_text=True,
                                        font_color=HexColor("#666666"),
                                        font_size=Decimal(10),
                                    )
                                )
                                
                                .no_borders()
                            )
                            
                            tetxtstr = f"""
                                        {KunEmpSpedName1} 
                                        {KunEmpSpedPLZ} {KunEmpSpedStrasse}
                                        {KunEmpSpedLKZ} {KunEmpSpedOrt}
                                    """
                            tetxtstr1 = f"""
                                        {KunAbsName1} 
                                        {KunAbsPLZ} {KunAbsStrasse}
                                        {KunAbsLKZ} {KunAbsOrt}
                                    """           
                            
                            layout.add(
                                FlexibleColumnWidthTable(number_of_columns=5, number_of_rows=1, )
                            
                                .add(
                                    Paragraph(
                                        tetxtstr ,
                                        padding_top=Decimal(12),
                                        respect_newlines_in_text=True,
                                        font_color=HexColor("#666666"),
                                        font_size=Decimal(10),
                                    )
                                )
                                
                                .add(
                                    Paragraph(
                                        "Fragthr",
                                        border_radius_top_left=Decimal(5),
                                        border_radius_top_right=Decimal(5),
                                        border_radius_bottom_left=Decimal(5),
                                        border_radius_bottom_right=Decimal(5),
                                        font_color=HexColor("#ffffff"),
                                        font_size=Decimal(14),
                                    )    
                                )
                                
                                .add(
                                    Paragraph(
                                        "Fragthr",
                                        border_radius_top_left=Decimal(5),
                                        border_radius_top_right=Decimal(5),
                                        border_radius_bottom_left=Decimal(5),
                                        border_radius_bottom_right=Decimal(5),
                                        font_color=HexColor("#ffffff"),
                                        font_size=Decimal(14),
                                    )    
                                )
                                
                                .add(
                                    Paragraph(
                                        "Fragthr",
                                        border_radius_top_left=Decimal(5),
                                        border_radius_top_right=Decimal(5),
                                        border_radius_bottom_left=Decimal(5),
                                        border_radius_bottom_right=Decimal(5),
                                        font_color=HexColor("#ffffff"),
                                        font_size=Decimal(14),
                                    )    
                                )
                                
                                .add(
                                    Paragraph(
                                        tetxtstr1 ,
                                        padding_top=Decimal(12),
                                        respect_newlines_in_text=True,
                                        font_color=HexColor("#666666"),
                                        font_size=Decimal(10),
                                    )
                                )
                                
                                .no_borders()
                            )
                            #*************************************************************************************************
                            t = FlexibleColumnWidthTable(number_of_columns=1, number_of_rows=1, )
                            t.add(TableCell(Paragraph("KunFFDlINr",font_color=HexColor("#ffffff")))).no_borders()
                            layout.add(t)
                            t = FlexibleColumnWidthTable(number_of_columns=5, number_of_rows=2, )
                            
                            # Header row
                            t.add(TableCell(Paragraph("KunFFDlINr",font_color=HexColor("#666666"))))
                            t.add(TableCell(Paragraph("AufNVEAnz", font_color=HexColor("#666666"))))
                            t.add(TableCell(Paragraph("AufTatsGewSum",font_color=HexColor("#666666"))))
                            t.add(TableCell(Paragraph("AufVPEAnz", font_color=HexColor("#666666"))))
                            t.add(TableCell(Paragraph("AufSollVPEAnz",font_color=HexColor("#666666"))))
                                # Data rows
                            t.add(Paragraph(f'{KunFFDlINr}', font_color=HexColor("#666666")))    
                            t.add(Paragraph(f'{AufNVEAnz}', font_color=HexColor("#666666")))   
                            t.add(Paragraph(f'{AufTatsGewSum}', font_color=HexColor("#666666")))   
                            t.add(Paragraph(f'{AufVPEAnz}', font_color=HexColor("#666666")))   
                            t.add(Paragraph(f'{AufSollVPEAnz}', font_color=HexColor("#666666")))       
                            
                            # Set padding
                            t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5)).no_borders()
                            layout.add(t)
                            
                            #**************************************************************************************************
                            # Новые import
                            t = FlexibleColumnWidthTable(number_of_columns=2, number_of_rows=2, )
                            t.add(TableCell(Image(POD,width=Decimal(128),height=Decimal(128),)))
                            t.add(TableCell(Image(IMAGE,width=Decimal(300),height=Decimal(300),)))
                            t.add(Paragraph(f'{PODName}', font_color=HexColor("#666666")))   
                            t.add(Paragraph(f'{TIME}', font_color=HexColor("#666666")))   
                            t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5)).no_borders()
                            layout.add(t)
                            
                            
                            #************************************************************************************************
                            WRITELOG(f"//srv-wss/Schnittstellen/GetMyInvoices/PDF/{AufNr}.pdf")
                            with open(Path(f"//srv-wss/Schnittstellen/GetMyInvoices/PDF/{AufNr}.pdf"), "wb") as pdf_file_handle:
                            #with open(Path(f"{AufNr}.pdf"), "wb") as pdf_file_handle:
                                PDF.dumps(pdf_file_handle, pdf)
                            #STATUSMAIKER (AufNr,NVE ,TIME, TYPE)
                            #************************************************************************************************************************************************                          
                        else:
                            print (NVE, TYPE , TIME ,  PODName, DRIVER, POD, IMAGE )
                        
                     #*************************************************************************************************************************   
            except:
                continue

WRITELOG('END')    
