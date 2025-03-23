"""
Script: Personio.py
Description: [ADD DESCRIPTION HERE]
Usage: python Personio.py
"""

import requests
import json
import os
import time
from time import gmtime , strftime
from dateutil import parser
from datetime import datetime, timedelta

LIST_PATCHT = f'//srv-wss/Schnittstellen/_Scripte/py/Personio/List_Time_Offs.json'
LIST_PATCHD = f'//srv-wss/Schnittstellen/_Scripte/py/Personio/PERSDATEN.json'
LIST_PATCHA = f'//srv-wss/Schnittstellen/_Scripte/py/Personio/absence-periods.json'
LIST_ATUCH =f'//srv-wss/Schnittstellen/_Scripte/py/Personio/Atuch.json'

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_absence_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data.get("data", [])

def parse_absence_periods(absence_data):
    parsed_periods = []
    for entry in absence_data:
        attributes = entry.get("attributes", {})
        employee = attributes.get("employee", {}).get("attributes", {})
        absence_type = attributes.get("absence_type", {}).get("attributes", {})
        
        parsed_periods.append({
            "id": attributes.get("id"),
            "employee_name": f"{employee.get('first_name', '')} {employee.get('last_name', '')}",
            "email": employee.get("email"),
            "absence_type": absence_type.get("name"),
            "start_date": attributes.get("start"),
            "end_date": attributes.get("end"),
            "effective_duration": attributes.get("effective_duration"),
            "status": attributes.get("status"),
            "breakdowns": attributes.get("breakdowns", [])
        })
    return parsed_periods

def print_absence_summary(parsed_periods):
    for period in parsed_periods:
        start_date = datetime.fromisoformat(period["start_date"][:-1])
        end_date = datetime.fromisoformat(period["end_date"][:-1])
        print(f"Employee: {period['employee_name']} ({period['email']})")
        print(f"Absence Type: {period['absence_type']}")
        print(f"Start Date: {start_date.strftime('%Y-%m-%d')} End Date: {end_date.strftime('%Y-%m-%d')}")
        print(f"Effective Duration: {period['effective_duration']} hours")
        print(f"Status: {period['status']}")
        print("Breakdowns:")
        for breakdown in period["breakdowns"]:
            print(f"  - {breakdown['date']}: {breakdown['effective_duration']} hours")
        print("-" * 40)

def TOKEN():
    
    with open(LIST_ATUCH, "r", encoding="utf-8") as file:
        data = json.load(file)
    # Extract and display relevant information
    if data.get("success"):
        token_data = data.get("data", {})
        parsed_data = {
            "Token": token_data.get("token")
        }
    # Print parsed data
        for key, value in parsed_data.items():
            print(value)
        return value
    else:
        print("The operation was not successful.")
        return 0
    
