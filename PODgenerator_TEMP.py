"""
Script: PODgenerator_TEMP.py
Description: [ADD DESCRIPTION HERE]
Usage: python PODgenerator_TEMP.py
"""

import os
from os import walk
from pathlib import Path
from decimal import Decimal 
import pymssql
from datetime import datetime
# import third party libraries:
from borb.pdf import Document
from borb.pdf.page.page import Page
#from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.multi_column_layout import MultiColumnLayout
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.pdf import PDF
from borb.pdf.canvas.layout.table.flexible_column_width_table import FlexibleColumnWidthTable
from borb.pdf import Paragraph
from borb.pdf.canvas.layout.table.table import Table, TableCell 
from borb.pdf.canvas.color.color import HexColor  
# NOTICE BELOW THE TYPE IS CONVERTED TO Path using pathlib
 #change to fit your path
mypathIN = r"//SRV-WSS/Schnittstellen/DansckDistribution/in/Image/"
mypathOUT = r"//SRV-WSS/Schnittstellen/GetMyInvoices/PDF/"
LIST_PATCH = '//srv-wss/Schnittstellen/DansckDistribution/all_POD_Files.txt'
server="srv-db1"
user = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
db_name="WinSped"


def create_pdf (AufNr, FileNAME , Conter ):
    IMAGE_PATH = Path('Hader.png')
    pdf = Document()
    page = Page()
    pdf.add_page(page)
    
    doc: Document = Document()

    # get Page width
    w: typing.Optional[Decimal] = page.get_page_info().get_width()
    assert w is not None

    # set a PageLayout
    layout = MultiColumnLayout(page,column_widths=[w - Decimal(100)],margin_top=Decimal(20),margin_right=Decimal(20),margin_bottom=Decimal(20),margin_left=Decimal(65),)
    
    
    #layout = SingleColumnLayout(page, margin_top=Decimal(20),margin_right=Decimal(20),margin_bottom=Decimal(20),margin_left=Decimal(20),)
    t = Image(image=IMAGE_PATH, width=448, height=100) #change the size as you wish
    #t = Image(image=IMAGE_PATH,) #change the size as you wish
    layout.add(t)

    #NVE = '10084285'
    sql_select = "select top 1 * from XXAV_drAbliefNWSL where AufNr ='" + AufNr + "'"
    db = pymssql.connect(server, user, password, db_name)
    cursor = db.cursor(as_dict=True)
    try:
        print(sql_select)
        cursor.execute(sql_select)
    except:
        print ('Xe-XE')
    
    for row in cursor:
        TourNr = str(row['TourNr'])
#        BordNr = str(row['BordNr'])
        KunEmpSpedName1 = str(row['KunEmpName1'])
        KunEmpSpedStrasse = str(row['KunEmpStrasse'])
        KunEmpSpedLKZ = str(row['EmgLKZ'])
        KunEmpSpedPLZ = str(row['EmgPLZ'])
        KunEmpSpedOrt = str(row['EmgOrt'])
        AufNr = str(row['AufNr'])
        RefNr = str(row['RefNr'])
        KfzZugID = str(row['KfzZugID'])
#         NVE = str(row['NVE'])
        KunAbsName1 = str(row['KunAbsName1'])
        KunAbsStrasse = str(row['KunAbsStrasse'])
        KunAbsLKZ = str(row['AbgLKZ'])
        KunAbsPLZ = str(row['AbgPLZ'])
        KunAbsOrt = str(row['AbgOrt'])
        LiefNr = str(row['LiefNr'])
#         KunFFDlINr = str(row['KunFFDlINr'])
#         AufNVEAnz = str(row['NVEAnz'])
        AufTatsGewSum = str(row['TatsGew'])
        AufVPEAnz = str(row['VpeAnz'])
