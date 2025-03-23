"""
Script: DD_Stat_NEW.py
Description: [ADD DESCRIPTION HERE]
Usage: python DD_Stat_NEW.py
"""

import os
import shutil
import logging
import requests
import pyodbc
import xml.etree.ElementTree as ET
from datetime import datetime
import random

# Настройка логирования
log_dir = "//srv-wss/Schnittstellen/_Scripte/log/"
#log_dir = "c:/temp/DD/log/"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}_DD_Stat_ERR.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

def write_log(message):
    logging.info(message)
    

def sql_result(query):
    write_log(query)
    conn_str = (
        "DRIVER={SQL Server};"
        "SERVER=srv-db1;"
        "DATABASE=WinSped;"
        "UID=gobabygo;"
        "PWD=comeback;"
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return f"{row[0]};{row[1]}" if row[1] else f"{row[0]};"
    return ""

def http_download(url, file_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        write_log(f"Downloaded {url} to {file_path}")
    except requests.RequestException as e:
        write_log(f"Error downloading {url}: {e}")

def process_files(directory, backup_dir, image_dir):
    if not os.path.exists(directory):
        write_log(f"Directory {directory} not found")
        return
    
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        write_log(f"Processing {file_path}")
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            for child in root:
                identifier = child.get("identifier", "")
                print(identifier)
                sql_query = f"""
                    SELECT SLAuf.AufNr, Nve.AufPosNr FROM XXASLAuf SLAuf
                    LEFT JOIN XXAAufExt TT ON SLAuf.AufIntNr = TT.AufIntNr
                    LEFT JOIN XXANVE NVE ON NVE.AufIntNr = SLAuf.AufIntNr
                    WHERE NVE.NVE = '{identifier}' OR TT.TrackandTraceEmail = '{identifier[:18]}'
                """
                result = sql_result(sql_query)
                
                if result:
                    aufnr, aufposnr = result.split(";")
                    print (aufnr, aufposnr)
                    for subchild in child:
                        ttime = subchild.get("time", "")
                        
                        ttype = subchild.get("type", "")
                        text = subchild.get("Text", "") or subchild.get("POD", "") or subchild.get("IMAGE", "")
                        print (aufnr, ttype, text) 
                        if len(aufnr.strip()) > 5:
                            status_file(aufnr, aufposnr, ttype, ttime, text)
                        
                        pod_url = subchild.get("POD", "")
                        image_url = subchild.get("IMAGE", "")
                        
                        if pod_url:
                            http_download(pod_url, os.path.join(image_dir, f"{identifier}_SIGN.PNG"))
                        if image_url:
                            http_download(image_url, os.path.join(image_dir, f"{identifier}_IMAGE.JPG"))
                    
            shutil.move(file_path, os.path.join(backup_dir, file_name))
        except Exception as e:
            write_log(f"Error processing {file_name}: {e}")

def status_file(aufnr, aufposnr, ttype, ttime, text):
    try:
        lisdat = ttime[:10].replace("-", "")
        liszeit = ttime[-8:].replace(":", "")
        RANDOMZHAL = str(random.random()).replace(".","")[:6]
        rndgen = str(hash(RANDOMZHAL))
        output_dir = "//srv-wss/Schnittstellen/DansckDistribution/out/LIS_IN_IN/"
        #output_dir = "c:/temp/DD/IN/"
        os.makedirs(output_dir, exist_ok=True)
        RANDOMZHAL = str(random.random()).replace(".","")[:6]
        file_name = f"D_DISTR{rndgen}.txt"
        file_path = os.path.join(output_dir, file_name)
        
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"START|D_DISTR{rndgen}|{lisdat}|||DDISTR|||Carstensen||||||||||||\n")
            f.write(f"STATUS|D_DISTR{rndgen}||{aufnr}|{aufposnr}|||{ttype}|||{text}|{lisdat}|{liszeit}||||||||||||||||||||||||||||||||||||\n")
            f.write(f"ENDE|D_DISTR{rndgen}|0|0|0|0|0|0|1|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|\n")
        write_log(f"Written status file: {file_path}")
    except Exception as e:
        write_log(f"Error writing status file: {e}")

# Пути к директориям
directory = "//srv-wss/Schnittstellen/DansckDistribution/in/scan/"
#directory = "c:/temp/DD/scan/"
backup_dir = "//srv-wss/Schnittstellen/DansckDistribution/in/BCK/"
#backup_dir = "c:/temp/DD/BCK/"
image_dir = "//srv-wss/Schnittstellen/DansckDistribution/in/Image/"
#image_dir = "c:/temp/DD/Image/"
# Запуск обработки файлов
process_files(directory, backup_dir, image_dir)