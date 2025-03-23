"""
Script: STAT_VTL.py
Description: [ADD DESCRIPTION HERE]
Usage: python STAT_VTL.py
"""

﻿#############################################################################
#############################################################################
#                               VCTL
#############################################################################
#############################################################################
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random
from os import walk
import os
import pandas as pd
import pymssql
import random, string
import datetime
import time
import random, string
from time import gmtime , strftime

#LIST_PATCH = r'%username%'
#LIST_PATCH = r'C:/Users/%username%/Downloads/'
LIST_PATCH = r'C:/Users/aw/Downloads/'
#LIST_PATCH = r'C:/Users/administrator.DOMCC/Downloads/'
vorg = strftime("%d%m%Y",  time.localtime(time.time() - 300*3600))
print (vorg)
server="srv-db1"
user = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
db_name="WinSped"
AufNr = ''

def Dat_ord(StatusDat):
    DD = str(StatusDat[:2])
    YYYY = str(StatusDat[6:10])
    MM =  str(StatusDat[3:5])
    tt =  str(StatusDat[-8:])
    NNN = f'{YYYY}-{MM}-{DD} {tt}'
    return NNN

def get_driver():
    """Создает и настраивает веб-драйвер."""
    options = Options()
    options.add_argument("--headless")  # Запуск без UI
    driver = webdriver.Chrome(options=options)
    return driver

def login_vtl(driver):
    """Вход в систему VTL."""
    driver.get("https://my.vtl.de/portal/login.aspx")
    driver.find_element(By.NAME, "ctl00$CPHMain$tbLoginDepotID").send_keys("04245")
    driver.find_element(By.NAME, "ctl00$CPHMain$tbLoginUser").send_keys("aw")
    driver.find_element(By.NAME, "ctl00$CPHMain$tbLoginKennwort").send_keys("Gksa960036!!")
    driver.find_element(By.NAME, "ctl00$CPHMain$btnLogin").click()

def download_report(driver, report_type):
    #print (report_type)
    driver.get("https://my.vtl.de/portal/StatusCenter/StatusOverview.aspx")
    time.sleep(8)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"#ctl00_CPHMainB_M_RadioButtonListReportType_{report_type}"))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ctl00_CPHMainB_M_DateTimePickerDateFrom_rdpDate_dateInput"))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ctl00_CPHMainB_M_DateTimePickerDateFrom_rdpDate_dateInput"))).send_keys(vorg)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ctl00_CPHMainB_M_RadButtonSearch"))).click()
    time.sleep(8)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ctl00_CPHMainB_M_ReportViewer_ctl09_ctl04_ctl00_ButtonImg"))).click()
    button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/form/div[5]/div[1]/div/div/table/tbody/tr[3]/td/div[1]/div/div[3]/table/tbody/tr/td/div[2]/div[7]")))#.click()
    time.sleep(12)
    driver.execute_script("$find('ctl00_CPHMainB_M_ReportViewer').exportReport('CSV');", button)
    time.sleep(8)

def ABHMESSPUNKT(ALLAUF):
    sql_select = f"""
    select distinct  
ST.StatusNr, ST.StatusDat ,ST.StatusZeit,  AUF.LiefNr, AUF.KommNr,AUF.AufgeberNr from XXASLStatu ST
left join XXASLAuf AUF on  ST.AufNr = AUF.AufNr
where --ST.AufNr = 10134338 and 
ST.StatusNr in ('3008','6104')
and ST.StatusDat >= (SELECT DATEADD(dd, 0, DATEDIFF(dd, 0, GETDATE()))-3)
and AUF.AufgeberNr = 1003942
and  AUF.LiefNr not in ({ALLAUF})
and  AUF.KommNr not in ({ALLAUF})
    """
    #print (sql_select)
    db = pymssql.connect(server, user, password, db_name)
    cursor = db.cursor(as_dict=True)
    cursor.execute(sql_select)
    Auf_Nr = ''
    for row in cursor:
        LiefNr = str(row['LiefNr']) if not None else ''
        KommNr = str(row['KommNr']) if not None else ''
       
        AufgeberNr = str(row['AufgeberNr'])
        STATIS = str(row['StatusDat'])[:10] if row['StatusDat'] is not None else 0
        STATHH = str(row['StatusZeit'])[-8:] if row['StatusZeit'] is not None else 0
        B00 = f'{STATIS} {STATHH}' if STATIS or STATHH != 0 else 0
        DEPO1 = '04245'
        DEPO2 = '04245'
        DEPO3 = '04245'
        if LiefNr[:6]== 'N04245':        
            STATUSVTLMAIKER ( KommNr , LiefNr, B00, 'B00', DEPO1,DEPO2,DEPO3, AufgeberNr)
        else:
            STATUSVTLMAIKER ( LiefNr , KommNr, B00, 'B00', DEPO1,DEPO2,DEPO3, AufgeberNr)
        
    #return Auf_Nr, AufgeberNr if result else None

