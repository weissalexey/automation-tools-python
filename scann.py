"""
Script: scann.py
Description: [ADD DESCRIPTION HERE]
Usage: python scann.py
"""


import cv2
import pytesseract
import os
import sys
import easyocr
reader = easyocr.Reader(['en'])  # Поддержка цифр
pytesseract.pytesseract.tesseract_cmd = r'c:\Program Files\Tesseract-OCR\tesseract.exe'
custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'


def extract_text_and_rename(image_path):
    # Загрузка изображения
    image = cv2.imread(image_path)
    if image is None:
        print(f"ERRor {image_path}")
        return
    
    height, width, _ = image.shape
    roi = image[0:int(height * 0.2), int(width * 0.6):width]  # Верхний правый угол
    
    # Конвертация в серый цвет и обработка для улучшения OCR
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)  # Градации серого
    gray = cv2.GaussianBlur(gray, (3, 3), 0)  # Сглаживание для уменьшения шума
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)  # Локальная бинаризация
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)  # Увеличение масштаба
    
    # Распознавание текста
    #text = reader.readtext(gray, detail=0, allowlist='0123456789')
    #text = pytesseract.image_to_string(gray, config=custom_config).strip()
    text = pytesseract.image_to_string(gray, config='--psm 11').strip()
    
    print (text)
    if not text:
        print("NICT GEKLAPT")
        return
    
    # Формирование безопасного имени файла
    safe_text = "".join(c if c.isalnum() else "_" for c in text)
    new_filename = f"{safe_text}.jpg"
    
    # Переименование файла
    directory = os.path.dirname(image_path)
    new_path = os.path.join(directory, new_filename)
    os.rename(image_path, new_path)
    print(f"Unbenant: {new_filename}")

if __name__ == "__main__":
    #if len(sys.argv) < 2:
    #    print("Использование: python script.py путь_к_изображению")
    #else:
    extract_text_and_rename('//srv-wss/Schnittstellen/_Scripte/py/Scanner/in/test.jpg')
