import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client-secret.json", scope)
client = gspread.authorize(creds)

timeStamps = client.open("Limelight Data Calculations").get_worksheet(2)

timeStamps.update_cell(1,5, "hello")