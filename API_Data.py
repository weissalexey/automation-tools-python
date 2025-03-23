"""
Script: API_Data.py
Description: [ADD DESCRIPTION HERE]
Usage: python API_Data.py
"""

#
#           Lixfeld Invoices to PDF
#
import requests
import json
import time
import base64
import datetime
from datetime import date, timedelta
path = r'//srv-dc2/DATEN$/FiBu/FiBu/CCL Lüdenscheid GmbH'
#path = r'n:\IT\script\getmyinvoicesLIXFELD\json'
FILE_NAME = r'E:/Schnittstellen/_Scripte/py/LIXFELDINVOISES/INI.JSON'
#FILE_NAME = 'INI.JSON'
def Api_json(FILE_NAME):
    import json 
    f = open(FILE_NAME)
    data = json.load(f)
    f.close()
    return data['API']

# Constant
key = Api_json(FILE_NAME)
headers = { 'X-API-KEY' : key}
param = {'documentApproval': True}
url = 'https://api.getmyinvoices.com/accounts/v3/documents/'
#VERZ= f'N:\IT\script\getmyinvoices\IT\'

# variable
#doc = '17820378'

# abfrage aller DocumentIDs über die API Documents ohne zuordnung + anschließendes speichern in einer Datei

all_doc_id = []

all_doc = requests.get(url, headers = headers)
all_doc_json = all_doc.json()

#print(all_doc_json)
for doc in all_doc_json['records']:
    tag = doc['tags']
    pay_status = doc['paymentStatus']
    all_doc_id.append(doc['documentUid'])
    #if tag != [] and pay_status != 'Paid':
        #print(tag)
    #    all_doc_id.append(doc['documentUid'])
print(all_doc_id)


# datei in der alle Werte gespeichert werden, die bereits exportiert wurden



# Filter
for doc in all_doc_id:
    with open(f'E:/Schnittstellen/_Scripte/py/LIXFELDINVOISES/all_data.txt') as d:
        if not str(doc) in d.read(): 
            d.close()
        
            data = requests.get( url + str(doc), headers = headers, params = param)
        # format data
            data_json_2 = data.json()
            data_json = data_json_2['meta_data']
            print (data_json)
        # get data
            if 'workflowDetails' in data_json:
                try:     
                    #currentWorkflowStep = data_json['workflowDetails']['currentWorkflowStep']['name']
                    currentWorkflowStep = data_json['workflowDetails']['currentWorkflowStep']['name']
                    Tag = data_json['tags']
                    DocumentID = data_json['documentUid']
                    DocumentCR = data_json['createdAt']
                    YYYY = DocumentCR[:4]
                    DD= str(DocumentCR[8:10])
                    if DD[:1] == '0' : 
                        DD= str(DocumentCR[8:10]).replace('0','')
                    MM= str(DocumentCR[5:7])
                    if MM[:1] == '0' : 
                        MM= str(DocumentCR[5:7]).replace('0','')
                    
                    print (DocumentCR)
                    print(YYYY + '-'+ MM +'-'+DD)
                    #DocumentCR = DocumentCR.erplace('-', ',')
                    DATEVONDOC = datetime.date(int(YYYY),int(MM),int(DD))
                    DATEAB = datetime.date(2024,1,1)
                    if DATEAB < DATEVONDOC :
                        #print(currentWorkflowStep)
                        file_content = data_json_2['fileContent']
                        #DateiName =   + "-" + DocumentID + ".pdf"
                        pdf = open(f'{path}/{DocumentCR}_{DocumentID}.pdf', 'xb')
                        #print (f'{path}\{DocumentCR}-{DocumentID}.pdf')
                        #pdf = open(f'n:\IT\script\getmyinvoicesLIXFELD\json\1{DocumentCR}-{DocumentID}.pdf', 'xb')
                        pdf.write(base64.b64decode(file_content))
                        pdf.close()
                        # requests
                        file_2 = open(f'E:/Schnittstellen/_Scripte/py/LIXFELDINVOISES/all_data.txt', 'a')
                        file_2.write(str(doc)+ '\n')
                        file_2.close()
                        #print(f'n:\IT\script\getmyinvoicesLIXFELD\json\1{DocumentCR}-{DocumentID}.pdf')
                except:
                    print('kein workflow')
                        
                else:
                    print('nicht gespeichert')

        
        