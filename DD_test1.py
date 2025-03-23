"""
Script: DD_test1.py
Description: [ADD DESCRIPTION HERE]
Usage: python DD_test1.py
"""

import os
from os import walk
from pathlib import Path
import pymssql
from datetime import datetime

now = datetime.now()
DtSt = str(now.strftime("%d %m %Y %H %M")).replace(' ','')
print (DtSt)

#print(f'mypathOUT{fName}.XML')
server="srv-db1"
user = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
db_name="WinSped"
    
LIST_PATCH = '//srv-wss/Schnittstellen/DansckDistribution/all_Files.txt'
mypathIN = r"//SRV-WSS/Schnittstellen/DansckDistribution/in/LIS_IN/"
mypathOUT = r"//srv-wss/Schnittstellen/DansckDistribution/out/XML/"

def FBNR_DEF():
    COUNT_FILE = os.path.join('//srv-wss/Schnittstellen/DansckDistribution/FBNR.COUNTER')
    if not os.path.exists(COUNT_FILE):
        num = 0
    else:
        f = open(COUNT_FILE, 'r')
        num = int(f.read())
        f.close()
    FBB =  str(num)
    num += 1
    f = open(COUNT_FILE, 'w')
    f.write(str(num))
    f.close()
    return FBB



def XMLMAIKER (fName,StrLine):
    with open(f'{mypathOUT}{fName}.XML', 'a') as out:
        out.write(StrLine +'\n')

def BEZEICHN(AUF):
    db3 = pymssql.connect(server, user, password, db_name)
    cursor3 = db3.cursor(as_dict=True)
    cursor3.execute(f"""select  max(AufPosNr) as BEZEICHN  from XXANVE where AufIntNr in (select AufIntNr from XXASLAuf where aufnr in ({AUF}))""")
    for row3 in cursor3:
        BEZEI = row3['BEZEICHN'] if row3['BEZEICHN'] is not None else 0
        return BEZEI

def AVIS_STATUS(status):
    match status:
        case 1:
            return 'RF60'
        case 101:
            return 'Z57'
        case 51:
            return 'X31'
        case 0:
            return ''
        case 15:
            return 'XF12'
        case 620:
            return 'ZF09'
        case 621:
            return 'XF09'
        case 622:
            return 'ZF10'
        case 623:
            return 'XF10'
        case 625:
            return 'ZF12'
        case 626:
            return 'XF12'
        case 627:
            return 'ZF16'
        case 628:
            return 'XF16'
        case 629:
            return 'X07'
        case 630:
            return 'X08'
        case 631:
            return 'X09'
        case 632:
            return 'X10'
        case 633:
            return 'X11'
        case 634:
            return 'X12'
        case 635:
            return 'X13'
        case 636:
            return 'X14'
        case 637:
            return 'X15'
        case 638:
            return 'X16'
        case 639:
            return 'PRI'
        case 640:
            return 'RF30'
        case 641:
            return 'RF60'
        case 642:
            return 'ZNAT'
        case _:
            return ''