def NVESTATUSTEXT(NVE):
    match NVE:
        case 'C00':
            return '(3000,3157)'
        case 'E00':
            return '(3029)'
        case 'F00':
            return '(3042)'
        case 'H00':
            return '(3073)'
        case 'I00':
            return '(3089)'
        case 'K00':
            return '(3122)'
        case 'L00':
            return '(3136)'
        case _:
            return ''

def STATUSVTLMAIKER (AufNr, AUF, StatusDat, STATUSNR, DEPO1, DEPO2, DEPO3, AufgeberNr):
    Q20STR = ''
    RANDOMZHAL = str(random.random()).replace(".","")[:6]
    #STATpatch = "//srv-wss/Schnittstellen/TEST/OUT/"
    STATpatch = "//srv-wss/Schnittstellen/VTL/Handewitt/Fulda/Export/Status_EXPORT/LIS2VTL/"
    now = strftime("%d%m%Y%H%M", gmtime())
    #print (StatusDat)
    HH = StatusDat[-8:].replace(":", "")
    #print (HH)
    StatusDat = StatusDat[:10]
    YY = str(StatusDat[2:4])
    YYYY = str(StatusDat[:4])
    MM =  str(StatusDat[5:7])
    DD =  str(StatusDat[8:10])
    KDAT = YY+MM+DD
    LDAT= DD+MM+YYYY
    NNN = DD + MM + YYYY + HH
    #print (NNN , " ", LDAT, " ", KDAT )
    STATUSTEXT = NVESTATUSTEXT(STATUSNR)
    if STATUSTEXT !=  '' :
        Q20STR = SQLAbfrageNVE (AufNr,AUF,STATUSTEXT, STATUSNR)
    AufNr=f'{AufNr:{' '}{'<'}{35}}'
    AUF = f'{AUF:{' '}{'<'}{70}}'
    #Q20STR = ''
    if AufgeberNr == '1003942':
        ABH = '   '
        ABHN = 'ue'
    else:
        ABH = '   '
        ABHN = 'ue'
        
    if Q20STR is not None:
        STRANZ = str(2 + Q20STR.count('\nQ20'))
    else:
        STRANZ= '2'
    #print (STRANZ)
    var = f'''
@@PHSTAT512 0512003500107   04001   04245
Q00100VTL{DEPO1}{ABH}                           {DEPO2}                              {DEPO3}
Q10{AufNr}{AUF}{STATUSNR}{LDAT}0647                                   0000                                                                                                         {KDAT}{NNN}{Q20STR}
Z0000000{STRANZ}{NNN}
@@PT
'''
    #print (var)
    with open(f'{STATpatch}04245_{ABHN}_{NNN + RANDOMZHAL}.txt', 'a') as out:
        print (f'{STATpatch}04245_{ABHN}_{NNN + RANDOMZHAL}.txt')
        out.write(var)
    time.sleep(1)
    if len(AUF)>8 :
        AUF = AUF.replace('N04245.', '')
    SYSTEM_VERKEHR_STATUS(AUF)
    StatusDat = ''
    Q20STR = ''