#         AufSollVPEAnz = str(row['AufSollVPEAnz'])
        Inhalt = str(row['Inhalt'])
        now = (row['BelBisDat'])
        now1 =(row['BelBisZeit'])
        #now = datetime.now()
        DtSt = str(now.strftime("%d-%m-%Y"))
        MiSt = str(now1.strftime("%H:%M"))
        print (AufNr)
    if  len(AufNr) == 8:   
        #************************************************************************************************
        #NVE = '340502690000023132'
        tetxtstr = 'Chr. Carstensen Logistics GmbH & Co. KG'
        LANGER_TEXT = ''
        tetxtstr1 = 'Abliefernachweis'
        if len(LANGER_TEXT) == 0:
            ZHALL = 56 - len(tetxtstr)
            LANGER_TEXT = f'{tetxtstr:{'T'}{'<'}{ZHALL}}'
        
            #create_pdf ('Hader.png')
            
            t = FlexibleColumnWidthTable(number_of_columns=3, number_of_rows=3, )
            tetxtstr = 'Chr. Carstensen Logistics GmbH & Co. KG'
            LANGER_TEXT = ''
            tetxtstr1 = 'Abliefernachweis'
            # Header row
            t.add(TableCell(Paragraph(tetxtstr,font_color=HexColor("#0b0d0f"), font_size=Decimal(10))))
            t.add(TableCell(Paragraph(LANGER_TEXT,font_color=HexColor("#ffffff"), font_size=Decimal(8))))
            t.add(TableCell(Paragraph(tetxtstr1, font_color=HexColor("#0b0d0f"), font_size=Decimal(14))))
            # Data rows
            tetxtstr = 'Am Güterbanhof 2'
            tetxtstr1 = 'Tour Nummer:' + TourNr
            LANGER_TEXT = 'LANGER_TEXT'
            if len(LANGER_TEXT) == 0:
                ZHALL = 56 - len(tetxtstr)
                LANGER_TEXT = f'{tetxtstr:{'T'}{'<'}{ZHALL}}'
                
            t.add(Paragraph(tetxtstr, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))    
            t.add(Paragraph(LANGER_TEXT, font_color=HexColor("#ffffff"), font_size=Decimal(10)))   
            t.add(Paragraph(tetxtstr1, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))   
            
            tetxtstr = 'D 24976 Handewitt'
            tetxtstr1 = 'Auftrags Nummer:' + AufNr
            LANGER_TEXT = 'LANGER_TEXT'
            if len(LANGER_TEXT) == 0:
                ZHALL = 56 - len(tetxtstr)
                LANGER_TEXT = f'{tetxtstr:{'T'}{'<'}{ZHALL}}'
                
            t.add(Paragraph(tetxtstr, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))    
            t.add(Paragraph(LANGER_TEXT, font_color=HexColor("#ffffff"), font_size=Decimal(10)))   
            t.add(Paragraph(tetxtstr1, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))   
            
            # Set padding
            t.set_padding_on_all_cells(Decimal(1), Decimal(1), Decimal(1), Decimal(5)).no_borders()
            layout.add(t)
            
            
        t = FlexibleColumnWidthTable(number_of_columns=3, number_of_rows=3, )
        tetxtstr = ''
        LANGER_TEXT = ''
        tetxtstr1 = ''
        # Header row
        t.add(TableCell(Paragraph(tetxtstr,font_color=HexColor("#0b0d0f"), font_size=Decimal(10))))
        t.add(TableCell(Paragraph(LANGER_TEXT,font_color=HexColor("#ffffff"), font_size=Decimal(8))))
        t.add(TableCell(Paragraph(tetxtstr1, font_color=HexColor("#0b0d0f"), font_size=Decimal(14))))

        # Data rows
        tetxtstr = ''
        tetxtstr1 = '' 
        LANGER_TEXT = ''
        if len(LANGER_TEXT) == 0:
            ZHALL = 56 - len(tetxtstr)
            LANGER_TEXT = f'{tetxtstr:{'T'}{'<'}{ZHALL}}'
            
        t.add(Paragraph(tetxtstr, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))    
        t.add(Paragraph(LANGER_TEXT, font_color=HexColor("#ffffff"), font_size=Decimal(10)))   
        t.add(Paragraph(tetxtstr1, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))   
        
        tetxtstr = ''
        tetxtstr1 = ''
        LANGER_TEXT = ''
        if len(LANGER_TEXT) == 0:
            ZHALL = 56 - len(tetxtstr)
            LANGER_TEXT = f'{tetxtstr:{'T'}{'<'}{ZHALL}}'
            
        t.add(Paragraph(tetxtstr, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))    
        t.add(Paragraph(LANGER_TEXT, font_color=HexColor("#ffffff"), font_size=Decimal(10)))   
        t.add(Paragraph(tetxtstr1, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))   
        
        # Set padding
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5)).no_borders()
        layout.add(t)
        ##################################################################################################
        #*************************************************************************************************
        #t = FlexibleColumnWidthTable(number_of_columns=1, number_of_rows=1, )
        #t.add(TableCell(Paragraph("KunFFDlINr",font_color=HexColor("#ffffff")))).no_borders()
        #layout.add(t)
        t = FlexibleColumnWidthTable(number_of_columns=3, number_of_rows=7, )
        tetxtstr = 'Absender:'
        LANGER_TEXT = 'Empfanger:'
        tetxtstr1 = ' '
        # Header row
        t.add(TableCell(Paragraph(tetxtstr,font_color=HexColor("#0b0d0f"), font_size=Decimal(10))))
        t.add(TableCell(Paragraph(LANGER_TEXT,font_color=HexColor("#0b0d0f"), font_size=Decimal(10))))
        t.add(TableCell(Paragraph(tetxtstr1, font_color=HexColor("#0b0d0f"), font_size=Decimal(10))))
        # Data rows
        tetxtstr = KunAbsName1
        LANGER_TEXT = KunEmpSpedName1 
        tetxtstr1 = f'Referenz Nummer:{RefNr}' 
        
            
        t.add(Paragraph(tetxtstr, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))    
        t.add(Paragraph(LANGER_TEXT, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))   
        t.add(Paragraph(tetxtstr1, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))   
        
        tetxtstr = KunAbsStrasse
        LANGER_TEXT = KunEmpSpedStrasse
        tetxtstr1 = f'Lieferschein-NR.:{LiefNr}'
        
        t.add(Paragraph(tetxtstr, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))    
        t.add(Paragraph(LANGER_TEXT, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))   
        t.add(Paragraph(tetxtstr1, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))   
        
        tetxtstr = f'{KunAbsLKZ} {KunAbsPLZ} {KunAbsOrt} '
        LANGER_TEXT = f'{KunEmpSpedLKZ} {KunEmpSpedPLZ} {KunEmpSpedOrt} '
        tetxtstr1 = 'Frachtführer: Chr.Carstensen Logistics GmbH&Co.KG'
        
        t.add(Paragraph(tetxtstr, font_color=HexColor("#0b0d0f"), font_size=Decimal(10),respect_newlines_in_text= False))    
        t.add(Paragraph(LANGER_TEXT, font_color=HexColor("#0b0d0f"), font_size=Decimal(10),respect_newlines_in_text= False))   
        t.add(Paragraph(tetxtstr1, font_color=HexColor("#0b0d0f"), font_size=Decimal(10), respect_newlines_in_text=True))   
        
        tetxtstr = ''
        LANGER_TEXT = ''
        tetxtstr1 = f'LKW Nummer:\t{KfzZugID}'
        
        t.add(Paragraph(tetxtstr, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))    
        t.add(Paragraph(LANGER_TEXT, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))   
        t.add(Paragraph(tetxtstr1, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))   
        
        tetxtstr = ''
        LANGER_TEXT = ''
        tetxtstr1 = ''
        
        t.add(Paragraph(tetxtstr, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))    
        t.add(Paragraph(LANGER_TEXT, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))   
        t.add(Paragraph(tetxtstr1, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))   
        
        tetxtstr = f'Ablieferdatum/-zeit '
        LANGER_TEXT = f'{DtSt} {MiSt} Uhr'
        tetxtstr1 = ''
        
        t.add(Paragraph(tetxtstr, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))    
        t.add(Paragraph(LANGER_TEXT, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))   
        t.add(Paragraph(tetxtstr1, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))   
        
        # Set padding
        t.set_padding_on_all_cells(Decimal(1), Decimal(1), Decimal(1), Decimal(5)).no_borders()
        layout.add(t)
        ##################################################################################################
        #*************************************************************************************************
        #t = FlexibleColumnWidthTable(number_of_columns=1, number_of_rows=1, )
        #t.add(TableCell(Paragraph("KunFFDlINr",font_color=HexColor("#ffffff")))).no_borders()
        #layout.add(t)
        t = FlexibleColumnWidthTable(number_of_columns=3, number_of_rows=3, )
        tetxtstr = 'Menge VPE'
        LANGER_TEXT = 'Inhalt'
        tetxtstr1 = 'Gew.in kg' 
        # Header row
        t.add(TableCell(Paragraph(tetxtstr,font_color=HexColor("#0b0d0f"), font_size=Decimal(10))))
        t.add(TableCell(Paragraph(LANGER_TEXT,font_color=HexColor("#0b0d0f"), font_size=Decimal(10))))
        t.add(TableCell(Paragraph(tetxtstr1, font_color=HexColor("#0b0d0f"), font_size=Decimal(10))))
        # Data rows
        tetxtstr = 'Menge PAL'
        LANGER_TEXT = ''
        tetxtstr1 = '' 
            
        t.add(Paragraph(tetxtstr, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))    
        t.add(Paragraph(LANGER_TEXT, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))   
        t.add(Paragraph(tetxtstr1, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))   
        
        tetxtstr = AufVPEAnz.replace('00','',1)
        LANGER_TEXT = Inhalt
        tetxtstr1 = AufTatsGewSum.replace('00','',1)
            
        t.add(Paragraph(tetxtstr, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))    
        t.add(Paragraph(LANGER_TEXT, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))   
        t.add(Paragraph(tetxtstr1, font_color=HexColor("#0b0d0f"), font_size=Decimal(10)))   
        
        # Set padding
        t.set_padding_on_all_cells(Decimal(1), Decimal(1), Decimal(1), Decimal(5)).no_borders()
        layout.add(t)
        PAT =FileNAME
        PAT1 =FileNAME.replace("SIGN.PNG","IMAGE.JPG")
        print (PAT)
        IMAGE_PATH = Path(PAT)
        my_file = Path(PAT1)
        #IMAGE_PATH = Path('A0010084285.JPG')
        if IMAGE_PATH.is_file():
            t1 = Image(image=IMAGE_PATH, width=200, height=100) #change the size as you wish

        t = FlexibleColumnWidthTable(number_of_columns=2, number_of_rows=2, )
        t.add(TableCell(Paragraph('TTTTTTTTTTTTTTTTTTTTTTTTTTT', font_color=HexColor("#ffffff"))),)
        t.add(TableCell(Paragraph('TTTTTTTTTTTTTTTTTTTTTTTTTTT', font_color=HexColor("#ffffff"))),)
        t.add(Paragraph('TTTTTTTTTTTTTTTTTTTTTTTTTTT', font_color=HexColor("#ffffff")))   
        t.add(Paragraph('Unterschrift', font_color=HexColor("#ffffff")))
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5)).no_borders()
        layout.add(t)

        t = FlexibleColumnWidthTable(number_of_columns=2, number_of_rows=2, )
        t.add(TableCell(Paragraph('TTTTTTTTTTTTTTTTTTTTTTTTTTT', font_color=HexColor("#ffffff"))),)
        t.add(TableCell(t1))
        t.add(Paragraph('TTTTTTTTTTTTTTTTTTTTTTTTTTT', font_color=HexColor("#ffffff")))   
        t.add(Paragraph('Unterschrift', font_color=HexColor("#ffffff")))
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5)).no_borders()
        layout.add(t)
        

        
        #page_layout.add(Image(image=IMAGE_PATH, width=100, height=100))
        
        
        IMAGE_PATH = Path('Footer1.png')
        t = Image(image=IMAGE_PATH, width=466, height=70)
        layout.add(t)
        
        IMAGE_PATH = Path('Footer.png')
        t = Image(image=IMAGE_PATH, width=466, height=70)
        layout.add(t)
        
    
        with open(Path(f"{NVE}.pdf"), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

if __name__ == "__main__":
    print ('Begin')
    #create_pdf('10084285')
    filenames = next(walk(mypathIN), (None, None, []))[2]  # [] if no file
    for fm in filenames:
        FNNVE = fm.split('_',1)[0]
        RAS= fm.split('.',1)[1]

        sql_select = f"select top 1 AufNr from XXASLAuf where AufArt != 'D' and AufIntNr in (select AufIntNr from XXANVE Where NVE = '{FNNVE}')" if len(FNNVE)== 20 else sql_select
        sql_select = "select top 1 AufNr from XXASLAuf as SLAuf left join  XXAAufExt TT on SLAuf.AufIntNr = TT.AufIntNr where AufArt != 'D'and TrackandTraceEmail  = '" + str(FNNVE) + "'" if len(FNNVE)== 18 else sql_select
        sql_select = f"select top 1 AufNr from XXASLAuf as SLAuf left join  XXAAufExt TT on SLAuf.AufIntNr = TT.AufIntNr where AufArt != 'D'and TrackandTraceEmail  = '" + str(FNNVE)[:-4] + "'" if len(FNNVE)== 22 else sql_select
        sql_select = f"select top 1 AufNr from XXASLAuf as SLAuf left join  XXAAufExt TT on SLAuf.AufIntNr = TT.AufIntNr where AufArt != 'D'and TrackandTraceEmail  = '" + str(FNNVE)[1:-5] + "'" if len(FNNVE)== 24 else  sql_select
        #else f"select top 1 AufNr from XXASLAuf where LiefNr  =  '{FNNVE[1:-6]}'"
        #print (sql_select)

        db1 = pymssql.connect(server, user, password, db_name)
        cursor1 = db1.cursor(as_dict=True)
        cursor1.execute(sql_select)

        try:
            #print (sql_select)
            for row1 in cursor1:
                FileNAME = mypathIN + fm
    
                AufNr = str(row1['AufNr']) if not None else ''
                #shutil.copy2(FileNAME, f"{LIST_PATCH}{fm}")
                with open(LIST_PATCH) as d:
                    if AufNr in d.read():
                        d.close()
                        print(AufNr + ' ist schon Da' )
    
                    else:
                        print (AufNr + ' ist nicht Da' )
                        file_2 = open(LIST_PATCH, 'a')
    
                        print (AufNr)
    
                        Conter = Conter + 1
                        if create_pdf (AufNr, FileNAME , Conter ) == 1:
                            file_2.write(AufNr + '\n')
                            file_2.close()
        except:
            print ('Xe-XE')

        try:
            shutil.move(mypathIN + fm,'//srv-wss/Schnittstellen/DansckDistribution/in/BCK/')
        except:
            os.remove(mypathIN + fm)
    print ('END')
   