def XMLmacher(AUF):
    print(AUF)


    StartLine = """<?xml version="1.0" encoding="Windows-1252" ?>
    <Bookings xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">"""
    #sql_select3 = f"""select * from XXAV__DFUTexte where KanKey in (select AufIntNr from XXASLAuf where aufnr in ({AUF}))"""
    sql_select1 = f"""select top 100 * from XXAV__DFUTexte where kankey in (select AufIntNr from XXASLAuf where aufnr in ({AUF}))"""
    sql_select2 = f"""select NVE from XXANVE where AufIntNr in (select AufIntNr from XXASLAuf where aufnr in ({AUF}))"""
    sql_select = f"""
use winsped 
select 
 SLAuf.UrAbsNr as '1000',
 SLAuf.EmpNr as '2000',
 SLAuf.FFNr as '3000',
--**********FBHeader*****************************************************************************
 SLAuf.aufnr as 'FBNR' 
,'64' as 'BookingCreator'  
--,Aufkun.Kundennr as 'KnNr' 
,'1000001' as 'TrgKnNr'
,str(SLAuf.aufnr) + left('00000000',8 - len(Aufkun.Kundennr)) + Ltrim(str(Aufkun.Kundennr)) + '64'  as 'TrackTraceNr' 
,'64' as 'TerminalNr' 
,SLAuf.refnr as 'Reference' 
,'' as 'Reference2' 
,'' as 'Reference3'
,CAsE when  SLAuf.erfDR = '-10' then 'D'  when SLAuf.BelNr = '1000001' Then 'PD' when  SLAuf.EndEmpNr = '1000001' then 'P' END as 'BookingType' 
--,SLAuf.EndEmpNr
,'' as 'ProduktionTest'
--,SLAuf.erfDR
--,CAsE when Abskun.Name3 is not null or Aufkun.DispoInf10 is not null or Empkun.Name3 is not null Then 'JA' Else 'NEJ' END AS 'Omex'
,CAsE when SLAuf.erfDR = '400' Then 'JA' Else 'NEJ' END AS 'Omex'
,deponr.KundenNr
,SLAuf.BelNr
,SLAuf.DispoInf10
,CAsE when SLAuf.DispoInf10 = '10002' Then Emp_Sped.LStName3   Else Emp_Sped.LStName3 END AS 'OmexTnrAfh'
,'Ta' as 'OmexTnrVia'
,CAsE when SLAuf.DispoInf10 = '10002'  Then Emp_Sped.LStName3   Else Emp_Sped.LStName3 END AS 'OmexTnrLev'
 --**********SenderAddress************************************************************************
,SLAuf.AbsNr as 'SenderKnNr'
,Abskun.NAME1 as 'SenderName'
,Abskun.strasse as 'SenderAddressLine1'
,'' as 'SenderAddressLine2'
,'' as 'SenderAddressLine3'
,Abskun.ort as 'SenderCity'
,Abskun.PLZ as 'SenderZip'
,Abskun.LKZ as 'SenderCountry'
,Abskun.tel as 'SenderPhoneNo'
,Abskun.email as 'SenderMail'
 --**********RecipientAddress********************************************************************
,SLAuf.EmpNr as 'RecipientKnNr'
,Empkun.NAME1 as 'RecipientName'
,Empkun.strasse as 'RecipientAddressLine1'
,'' as 'RecipientAddressLine2'
,'' as 'RecipientAddressLine3'
,Empkun.ort as 'RecipientCity'
,Empkun.PLZ as 'RecipientZip'
,Empkun.LKZ as 'RecipientCountry'
,Empkun.tel as 'RecipientMail'
,Empkun.email as 'RecipientPhoneNo'
 --**********General-element*********************************************************************
,SLAuf.AufInfo as 'Notes'
,SLAuf.EntVonDat as 'DeliveryDate'
,SLAuf.EntVonZeit as 'DeliveryTime'
,SLAuf.TatsGew  as 'TotalWeight'
,SLAuf.KMMaut /10 as 'TotalVolume'
,SLAuf.ColliAnzSu as 'TotalColli'
,SLAuf.LMAnz * 100 as 'TotalLDM'
,CAsE when SLAuf.Frankatur = '3'  Then 'FRANKO'  Else 'UFRANKO' END AS 'Franco' -- "FRANKO"/"UFRANKO"
 --**********Specialities-element****************************************************************
,NachFrei as 'CODAmount'
,BelVonDat as 'CollectionDate'
,BelVonZeit as 'CollectionTime'
,CAsE when DispoInfo5 is not null Then 'JA' Else 'NEJ' END AS 'DangerousGoods'
,CAsE when Empkun.NAME1 like '%Post Danmark%'  or Abskun.NAME1 like '%Post Danmark%' Then 'JA' Else 'NEJ' END AS 'CarPackage'
,CAsE when SLAPos.Vpe like 'FP' or  SLAPos.Vpe like 'HP' or  SLAPos.Vpe like 'VP' Then 'JA' Else 'NEJ' END AS 'ExchangePallets'
,CAsE when SLAPos.Vpe like 'FP' Then SLAPos.VpeAnz Else null END AS 'ExchangePallets1_1'
,CAsE when SLAPos.Vpe like 'HP' Then SLAPos.VpeAnz Else null END AS 'ExchangePallets1_2'
,CAsE when SLAPos.Vpe like 'VP' Then SLAPos.VpeAnz Else null END AS 'ExchangePallets1_4'
 --**********DescriptionOfGoods -element*********************************************************
 ,NVE.AufPosNr as 'LineNr'
 ,NVE.NVE as 'BarCode'
 --,CAsE when SLAPos.Vpe like 'FP'or SLAPos.Vpe like 'VP' or SLAPos.Vpe like 'HP' Then '1/1' Else SLAPos.kammer END AS  'ColliType'
 --,CAsE when SLAPos.kammer is not null then  SLAPos.kammer else SLAPos.Vpe like 'FP'or SLAPos.Vpe like 'VP' or SLAPos.Vpe like 'HP' Then '1/1' Else SLAPos.Vpe END AS  'ColliType'
 ,SLAPos.kammer AS  'ColliType'
 ,SumPos.Inhalt as 'GoodsDescription'
 ,SumPos.TatsGew as 'Weight'
 ,SLAuf.QMAnz as 'Volume'
 ,SLAuf.LMAnz * 100 as 'LDM'
 ,DlSvCtrl as 'ADR_UN'
 ,SLAPos.AufIntNr as 'ParcelReference'
 ,SumPos.Breite / 10 as 'Width'
 ,SumPos.Laenge / 10 as 'Length'
 ,SumPos.Hoehe / 10  as 'Height'
 ,'1' as 'colli'
 ,'' as 'VID' 
 ,EmpSped
 ,GG.ADRKlasse as 'Klasse'
 ,GG.ADRZiffer as 'EmbGruppe'
 ,GG.UNNummerA as 'UNnr'
 ,GG.Stoffname as 'Beskrivelse' 
 ,GG.GgutWert as 'Point'
 ,NVELfdNr
--,SLAPos.AufPosNr as BEZEICHN
 --,*--from XXANVE as NVE
 from XXASLAuf as SLAuf
left join xxakun Empkun on Empkun.Kundennr = SLAuf.EmpNr
left join XXANVE NVE on NVE.AufIntNr = SLAuf.AufIntNr
LEFT JOIN XXASLAPos SLAPos ON SLAuf.AufIntNr = SLAPos.AufIntNr and NVE.AufPosNr = SLAPos.AufPosNr
left join xxakun Aufkun on Aufkun.Kundennr = SLAuf.Aufgebernr
left join xxakun Abskun on Abskun.Kundennr = SLAuf.UrAbsNr
left join xxakun deponr on deponr.Kundennr = SLAuf.FFNr
left join xxakun Emp_Sped on Emp_Sped.Kundennr = SLAuf.EmpSped
left join xxaSLAPos SumPos on SLAuf.AufIntNr = SumPos.AufIntNr and  NVE.AufPosNr = SumPos.AufPosNr
left join XXAAufGgut GG on SLAuf.AufIntNr = GG.AufIntNr

where SLAuf.AufArt != 'D' and nve.AufIntNr in (select AufIntNr from XXASLAuf where aufnr in ({AUF})) 
"""
    db = pymssql.connect(server, user, password, db_name)
    cursor = db.cursor(as_dict=True)
    Bschaffen = ''
    
    cursor.execute(sql_select)
    with open(LIST_PATCH) as d:
        if str(AUF) in d.read(): 
            d.close()
            print(AUF + ' ist schon Da' )
            #WRITELOG(AUF + ' ist schon Da' )
        else:
            #WRITELOG (AUF + ' ist nicht Da' )
            print (AUF + ' ist nicht Da' )
            file_2 = open(LIST_PATCH, 'a')
            file_2.write(AUF + '\n')

            FBNR_ALT = ''
            TEW_DAT = 0
            for row in cursor:
        
                #FBNR = str(row['FBNR']) if row['FBNR'] is not None else ''
                FBNR1 = str(FBNR_DEF())
                FBNR = '64500000'[:-len(FBNR1)] + FBNR1
                print (FBNR)
                #DtSt = f'{str(DtSt)} - {Str( AUF)}'
                BookingCreator = str(row['BookingCreator']) if row['BookingCreator'] is not None else ''
                #KnNr = str(row['KnNr']) if row['KnNr'] is not None else ''
                TrgKnNr = str(row['TrgKnNr']) if row['TrgKnNr'] is not None else ''
                #TrackTraceNr = str(row['TrackTraceNr']).replace(' ', '') if row['TrackTraceNr'] is not None else ''
                TrackTraceNr = '0000968664'
                TrackTraceNr = FBNR + TrackTraceNr
                TerminalNr = str(row['TerminalNr']) if row['TerminalNr'] is not None else ''
                Reference = str(row['Reference']) if row['Reference'] is not None else ''
                Reference3 = AUF
                Reference2 = str(row['Reference2']) if row['Reference2'] is not None else ''
                #Reference3 = str(row['Reference3']) if row['Reference3'] is not None else ''
                #Reference = FBNR
                BookingType = str(row['BookingType']) if row['BookingType'] is not None else ''
                ProduktionTest = str(row['ProduktionTest']) if row['ProduktionTest'] is not None else ''
                DispoInf10 = row['DispoInf10'] if row['DispoInf10'] is not None else 0
                Omex = str(row['Omex']) if row['Omex'] is not None else ''
                OmexTnrAfh = str(row['OmexTnrAfh']) if row['OmexTnrAfh'] is not None else ''
                OmexTnrVia = str(row['OmexTnrVia']) if row['OmexTnrVia'] is not None else ''
                OmexTnrLev = str(row['OmexTnrLev']) if row['OmexTnrLev'] is not None else ''
                SenderKnNr = str(row['SenderKnNr']) if row['SenderKnNr'] is not None else ''
                SenderName = str(row['SenderName']) if row['SenderName'] is not None else ''
                SenderAddressLine1 = str(row['SenderAddressLine1']) if row['SenderAddressLine1'] is not None else ''
                SenderAddressLine2 = str(row['SenderAddressLine2']) if row['SenderAddressLine2'] is not None else ''
                SenderAddressLine3 = str(row['SenderAddressLine3']) if row['SenderAddressLine3'] is not None else ''
                SenderCity = str(row['SenderCity']) if row['SenderCity'] is not None else ''
                SenderZip = str(row['SenderZip']) if row['SenderZip'] is not None else ''
                SenderCountry = str(row['SenderCountry']) if row['SenderCountry'] is not None else ''
                SenderPhoneNo = str(row['SenderPhoneNo']) if row['SenderPhoneNo'] is not None else ''
                SenderMail = str(row['SenderMail']) if row['SenderMail'] is not None else ''
                RecipientKnNr = str(row['RecipientKnNr']) if row['RecipientKnNr'] is not None else ''
                RecipientName = str(row['RecipientName']) if row['RecipientName'] is not None else ''
                RecipientAddressLine1 = str(row['RecipientAddressLine1']) if row['RecipientAddressLine1'] is not None else ''
                RecipientAddressLine2 = str(row['RecipientAddressLine2']) if row['RecipientAddressLine2'] is not None else ''
                RecipientAddressLine3 = str(row['RecipientAddressLine3']) if row['RecipientAddressLine3'] is not None else ''
                RecipientCity = str(row['RecipientCity']) if row['RecipientCity'] is not None else ''
                RecipientZip = str(row['RecipientZip']) if row['RecipientZip'] is not None else ''
                RecipientCountry = str(row['RecipientCountry']) if row['RecipientCountry'] is not None else ''
                RecipientMail = str(row['RecipientMail']) if row['RecipientMail'] is not None else ''
                RecipientPhoneNo = str(row['RecipientPhoneNo']) if row['RecipientPhoneNo'] is not None else ''
                Notes = str(row['Notes']) if row['Notes'] is not None else ''
                DeliveryDate = row['DeliveryDate'] if row['DeliveryDate'] is not None else ''
                DeliveryDate = str(DeliveryDate.strftime("%Y%m%d"))
                DeliveryTime = row['DeliveryTime'] if row['DeliveryTime'] is not None else ''
                DeliveryTime = str(DeliveryTime.strftime("%H:%M"))
                TotalWeight = str(row['TotalWeight']).replace('.0000', '')  if row['TotalWeight'] is not None else ''
                TotalVolume = str(row['TotalVolume']).replace('.0000', '')  if row['TotalVolume'] is not None else ''
                TotalColli = str(row['TotalColli']).replace('.0000', '')  if row['TotalColli'] is not None else ''
                TotalLDM = str(row['TotalLDM'] * 100).replace('.0000', '')  if row['TotalLDM'] is not None else ''
                Franco = str(row['Franco']) if row['Franco'] is not None else ''
                CODAmount = str(row['CODAmount']) if row['CODAmount'] is not None else ''
                CollectionDate = row['CollectionDate'] if row['CollectionDate'] is not None else ''
                CollectionDate = str(CollectionDate.strftime("%Y%m%d"))
                CollectionTime = row['CollectionTime'] if row['CollectionTime'] is not None else ''
                CollectionTime = str(CollectionTime.strftime("%H:%M")) 
        
                DangerousGoods = str(row['DangerousGoods']) if row['DangerousGoods'] is not None else ''
                CarPackage = str(row['CarPackage']) if row['CarPackage'] is not None else ''
                CarPackage = str(row['CarPackage']) if row['CarPackage'] is not None else ''
                ExchangePallets = str(row['ExchangePallets']) if row['ExchangePallets'] is not None else ''
                ExchangePallets1_1 = str(row['ExchangePallets1_1']) if row['ExchangePallets1_1'] is not None else ''
                ExchangePallets1_2 = str(row['ExchangePallets1_2']) if row['ExchangePallets1_2'] is not None else ''
                ExchangePallets1_4 = str(row['ExchangePallets1_4']) if row['ExchangePallets1_4'] is not None else ''
                LineNr = str(row['LineNr']) if row['LineNr'] is not None else ''
                BarCode = str(row['BarCode']) if row['BarCode'] is not None else ''
                ColliType = str(row['ColliType']) if row['ColliType'] is not None else ''
                GoodsDescription = str(row['GoodsDescription']) if row['GoodsDescription'] is not None else ''
                Weight = str(row['Weight']).replace('.0000', '') if row['Weight'] is not None else ''
                Volume = str(row['Volume']).replace('.0000', '')  if row['Volume'] is not None else ''
                LDM = str(row['LDM'] * 100) .replace('.0000', '') if row['LDM'] is not None else ''
                ADR_UN = str(row['ADR_UN']) if row['ADR_UN'] is not None else ''
                ParcelReference = str(row['ParcelReference']) if row['ParcelReference'] is not None else ''
                Width = str(row['Width']).replace('.0000', '')  if row['Width'] is not None else ''
                Length = str(row['Length']).replace('.0000', '')  if row['Length'] is not None else ''
                Height = str(row['Height']).replace('.0000', '')  if row['Height'] is not None else ''
                colli = str(row['colli']) if row['colli'] is not None else ''
                Klasse = str(row['Klasse']) if row['Klasse'] is not None else ''
                EmbGruppe = str(row['EmbGruppe']) if row['EmbGruppe'] is not None else ''
                UNnr = str(row['UNnr']) if row['UNnr'] is not None else ''
                Beskrivelse = str(row['Beskrivelse']) if row['Beskrivelse'] is not None else ''
                Point = str(row['Point']) if row['Point'] is not None else ''
                NVELfdNr = row['NVELfdNr'] if row['NVELfdNr'] is not None else 0
                
                
                #BEZEICHN = row['BEZEICHN'] if row['BEZEICHN'] is not None else 0
                BEZEICHN1 = BEZEICHN(AUF)
                if ProduktionTest == 'T':
                    Reference = 'Test-'+ Reference
                    Reference2 = 'Test-'+ Reference2
                    Reference3 = 'Test-'+ Reference3
                if DispoInf10 == 10001:
                    Bschaffen = '_OL'
                    OmexTnrAfh = '64'
                    OmexTnrLev = ''
                else: 
                
                    Bschaffen = '_OA'
                    OmexTnrLev = '64'
                    OmexTnrAfh = ''
                if TEW_DAT==0:
                    XMLMAIKER (DtSt + AUF + Bschaffen ,'<?xml version="1.0" encoding="iso-8859-1"?>')
                    XMLMAIKER (DtSt + AUF + Bschaffen ,'<Bookings xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">')        
                    TEW_DAT =+1
                if len(FBNR) > 0:
                    print (BarCode)
                    
                    if FBNR_ALT != BarCode:
                        if FBNR_ALT != '':
                            XMLMAIKER (DtSt + AUF + Bschaffen ,'  </Booking>')
                        XMLMAIKER (DtSt + AUF + Bschaffen ,'  <Booking>')
                        XMLMAIKER (DtSt + AUF + Bschaffen ,'    <FBHeader>')
                        #XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <FID>28a201c1-971e-439d-a33b-17ee1f3ce3e7</FID>')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <FBNR>{FBNR}</FBNR>') if len(FBNR)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <FBNR />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <BookingCreator>{BookingCreator}</BookingCreator>') if len(BookingCreator)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <BookingCreator />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <KnNr>9686</KnNr>') 
                        #x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <TrgKnNr>{TrgKnNr}</TrgKnNr>') if len(TrgKnNr)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <TrgKnNr />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <TrackTraceNr>{TrackTraceNr}</TrackTraceNr>') if len(TrackTraceNr)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <TrackTraceNr />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <TerminalNr>{TerminalNr}</TerminalNr>') if len(TerminalNr)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <TerminalNr />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Reference>{Reference}</Reference>') if len(Reference)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Reference />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Reference2>{Reference2}</Reference2>') if len(Reference2)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Reference2 />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Reference3>{Reference3}</Reference3>') if len(Reference3)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Reference3 />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <BookingType>{BookingType}</BookingType>') if len(BookingType)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <BookingType />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ProduktionTest>{ProduktionTest}</ProduktionTest>') if len(ProduktionTest)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ProduktionTest />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Omex>{Omex}</Omex>') if len(Omex)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Omex />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <OmexTnrAfh>{OmexTnrAfh}</OmexTnrAfh>') if len(OmexTnrAfh)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <OmexTnrAfh />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <OmexTnrVia>{OmexTnrVia}</OmexTnrVia>') if len(OmexTnrVia)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <OmexTnrVia />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <OmexTnrLev>{OmexTnrLev}</OmexTnrLev>') if len(OmexTnrLev)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <OmexTnrLev />')
                        XMLMAIKER (DtSt + AUF + Bschaffen ,'    </FBHeader>')
                        FBNR_ALT = BarCode
                        XMLMAIKER (DtSt + AUF + Bschaffen ,'    <SenderAddress>')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderKnNr>{SenderKnNr}</SenderKnNr>') if len(SenderKnNr)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderKnNr />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderName>{SenderName}</SenderName>') if len(SenderName)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderName />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderAddressLine1>{SenderAddressLine1}</SenderAddressLine1>') if len(SenderAddressLine1)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderAddressLine1 />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderAddressLine2>{SenderAddressLine2}</SenderAddressLine2>') if len(SenderAddressLine2)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderAddressLine2 />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderAddressLine3>{SenderAddressLine3}</SenderAddressLine3>') if len(SenderAddressLine3)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderAddressLine3 />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderCity>{SenderCity}</SenderCity>') if len(SenderCity)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderCity />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderZip>{SenderZip}</SenderZip>') if len(SenderZip)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderZip />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderCountry>{SenderCountry}</SenderCountry>') if len(SenderCountry)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderCountry />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderPhoneNo>{SenderPhoneNo}</SenderPhoneNo>') if len(SenderPhoneNo)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderPhoneNo />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderMail>{SenderMail}</SenderMail>') if len(SenderMail)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <SenderMail />')
                        XMLMAIKER (DtSt + AUF + Bschaffen ,'    </SenderAddress>')
                        XMLMAIKER (DtSt + AUF + Bschaffen ,'    <RecipientAddress>')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientKnNr>{RecipientKnNr}</RecipientKnNr>') if len(RecipientKnNr)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientKnNr />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientName>{RecipientName}</RecipientName>') if len(RecipientName)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientName />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientAddressLine1>{RecipientAddressLine1}</RecipientAddressLine1>') if len(RecipientAddressLine1)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientAddressLine1 />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientAddressLine2>{RecipientAddressLine2}</RecipientAddressLine2>') if len(RecipientAddressLine2)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientAddressLine2 />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientAddressLine3>{RecipientAddressLine3}</RecipientAddressLine3>') if len(RecipientAddressLine3)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientAddressLine3 />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientCity>{RecipientCity}</RecipientCity>') if len(RecipientCity)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientCity />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientZip>{RecipientZip}</RecipientZip>') if len(RecipientZip)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientZip />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientCountry>{RecipientCountry}</RecipientCountry>') if len(RecipientCountry)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientCountry />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientMail>{RecipientMail}</RecipientMail>') if len(RecipientMail)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientMail />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientPhoneNo>{RecipientPhoneNo}</RecipientPhoneNo>') if len(RecipientPhoneNo)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <RecipientPhoneNo />')
                        XMLMAIKER (DtSt + AUF + Bschaffen ,'    </RecipientAddress>')
                        XMLMAIKER (DtSt + AUF + Bschaffen ,'    <General>')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Notes>{Notes}</Notes>') if len(Notes)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Notes />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <DeliveryDate>{DeliveryDate}</DeliveryDate>') if len(DeliveryDate)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <DeliveryDate />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <DeliveryTime>{DeliveryTime}</DeliveryTime>') if len(DeliveryTime)!='00:00' else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <DeliveryTime />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <TotalWeight>{TotalWeight}</TotalWeight>') if len(TotalWeight)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <TotalWeight />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <TotalVolume>{TotalVolume}</TotalVolume>') if len(TotalVolume)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <TotalVolume />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <TotalColli>{TotalColli}</TotalColli>') if len(TotalColli)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <TotalColli />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <TotalLDM>{TotalLDM}</TotalLDM>') if len(TotalLDM)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <TotalLDM />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Franco>{Franco}</Franco>') if len(Franco)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Franco />')
                        XMLMAIKER (DtSt + AUF + Bschaffen ,'    </General>')
                        XMLMAIKER (DtSt + AUF + Bschaffen ,'    <Specialities>')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <CODAmount>{CODAmount}</CODAmount>') if len(CODAmount)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <CODAmount />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <CollectionDate>{CollectionDate}</CollectionDate>') if len(CollectionDate)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <CollectionDate />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <CollectionTime>{CollectionTime}</CollectionTime>') if len(CollectionTime)!='00:00' else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <CollectionTime />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <DangerousGoods>{DangerousGoods}</DangerousGoods>') if len(DangerousGoods)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <DangerousGoods />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <CarPackage>{CarPackage}</CarPackage>') if len(CarPackage)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <CarPackage />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <CarPackage>{CarPackage}</CarPackage>') if len(CarPackage)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <CarPackage />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ExchangePallets>{ExchangePallets}</ExchangePallets>') if len(ExchangePallets)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ExchangePallets />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ExchangePallets1_1>{ExchangePallets1_1}</ExchangePallets1_1>') if len(ExchangePallets1_1)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ExchangePallets1_1 />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ExchangePallets1_2>{ExchangePallets1_2}</ExchangePallets1_2>') if len(ExchangePallets1_2)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ExchangePallets1_2 />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ExchangePallets1_4>{ExchangePallets1_4}</ExchangePallets1_4>') if len(ExchangePallets1_4)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ExchangePallets1_4 />')
                        XMLMAIKER (DtSt + AUF + Bschaffen ,'    </Specialities>')
                        XMLMAIKER (DtSt + AUF + Bschaffen ,'    <DescriptionOfGoods>')
                        db2 = pymssql.connect(server, user, password, db_name)
                        cursor2 = db2.cursor(as_dict=True)
                        cursor2.execute(sql_select2)
                        NVE2 = ''
                        for row2 in cursor2:
                            if len(NVE2) > 0:
                                NVE2 =NVE2 + ';' + str(row2['NVE']) if row2['NVE'] is not None else ''
                            else:
                                NVE2 = str(row2['NVE']) if row2['NVE'] is not None else ''
                        BarCode = NVE2 if BEZEICHN1 == 1 else BarCode
                        XMLMAIKER (DtSt + AUF + Bschaffen ,'      <AccountCode />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <LineNr>{LineNr}</LineNr>') if len(LineNr)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <LineNr />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <BarCode>{BarCode}</BarCode>') if len(BarCode)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <BarCode />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ColliType>{ColliType}</ColliType>') if len(ColliType)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ColliType />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <GoodsDescription>{GoodsDescription}</GoodsDescription>') if len(GoodsDescription)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <GoodsDescription />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Weight>{Weight}</Weight>') if len(Weight)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Weight />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Volume>{Volume}</Volume>') if len(Volume)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Volume />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <LDM>{LDM}</LDM>') if len(LDM)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <LDM />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ADR_UN>{ADR_UN}</ADR_UN>') if len(ADR_UN)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ADR_UN />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ParcelReference>{ParcelReference}</ParcelReference>') if len(ParcelReference)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ParcelReference />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Width>{Width}</Width>') if len(Width)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Width />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Length>{Length}</Length>') if len(Length)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Length />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Height>{Height}</Height>') if len(Height)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Height />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <colli>{colli}</colli>') if len(colli)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <colli />')
                        #x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <VID>{VID}</VID>') if len(VID)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <VID />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <UnNr>{UNnr}</UnNr>') if len(UNnr)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <UnNr />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Beskrivelse>{Beskrivelse}</Beskrivelse>') if len(Beskrivelse)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Beskrivelse />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Klasse>{Klasse}</Klasse>') if len(Klasse)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Klasse />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <EmbGruppe>{EmbGruppe}</EmbGruppe>') if len(EmbGruppe)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <EmbGruppe />')
                        x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Point>{Point}</Point>') if len(Point)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Point />')
                        XMLMAIKER (DtSt + AUF + Bschaffen ,'    </DescriptionOfGoods>')
                        db1 = pymssql.connect(server, user, password, db_name)
                        cursor1 = db1.cursor(as_dict=True)
                        cursor1.execute(sql_select1)
                        for row1 in cursor1:
                            TextNr = row1['TextNr'] if row1['TextNr'] is not None else 0
                            if TextNr>0:
                                XMLMAIKER (DtSt + AUF + Bschaffen ,'    <Services>')
                                x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Kode>{AVIS_STATUS(TextNr)}</Kode>') if len(AVIS_STATUS(TextNr))>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Kode />')
                                XMLMAIKER (DtSt + AUF + Bschaffen ,'    </Services>')
                    else:
                        #XMLMAIKER (DtSt,'  </Booking>')
                        if BEZEICHN1 > 1:
                            XMLMAIKER (DtSt + AUF + Bschaffen ,'    <DescriptionOfGoods>')
                            x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <LineNr>{LineNr}</LineNr>') if len(LineNr)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <LineNr />')
                            x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <BarCode>{BarCode}</BarCode>') if len(BarCode)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <BarCode />')
                            x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ColliType>{ColliType}</ColliType>') if len(ColliType)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ColliType />')
                            x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <GoodsDescription>{GoodsDescription}</GoodsDescription>') if len(GoodsDescription)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <GoodsDescription />')
                            x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Weight>{Weight}</Weight>') if len(Weight)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Weight />')
                            x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Volume>{Volume}</Volume>') if len(Volume)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Volume />')
                            x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <LDM>{LDM}</LDM>') if len(LDM)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <LDM />')
                            x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ADR_UN>{ADR_UN}</ADR_UN>') if len(ADR_UN)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ADR_UN />')
                            x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ParcelReference>{ParcelReference}</ParcelReference>') if len(ParcelReference)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <ParcelReference />')
                            x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Width>{Width}</Width>') if len(Width)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Width />')
                            x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Length>{Length}</Length>') if len(Length)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Length />')
                            x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Height>{Height}</Height>') if len(Height)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Height />')
                            x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <colli>{colli}</colli>') if len(colli)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <colli />')
