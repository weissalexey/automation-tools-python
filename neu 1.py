"""
Script: neu 1.py
Description: [ADD DESCRIPTION HERE]
Usage: python neu 1.py
"""

import requests

cookies = {
    'ASPSESSIONIDQWTSDDAB': 'OKNPGMFCKKEFOELDEHHEKDAA',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://cc.online-book.dk',
    'Connection': 'keep-alive',
    'Referer': 'https://cc.online-book.dk/sites/arkiv/start_ny_arkiv.asp',
    # 'Cookie': 'ASPSESSIONIDQWTSDDAB=OKNPGMFCKKEFOELDEHHEKDAA',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'frame',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=4',
}

data = {
    'T1': 'tn',
    'T2': 'carstensen',
    'B1': 'Login',
}

response = requests.post('https://cc.online-book.dk/adm/login.asp', cookies=cookies, headers=headers, data=data)

data = 'T4=&T1=&T15=&T2=&T16=&T3=&T7=&T14=&T8=&T11=&T21=&T12=&T20=&T13=&T19=&T5=&T18=&T9=&T17=&T6=&T10=&T22=&T23=&T24=&T25=&T26=&T27=&T28=&T29=&T30=&T31=&T32=27-06-2024&T33=&T34=&sort=modtagetDato&B1=S^%^F8g'

response = requests.post('https://cc.online-book.dk/sites/arkiv/vis_ny_liste.asp', cookies=cookies, headers=headers, data=data)
print(response)

return response.text

#LIST_PATCH = '//srv-wss/Schnittstellen/DansckDistribution/all_Coli.txt'
#file_3 = open(LIST_PATCH, 'w+')
#file_3.write(response.text)