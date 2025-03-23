"""
Script: EXCHENGE.py
Description: [ADD DESCRIPTION HERE]
Usage: python EXCHENGE.py
"""

import subprocess
import pandas as pd
from datetime import datetime
import pytz

# Считываем данные из вашего источника (например, CSV или списка)
data = [
    {'Employee': 'Alex Weiss', 'Email': 'aw@carstensen.eu', 'Start Date': '2025-04-03T00:00:00+02:00', 'End Date': '2025-07-03T00:00:00+02:00', 'Days Count': 9, 'Status': 'approved', 'Type': 'Urlaub', 'Category': 'paid_vacation'},
    # Дополнительные данные...
]

# Преобразуем данные в DataFrame для удобной обработки
df = pd.DataFrame(data)

# Текущая дата в формате ISO 8601 с учётом часового пояса
today = datetime.now(pytz.timezone('Europe/Berlin'))  # Берлинский часовой пояс (CET/CEST)

# Функция для проверки даты отпуска
def is_vacation_today(start_date, end_date):
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)
    return start_date <= today <= end_date

# Функция для настройки автоответа
def set_autoreply(email, start_date, end_date):
    start_date_formatted = datetime.fromisoformat(start_date).strftime('%d.%m.%Y')
    end_date_formatted = datetime.fromisoformat(end_date).strftime('%d.%m.%Y')
    
    command = f"""
    Set-MailboxAutoReplyConfiguration -Identity "{email}" -AutoReplyState Scheduled -StartTime "{start_date_formatted}" -EndTime "{end_date_formatted}" `
    -InternalMessage "<!DOCTYPE html><html><style> body > p {{ font-size: 9px; font-family: Arial, sans-serif; color: #000000;}}</style><body><p>Dear Sender,<br><br>Thank you for your email. I am currently out of the office.<br><br>Thank you for your understanding.</p></body></html>" `
    -ExternalMessage "<!DOCTYPE html><html><style> body > p {{ font-size: 9px; font-family: Arial, sans-serif; color: #000000;}}</style><body><p>Dear Sender,<br><br>Thank you for your email. I am currently out of the office.<br><br>Thank you for your understanding.</p></body></html>" `
    -ExternalAudience All
    """
    print (command)
    try:
        subprocess.run(["powershell", "-Command", command], check=True)
        print(f"Auto-reply set for {email} from {start_date} to {end_date}.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting auto-reply for {email}: {e}")

# Обрабатываем каждый отпуски и настраиваем автоответы
for index, row in df.iterrows():
    if is_vacation_today(row['Start Date'], row['End Date']):
        print(f"Setting auto-reply for {row['Employee']} ({row['Email']}) from {row['Start Date']} to {row['End Date']}")
        set_autoreply(row['Email'], row['Start Date'], row['End Date'])
    else:
        print(f"{row['Employee']} is not on vacation today.")
