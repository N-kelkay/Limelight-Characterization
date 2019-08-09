import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client-secret.json", scope)
client = gspread.authorize(creds)

pp = pprint.PrettyPrinter()
rawData = client.open("Limelight Data Calculations").get_worksheet(1)

camtranData = rawData.col_values(2)
#pp.pprint(camtranData)
camtranData.pop(0)
listOfxzyaw = []

fullList = camtranData[2000] #it's a string--> '[-12.42504555564065, 0.42380815721145304, -22.18154928200209, 2.2081758051849913, -31.255522674289537, -0.3133550209905969]'



#Finds the x, z, and yaw as a float number 
#If the passed in value is empty it returns an empty string
def cutList (value):
    if len(value) < 30: # if characters are less than 30, which is for [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], then do not pass it to the algorithem
        return ""
    else:
        actualList = list(value.split(","))
        x = float(actualList[0].replace("[", ""))
        z = float(actualList[2].replace(" ", ""))
        yaw = float(actualList[4].replace(" ", ""))
        return [x, z, yaw]
