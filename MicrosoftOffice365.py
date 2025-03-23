"""
Script: MicrosoftOffice365.py
Description: [ADD DESCRIPTION HERE]
Usage: python MicrosoftOffice365.py
"""


import requests
import json
from msal import ConfidentialClientApplication

# Ваши данные из Azure
CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = os.getenv('APP_SECRET', 'YOUR_SECRET_HERE')
TENANT_ID = "TENANT_ID"

# URL для получения токена
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

# Получение токена доступа
app = ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
token_response = app.acquire_token_for_client(scopes=SCOPES)

if "access_token" in token_response:
    access_token = token_response["access_token"]
else:
    raise Exception("Token ERROR")

# Данные встречи
event = {
    "subject": "Urlaub",
    "body": {
        "contentType": "HTML",
        "content": "Urlaub"
    },
    "start": {
        "dateTime": "2024-02-01T10:00:00",
        "timeZone": "UTC"
    },
    "end": {
        "dateTime": "2024-02-01T11:00:00",
        "timeZone": "UTC"
    },
    "location": {
        "displayName": "Urlaub"
    },
    "attendees": [
        {
            "emailAddress": {
                "address": "client@example.com",
                "name": "Alex Weiss"
            },
            "type": "required"
        }
    ]
}

# Запрос к Microsoft Graph API
headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
response = requests.post("https://graph.microsoft.com/v1.0/me/events", headers=headers, data=json.dumps(event))

if response.status_code == 201:
    print("Urlaub gebucht")
else:
    print(f"Ошибка: {response.status_code}, {response.text}")