def SQLAbfrage(FBNR):
    sql_select = f"select top 1 AufNr, AufgeberNr from XXASLAuf  where  LiefNr = '{FBNR}' or KommNr = '{FBNR}'"
    #print (sql_select)
    db = pymssql.connect(server, user, password, db_name)
    cursor = db.cursor(as_dict=True)
    cursor.execute(sql_select)
    Auf_Nr = ''
    for row in cursor:
        Auf_Nr = str(row['AufNr'])
        AufgeberNr = str(row['AufgeberNr'])
        print (Auf_Nr, AufgeberNr)
    return Auf_Nr, AufgeberNr if result else None

def SQLAbfragee(AUF,STATIS_VTL, AufgeberNr):
    sql_select = f"""select top 1 AUF.AufgeberNr, ST.StatusDat ,ST.StatusZeit,  AUF.LiefNr, AUF.KommNr, DispoInf10 from XXASLStatu ST
left join XXASLAuf AUF on  ST.AufNr = AUF.AufNr
where ST.AufNr = {AUF} and ST.StatusNr in ({STATIS_VTL})
"""
    #print (sql_select)
    db = pymssql.connect(server, user, password, db_name)
    cursor = db.cursor(as_dict=True)
    cursor.execute(sql_select)
    STATHH = ''
    STATIS = ''
    AufNr = 0
    for row in cursor:
        if row['AufgeberNr'] == '1003942' and STATIS_VTL == '3008':
            AufNr = str(row['KommNr']) if row['KommNr'] is not None else f'N04245.{AUF}'
            LiefNr= str(row['LiefNr']) if row['LiefNr'] is not None else f'N04245.{AUF}'
            if AufNr[:6] != 'N04245':
                AufNr = AufNr
            else:
                AufNr = LiefNr if LiefNr != 0 else f'N04245.{AUF}'
        else:
            AufNr = str(row['LiefNr']) if row['LiefNr'] is not None else 0
            
        STATIS = str(row['StatusDat'])[:10] if row['StatusDat'] is not None else 0
        STATHH = str(row['StatusZeit'])[-8:] if row['StatusZeit'] is not None else 0
        STATIS = f'{STATIS} {STATHH}' if STATIS or STATHH != 0 else 0
        print (STATIS, AufNr, AUF, STATIS_VTL, AufgeberNr)
    return STATIS, AufNr

def SQLAbfrageNVE(AufNr, AUF, STATUSTEXT, STATUSNR):
    sql_select = f"select StatusDat , StatusZeit ,NVE from XXANVEStat NS left join XXASLAuf SL on sl.AufIntNr = ns.AufIntNr and NS.StatusNr in {STATUSTEXT} where Sl.aufnr = '{AUF}'"
    #print (sql_select)
    db = pymssql.connect(server, user, password, db_name)
    cursor = db.cursor(as_dict=True)
    cursor.execute(sql_select)
    Q20STR = ''
    STTR = STATUSNR[:1]
    for row in cursor:
        NVE = str(row['NVE'])
        AufNr=f'{AufNr:{' '}{'<'}{35}}'
        NVE = f'{NVE:{' '}{'<'}{35}}'
        STDAT = str(row['StatusDat']) if row['StatusDat'] is not None else 0
        STTEM = str(row['StatusZeit']) if row['StatusZeit'] is not None else 0
        if NVE is not None:
            AufNr=f'{AufNr:{' '}{'<'}{35}}'
            NVE = f'{NVE:{' '}{'<'}{35}}'
            StatusDat = str(STDAT[:10])
            YYYY = StatusDat[:4]
            MM =  StatusDat[5:7]
            DD =  StatusDat[8:10]
            LDAT= DD+MM+YYYY
            HH = STTEM[-8:].replace(":", "")
            NNN = DD + MM + YYYY + HH
            Q20STR =  Q20STR + f'\nQ20{AufNr}{STTR}  {NVE}{NNN}{STTR}00'
            NVE = None
        else:
            print ('None')
    return Q20STR

def Now_test(ALLAUF):

    state_file = "//srv-wss/Schnittstellen/_Scripte/py/VTL/last_dfu_date.txt"

    now = datetime.datetime.now()

    if now.hour > 14 or (now.hour == 14 and now.minute >= 45):
        last_run_date = None
        if os.path.exists(state_file):
            with open(state_file, "r") as f:
                last_run_date_str = f.read().strip()
                try:
                    last_run_date = datetime.datetime.strptime(last_run_date_str, "%Y-%m-%d").date()
                except ValueError:
                    pass  
        if last_run_date != now.date():
            ABHMESSPUNKT(ALLAUF)
            with open(state_file, "w") as f:
                f.write(now.strftime("%Y-%m-%d"))
        else:
            print(f"{now}: Ok ")
    else:
        print(f"{now}: No ")

