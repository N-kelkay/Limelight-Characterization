import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client-secret.json", scope)
client = gspread.authorize(creds)

pp = pprint.PrettyPrinter()
dataCalc = client.open("Limelight Data Calculations").sheet1
rawData = client.open("Limelight Data Calculations").get_worksheet(1)
timeStamps = client.open("Limelight Data Calculations").get_worksheet(2)

#Coverts a time stamp from minutes to miliseconds
def getMiliSec(value):
    split1Ind = value.split(' ')
    time = ""
    for x in split1Ind: # finds the time it was split
        if ':' in x:
            time = x
            break
    splitTime = time.split(':') #splits the time Ex: '1:25.28' -> ['1', '25.28']
    toMiliSecConvertion = (int(splitTime[0]) * 60 + int(splitTime[1].split('.')[0])) * 1000
    return(toMiliSecConvertion)

#converts all stamp time to miliseconds
columnAdata = timeStamps.col_values(1)
columnAdata.pop(0)
listOfMiliSeconds = []
for x in columnAdata:
    listOfMiliSeconds.append(getMiliSec(x))

#adds the time stamps into the time stamps sheet
# i = 0
# while i <= len(listOfMiliSeconds):
#     timeStamps.update_cell(i + 1, 3, listOfMiliSeconds[i])
#     i += 1