def ATUCH():
    if not os.path.exists(LIST_ATUCH):
        url = "https://api.personio.de/v1/auth"
        payload = {
            "client_id": "papi-4bd08fb2-fd47-48f1-bb84-ce91a383da8f",
            "client_secret": "papi-MjkxNDY2OWYtZjI5ZS00YTY0LWE5YTgtYTZjMjZjYzI0MThk"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        with open(f'//srv-wss/Schnittstellen/_Scripte/py/Personio/Atuch.json', 'wb') as out:
            out.write(response.content)
            out.close
    else: 
        current_time = int(time.time() )
        day = int(43200)
        file_location = os.path.join(os.getcwd(), LIST_ATUCH)
        file_time = int(os.stat(file_location).st_mtime) 
        print (current_time - file_time, day)
        if(current_time - file_time  > day): 
            print(f" Delete : {LIST_ATUCH}", file_time, current_time, day) 
            os.remove(file_location) 

def PERSDATEN():
    Token = TOKEN()
    if Token != 0:
            
        url = "https://api.personio.de/v1/company/employees"
        #url = "https://api.personio.de/v1/company/custom-reports/columns?columns=100"
        #url = "https://api.personio.de/v1/company/custom-reports/reports/report_id"
        #url = "https://api.personio.de/v1/company/absence-periods"
        headers = {
            "accept": "application/json",
            "X-Personio-Partner-ID": "chr-carstensen-logistics",
            "authorization": f"Bearer {Token}"
        }
        response = requests.get(url, headers=headers)
        print(response)
        with open(LIST_PATCHD, 'wb') as out:
            out.write(response.content)
            out.close
    else:
         print("The operation was not successful.")

def PERList_Time_Offs():
    Token = TOKEN()
    if Token != 0:
            
        #url = "https://api.personio.de/v1/company/employees"
        #url = "https://api.personio.de/v1/company/custom-reports/columns?columns=100"
        #url = "https://api.personio.de/v1/company/custom-reports/reports/report_id"
        url = "https://api.personio.de/v1/company/time-offs?limit=200&offset=0"
        headers = {
            "accept": "application/json",
            "X-Personio-Partner-ID": "chr-carstensen-logistics",
            "authorization": f"Bearer {Token}"
        }
        response = requests.get(url, headers=headers)
        print(response)
        with open(LIST_PATCHT, 'wb') as out:
            out.write(response.content)
            out.close
    else:
         print("The operation was not successful.")

def ABWESDATEN():
    Token = TOKEN()
    if Token != 0:
            
        #url = "https://api.personio.de/v1/company/employees"
        #url = "https://api.personio.de/v1/company/custom-reports/columns?columns=100"
        url = "https://api.personio.de/v1/company/employees?limit=10&offset=0&attributes[]=%3Fattributes%5B%5D%3Dfirst_name%26attributes%5B%5D%3Dlast_name%26attributes%5B%5D%3DPersonalnummer'"
        #url = "https://api.personio.de/v1/company/absence-periods"
        headers = {
            "accept": "application/json",
            "X-Personio-Partner-ID": "chr-carstensen-logistics",
            "authorization": f"Bearer {Token}"
        }
        response = requests.get(url, headers=headers)
        print(response)
        with open(LIST_PATCHA, 'wb') as out:
            out.write(response.content)
            out.close
    else:
         print("The operation was not successful.")

def parse_time_offs(data):
    time_offs = []
    
    for entry in data.get("data", []):
        attributes = entry.get("attributes", {})
        employee = attributes.get("employee", {}).get("attributes", {})
        time_off_type = attributes.get("time_off_type", {}).get("attributes", {})
        
        time_offs.append({
            "ID": time_off_type.get("id", ""),
            "Employee": f"{employee.get('first_name', {}).get('value', '')} {employee.get('last_name', {}).get('value', '')}",
            "Email": employee.get("email", {}).get("value", ""),
            "Start Date": attributes.get("start_date", ""),
            "End Date": attributes.get("end_date", ""),
            "Days Count": attributes.get("days_count", ""),
            "Status": attributes.get("status", ""),
            "Type": time_off_type.get("name", ""),
            "Category": time_off_type.get("category", ""),
        })
    
    return time_offs
    
from datetime import datetime, timedelta  # Import timedelta here, not inside the loop

def List_Time_Offs():
    filename = LIST_PATCHT  # Adjust if needed
    data = load_json(filename)
    parsed_data = parse_time_offs(data)

    today = datetime.now()
    three_days_ago = today + timedelta(days=8)
    print(three_days_ago)

    # Filter by email, status, and start date
    filtered_data = [
        entry for entry in parsed_data 
        if entry['Email'].endswith('@carstensen.eu') 
        and entry['Status'].endswith('approved')
    ]

    # Sort by Start Date
    sorted_data = sorted(filtered_data, key=lambda x: datetime.fromisoformat(x["Start Date"][:-6] + ":00"))

    # Prepare the PowerShell script
    ps_script_lines = []

    # Generate the PowerShell script for each employee
    for entry in sorted_data:
        start_date = parser.parse(entry["Start Date"]).replace(tzinfo=None)
        print(f'{today} <= {start_date} <= {three_days_ago}')

        if today <= start_date <= three_days_ago:
            print(start_date)
            end_date = parser.parse(entry["End Date"])

            # Check if start_date and end_date are the same and adjust end_date if necessary
            if start_date.strftime("%Y-%m-%d %H:%M:%S") == end_date.strftime("%Y-%m-%d %H:%M:%S"):
                end_date += timedelta(hours=23)

            ps_filename = f"//srv-wss/Schnittstellen/_Scripte/py/Personio/PS1/{entry['ID']}.ps1"
            ps_command = (f'Set-MailboxAutoReplyConfiguration -Identity "{entry["Email"]}" -AutoReplyState Scheduled '
                f'-StartTime "{start_date.strftime("%Y-%m-%d %H:%M:%S")}" -EndTime "{end_date.strftime("%Y-%m-%d %H:%M:%S")}" '
                f'-InternalMessage "<!DOCTYPE html><html><style> body > p {{ font-size: 9px; font-family: Arial, sans-serif; color: #000000;}}</style>'
                f'<body><p>Dear Sender,<br><br>Thank you for your email. I am currently out of the office until {end_date.strftime("%Y-%m-%d")}.<br><br>'
                f'If you need immediate assistance, please contact Info@carstensen.eu.<br><br>Thank you for your understanding.</p></body></html>"')

            with open(ps_filename, "w", encoding="utf-8") as ps_file:
                ps_file.write(ps_command + "\n")

            print(f"PowerShell script written to {ps_filename}")

        #ps_script_lines.append(ps_command)

    # Write the PowerShell script to a file
    
    
        #for line in ps_script_lines:
        #    ps_filename = f"//srv-wss/Schnittstellen/_Scripte/py/Personio/PS1/{entry["ID"]}.ps1"
        #    with open(ps_filename, "w", encoding="utf-8") as ps_file:
        #        ps_file.write(line + "\n")
        #        ps_file.close    
        #        print(f"PowerShell script written to {ps_filename}")


if __name__ == "__main__":
    
    
    ATUCH()
    
    PERSDATEN()
    
    #ABWESDATEN()
    
    PERList_Time_Offs()
    
    file_path = LIST_PATCHD
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    employees = data.get("data", [])

    parsed_employees = []
    for employee in employees:
        attributes = employee.get("attributes", {})
        parsed_employees.append({
            "ID": attributes.get("id", {}).get("value"),
            "First Name": attributes.get("first_name", {}).get("value"),
            "Last Name": attributes.get("last_name", {}).get("value"),
            "Preferred Name": attributes.get("preferred_name", {}).get("value"),
            "Email": attributes.get("email", {}).get("value"),
            "Status": attributes.get("status", {}).get("value"),
            "URLAUB_ID": attributes.get("absence_entitlement", {}).get("value", [{}])[0].get("attributes", {}).get("id"),
            "URLAUB_TYPE": attributes.get("absence_entitlement", {}).get("value", [{}])[0].get("attributes", {}).get("name"),
            "URLAUB_CTEGORY": attributes.get("absence_entitlement", {}).get("value", [{}])[0].get("attributes", {}).get("category"),
            "Absence Entitlement": attributes.get("absence_entitlement", {}).get("value", [{}])[0].get("attributes", {}).get("entitlement")
        })


    # Print the parsed employee data
    for employee in parsed_employees:
        if employee['Email'].endswith('@carstensen.eu'):# and datetime.fromisoformat(employee["Start Date"][:-1]) >= three_days_ago:
            print(employee['ID'], employee['First Name'], employee['Last Name'], employee['Preferred Name'],employee['Email'], employee['Status'],employee['URLAUB_ID'],employee['URLAUB_TYPE'],employee['URLAUB_CTEGORY'],employee['Absence Entitlement'])
    os.remove(LIST_PATCHD)
    
    List_Time_Offs()
    
    #file_path = LIST_PATCHA
    #absence_data = load_absence_data(file_path)
    #parsed_periods = parse_absence_periods(absence_data)
    #print_absence_summary(parsed_periods)
    
    