def update_infosymbol(AUF: int, connection: pymssql.Connection) -> int:

    sql_update = """
    UPDATE XXASLAufInfSym
    SET infosymbol56 = 560
    WHERE infosymbol56 <> 562
      AND AufIntNr IN (
          SELECT AufIntNr FROM xxaslauf WHERE AufNr = %s
      )
    """
    cursor = connection.cursor()
    cursor.execute(sql_update, (AUF,))
    connection.commit()
    updated_rows = cursor.rowcount
    cursor.close()
    return updated_rows

def SYSTEM_VERKEHR_STATUS(AUF):
   
    try:
        conn = pymssql.connect(server=server, user=user, password=password, database=db_name)
        #conn = get_connection(server, user, password, db_name)
        rows_updated = update_infosymbol(AUF, conn)
        print(f'Aktualisierte Zeilen: {rows_updated}')  # Немецкий вывод
    except pymssql.Error as e:
        print("Fehler bei der Datenbankverbindung:", e)
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":


    driver = get_driver()
    try:
        login_vtl(driver)
        for report_type in range(3):
            download_report(driver, report_type)
    finally:
        driver.quit()

    filenames = next(walk(LIST_PATCH), (None, None, []))[2]  # [] if no file
    ALLAUF = ''
    for fm in filenames:
        #print (fm)
        if fm[:25] == 'ConsignmentStatusOverview':
            #try:
            df = pd.read_csv(LIST_PATCH + fm)
            df = df.fillna(0)
            print (fm)
            for _, row in df.iterrows():
                AufgeberNr = ''
                AUF = ''
                B00 = 0
                C00 = 0
                E00 = 0
                F00 = 0
                H00 = 0
                I00 = 0
                K00 = 0
                L00 = 0
                POD = 0
                L00_Flag = 0
                K00_Flag = 0
                I00_Flag = 0
                H00_Flag = 0
                F00_Flag = 0
                E00_Flag = 0
                C00_Flag = 0
                B00_Flag = 0
                DEPO1 = ''
                DEPO2 = ''
                DEPO3 = ''
                INTERN_FLAF = 0

                if len(row) >6:
                    print (row[20])
                    
                    if row[20] != 0 and row[20] != '' :
                        if ALLAUF != '':
                            ALLAUF = f"'{ALLAUF}','{row[20]}'".replace("''","'")
                        else:
                            ALLAUF = f"'{row[20]}'".replace("''","'")
                        
                    if row[20][:6]== 'N04245' and len(row[20])== 15:
                        AUF = row[20].replace('N04245.', '')
                        INTERN_FLAF = 1
                        print ('Intern')
                    else:
                        print ('Extern')
                        INTERN_FLAF = 0
                        try:
                            AUF, AufgeberNr = SQLAbfrage(row[20])
                        except:
                            AUF = None
                    if AUF is not None:
                        print (AUF)
                        DEPO1, DEPO2, DEPO3 = [f'0{str(row[22])}' if row[22] !=0 else '     ', f'0{str(row[23])}' if row[23] !=0 else '     ', f'0{str(row[24])}' if row[24] !=0 else '     ' ]
                        DEPO1 = DEPO1 if len(DEPO1) == 5 else  f'{DEPO1:{' '}{'<'}{5}}'
                        DEPO2 = DEPO2 if len(DEPO2) == 5 else  f'{DEPO2:{' '}{'<'}{5}}'
                        DEPO3 = DEPO3 if len(DEPO3) == 5 else  f'{DEPO3:{' '}{'<'}{5}}'
                        DEPO1 = '04245' if INTERN_FLAF == 1 and DEPO1 != '04245' and DEPO3 != '04245' else DEPO1
                        DEPO3 = '04245' if INTERN_FLAF == 0 and DEPO1 != '04245' and DEPO3 != '04245' else DEPO3
                        print (DEPO1, DEPO2, DEPO3)
                        B00 = Dat_ord(row[30]) if row[30] != 0 else 0
                        C00 = Dat_ord(row[31]) if row[31] != 0 else 0
                        E00 = Dat_ord(row[32]) if row[32] != 0 else 0
                        F00 = Dat_ord(row[33]) if row[33] != 0 else 0
                        H00 = Dat_ord(row[34]) if row[34] != 0 else 0
                        I00 = Dat_ord(row[35]) if row[35] != 0 else 0
                        K00 = Dat_ord(row[36]) if row[36] != 0 else 0
                        L00 = Dat_ord(row[37]) if row[37] != 0 else 0
                        POD = Dat_ord(row[38]) if row[38] != 0 else 0
                        print (B00, C00, E00, F00, H00, I00, K00, L00)
                        #if len (AUF) > 0 and L00 == 0:
                        if len (AUF) > 0 :
    ################################################################################################################################################

                            if L00 == 0 and DEPO3 == '04245':
                                L00, NOC = SQLAbfragee(AUF, '3199' , AufgeberNr)
                                L00 = L00 if L00 is not None else 0
                                L00 = L00 if L00 != '' else 0
                                L00 = L00 if L00 != 0 else 0
                                if L00 != 0:
                                    print (L00, 'L00')
                                    STATUSVTLMAIKER ( row[20] , AUF, L00, 'L00', DEPO1,DEPO2,DEPO3, AufgeberNr)
                                    L00_Flag = 1
                                else:
                                    L00_Flag = 0

                            if K00 == 0 and DEPO3 == '04245':
                                K00, NOC = SQLAbfragee(AUF, '3188', AufgeberNr)
                                K00 = K00 if K00 is not None else L00
                                K00 = K00 if K00 != '' else L00
                                K00 = K00 if K00 != 0 else L00
                                if K00 != 0:
                                    print (K00, 'K00')
                                    STATUSVTLMAIKER ( row[20] , AUF, K00, 'K00', DEPO1,DEPO2,DEPO3, AufgeberNr)
                                    K00_Flag = 1
                                else:
                                    if L00_Flag ==1:
                                        K00 = L00
                                        STATUSVTLMAIKER ( row[20] , AUF, K00, 'K00', DEPO1,DEPO2,DEPO3, AufgeberNr)
                                        K00_Flag = 1
                                    else:
                                        K00_Flag = 0

                            if I00 == 0 and DEPO3 == '04245':
                                I00, NOC = SQLAbfragee(AUF, '3124', AufgeberNr)
                                I00 = I00 if I00 is not None else K00
                                I00 = I00 if I00 != '' else K00
                                I00 = I00 if I00 != 0 else K00
                                if I00 != 0:
                                    print (I00, 'I00')
                                    STATUSVTLMAIKER ( row[20] , AUF, I00, 'I00', DEPO1,DEPO2,DEPO3, AufgeberNr)
                                    I00_Flag = 1
                                else:
                                    if K00_Flag ==1:
                                        I00 = K00
                                        STATUSVTLMAIKER ( row[20] , AUF, I00, 'I00', DEPO1,DEPO2,DEPO3, AufgeberNr)
                                        I00_Flag = 1
                                    else:
                                        I00_Flag = 0


                            if H00 == 0 and DEPO1 == '04245':
                                H00, NOC = SQLAbfragee(AUF, '3114', AufgeberNr)
                                H00 = H00 if H00 is not None else I00
                                H00 = H00 if H00 != '' else I00
                                H00 = H00 if H00 != 0 else I00
                                if H00 != 0:
                                    print (H00, 'H00')
                                    STATUSVTLMAIKER (row[20] , AUF, H00, 'H00', DEPO1,DEPO2,DEPO3, AufgeberNr)
                                    H00_Flag = 1
                                else:
                                    if I00_Flag ==1:
                                        H00 = I00
                                        STATUSVTLMAIKER ( row[20] , AUF, H00, 'H00', DEPO1,DEPO2,DEPO3, AufgeberNr)
                                        H00_Flag = 1
                                    else:
                                        H00_Flag = 0

                            if F00 == 0 and DEPO1 == '04245':
                                F00, NOC = SQLAbfragee(AUF, '3075', AufgeberNr)
                                F00 = F00 if F00 is not None else H00
                                F00 = F00 if F00 != '' else H00
                                F00 = F00 if F00 != 0 else H00
                                if F00 != 0:
                                    print (F00, 'F00')
                                    STATUSVTLMAIKER (row[20] , AUF, F00, 'F00', DEPO1,DEPO2,DEPO3, AufgeberNr)
                                    F00_Flag = 1
                                else:
                                    if H00_Flag ==1:
                                        F00 = H00
                                        STATUSVTLMAIKER (row[20] , AUF, F00, 'F00', DEPO1,DEPO2,DEPO3, AufgeberNr)
                                        F00_Flag = 1
                                    else:
                                        F00_Flag = 0

                            if E00 == 0 and DEPO1 == '04245':
                                E00, NOC = SQLAbfragee(AUF, '3068', AufgeberNr)
                                E00 = E00 if E00 is not None else F00
                                E00 = E00 if E00 != '' else F00
                                E00 = E00 if E00 != 0 else F00
                                if E00 != 0:
                                    print (E00, 'E00')
                                    STATUSVTLMAIKER (row[20] , AUF, E00, 'E00', DEPO1,DEPO2,DEPO3, AufgeberNr)
                                    E00_Flag = 1
                                else:
                                    if F00_Flag ==1:
                                        E00 = F00
                                        STATUSVTLMAIKER (row[20] , AUF, E00, 'E00', DEPO1,DEPO2,DEPO3, AufgeberNr)
                                        E00_Flag = 1
                                    else:
                                        E00_Flag = 0

                            if C00 == 0 and DEPO1 == '04245':
                                C00, NOC = SQLAbfragee(AUF, '3030', AufgeberNr)
                                C00 = C00 if C00 is not None else E00
                                C00 = C00 if C00 != '' else E00
                                C00 = C00 if C00 != 0 else E00
                                if C00 != 0:
                                    print (C00, 'C00')
                                    STATUSVTLMAIKER (row[20] , AUF, C00, 'C00', DEPO1,DEPO2,DEPO3, AufgeberNr)
                                    C00_Flag = 1
                                else:
                                    if E00_Flag ==1:
                                        C00 = E00
                                        STATUSVTLMAIKER (row[20] , AUF, C00, 'C00', DEPO1,DEPO2,DEPO3, AufgeberNr)
                                        C00_Flag = 1
                                    else:
                                        C00_Flag = 0

                            if B00 == 0 and DEPO1 == '04245':
                                #B00, NOC = SQLAbfragee(AUF, "'3008','6104'")
                                B00, NOC = SQLAbfragee(AUF, '3008', AufgeberNr)
                                
                                NOC = NOC if NOC != 0 else row[20]
                                B00 = B00 if B00 is not None else C00
                                B00 = B00 if B00 != '' else C00
                                B00 = B00 if B00 != 0 else C00
                                NOC = row[20] if NOC.find('.') == 0 else NOC
                                NOC = row[20] if NOC.find('@') != 0 else NOC
                                if B00 != 0:
                                    print (B00, 'B00')
                                    #STATUSVTLMAIKER ( NOC , AUF, B00, 'B00', DEPO1,DEPO2,DEPO3, AufgeberNr)
                                    STATUSVTLMAIKER ( row[20] , AUF, B00, 'B00', DEPO1,DEPO2,DEPO3, AufgeberNr)
                                    B00_Flag = 1
                                else:
                                    if C00_Flag ==1:
                                        B00 = C00
                                        #STATUSVTLMAIKER ( NOC , AUF, B00, 'B00', DEPO1,DEPO2,DEPO3, AufgeberNr)
                                        STATUSVTLMAIKER ( row[20] , AUF, B00, 'B00', DEPO1,DEPO2,DEPO3, AufgeberNr)
                                        B00_Flag = 1
                                    else:
                                        B00_Flag = 0

            os.remove(LIST_PATCH + fm)

print (strftime("%d-%m-%Y %H:%M",  time.localtime(time.time())))
#ABHMESSPUNKT(ALLAUF)
Now_test(ALLAUF)
