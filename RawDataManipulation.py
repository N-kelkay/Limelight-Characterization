import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client-secret.json", scope)
client = gspread.authorize(creds)

pp = pprint.PrettyPrinter()
rawData = client.open("Limelight Data Calculations").get_worksheet(1)




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

camtranData = rawData.col_values(2)
#pp.pprint(camtranData)
camtranData.pop(0)
listOfxzyaw = []

for x in camtranData: #x is a string of the values
    returnValue = cutList(x)
    listOfxzyaw.append(returnValue)

print(len(listOfxzyaw[1]))



#Adds the trimmed list to the sheet
#It first converts the list into a string
i = 0
while i <= len(listOfxzyaw): #needs to start at 2, 4
    if len(listOfxzyaw[i]) == 0:
        i += 1
    else:
        toStringChg = "[" + str(listOfxzyaw[i][0]) + " " +  str(listOfxzyaw[i][1]) + " " + str(listOfxzyaw[i][2]) + "]"
        rawData.update_cell(2 + i, 4, toStringChg)
        i += 1