#                            x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <VID>{VID}</VID>') if len(VID)>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <VID />')
                            x = XMLMAIKER (DtSt + AUF + Bschaffen ,'    </DescriptionOfGoods>')
                            db1 = pymssql.connect(server, user, password, db_name)
                            cursor1 = db1.cursor(as_dict=True)
                            cursor1.execute(sql_select1)
                            for row1 in cursor1:
                                TextNr = row1['TextNr'] if row1['TextNr'] is not None else 0
                                if TextNr>0:
                                    XMLMAIKER (DtSt + AUF + Bschaffen ,'    <Services>')
                                    x = XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Kode>{AVIS_STATUS(TextNr)}</Kode>') if len(AVIS_STATUS(TextNr))>0 else XMLMAIKER (DtSt + AUF + Bschaffen ,f'      <Kode />')
                                    XMLMAIKER (DtSt + AUF + Bschaffen ,'    </Services>')
            XMLMAIKER (DtSt + AUF + Bschaffen ,'  </Booking>')
            XMLMAIKER (DtSt + AUF + Bschaffen ,'</Bookings>')
            print ('end')
        
if __name__ == "__main__":
    print ('Begin')
    filenames = next(walk(mypathIN), (None, None, []))[2]  # [] if no file
    for fm in filenames:
        with open(mypathIN + fm) as file:
            for line in file:
               AUFTR = line.split("|")
               if AUFTR[0] == 'AUFTR':
                print (AUFTR[3])
                XMLmacher (AUFTR[3])