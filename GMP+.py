"""
Script: GMP+.py
Description: [ADD DESCRIPTION HERE]
Usage: python GMP+.py
"""

import os, shutil
import cv2
from pdf2image import convert_from_path
import time
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'c:\Program Files\Tesseract-OCR\tesseract.exe'
print("Begin")
NOGMP_folder = '//srv-wss/Schnittstellen/_Scripte/py/GMP+/NOGMP'
img_folder = '//srv-wss/Schnittstellen/_Scripte/py/GMP+/PNG'
GMP_folder = '//srv-wss/Schnittstellen/_Scripte/py/GMP+/GMP'
poppler = r"c:\poppler\Library\bin"
for file in os.listdir(img_folder):
    file1 = file.upper()
    if file1.endswith('.PNG'):
        png_path = os.path.join(img_folder, file)
        print (file)
        img = cv2.imread(png_path)
        text = pytesseract.image_to_string(img)
        #print(text)
        index = text.find("GMP")
        if index == -1:
            print("es ist Kein GMP +")
            try:
                shutil.move(png_path, NOGMP_folder + f'/{file}')
            except:
                print (1)
        else:
            print("es ist GMP +")
            try:
                shutil.move(png_path, GMP_folder + f'/{file}')
            except:
                print (2)
print("Finished!")

