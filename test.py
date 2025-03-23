"""
Script: test.py
Description: [ADD DESCRIPTION HERE]
Usage: python test.py
"""

import pyodbc

server="srv-db1"
user = os.getenv('APP_USER', 'YOUR_USERNAME_HERE')
password = os.getenv('APP_PASSWORD', 'YOUR_PASSWORD_HERE')
db_name="WinSped"


def LiefNrUpdate (AUF,TrackTraceNr ):
    #db3 = pymssql.connect(server, user, password, db_name)
    #cursor3 = db3.cursor(as_dict=True)
    SQLLLLL =f"""use winsped update XXAAufExt set TrackandTraceEmail = '{TrackTraceNr}' where AufIntNr in (select AufIntNr from XXASLAuf where aufnr in ('{AUF}'))"""
    print (SQLLLLL)
    #cursor3.execute(SQLLLLL)
    file_3 = open('//srv-wss/Schnittstellen/DansckDistribution/UPD.SQL', 'a')
    file_3.write(SQLLLLL + '\n')
    file_3.close
    try:
        connection = pyodbc.connect(
            "Driver={SQL Server};"
            f"Server={server};"
            f"Database={db_name};"
            f"UID={user};"
            f"PWD={password};"
        )

        cursor = connection.cursor()
        print("Connected to SQL Server")
        
        return 1
        
    except pyodbc.Error as e:
        print(f"Error: {e}")
        return 2
        
    try:
        #update_query = "UPDATE users SET email = ? WHERE username = ?"
        update_query = "update XXAAufExt set TrackandTraceEmail ='?' where AufIntNr in (select AufIntNr from XXASLAuf where aufnr in ('?'))"
        user_data = (TrackTraceNr, AUF)
    
        #cursor.execute(update_query, user_data)
        cursor.execute(SQLLLLL)
        connection.commit()
        print("Data updated successfully")
    
    except pyodbc.Error as e:
        print(f"Error: {e}")
    
if __name__ == "__main__":
    print ('Begin')
    if LiefNrUpdate ('20274026','160167767550391167-TEST') == 1:
    #if LiefNrUpdate (AUF,TrackTraceNr) == 1:
        print ('ok')