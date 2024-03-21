import os
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from collections import defaultdict

class Questions:
    def __init__(self, id, level, data_collection_method, category, sub_cat, item_stem, anchor):
        self.id = id
        self.level = level
        self.dcm = data_collection_method
        self.category = category
        self.sub_cat = sub_cat
        self.question = item_stem
        self.anchor = anchor

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
spreadsheet_id = "1nOYY4SqnoJ3il2QJ7vMOngiIXLBKX2pgskLNoDUdPC4"
range_name = ['Career Development!A2:Z', 'Community Engagement!A2:Z', 'Student-Athlete Performance!A2:Z', 'Personal Development, Misc.!A2:Z']

def main():
    creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        data = {}
        id = 0
        id_and_questions = {}
        for spread in range_name:
            service = build("sheets", "v4", credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = (
                sheet.values()
                .get(spreadsheetId=spreadsheet_id, range=spread)
                .execute()
            )
            #Values is a list of the rows in the spreadsheets
            
            values = result.get("values", [])

            if not values:
                print("No data found.")
                return
            
            #Making each entry in values to be a Questions object
            category = spread[:len(spread) - 5]
            sub_categories = defaultdict(list)
            for i in range(len(values)):
                temp = values[i]
                if spread == 'Career Development!A2:Z':
                    values[i] = Questions(id, temp[0], temp[3], category, temp[4], temp[5], temp[7])
                else:
                    values[i] = Questions(id, temp[0], temp[3], category, temp[4], temp[5], temp[6])
                sub = values[i].sub_cat.split("->")
                values[i].sub_cat = sub
                sub_categories[sub[0]].append(values[i])
                id_and_questions[values[i].id] = values[i]
                id += 1
            #Adding sheet into data dictionary with its sheet name as keys
            data[category] = sub_categories
        return (data, id_and_questions)

    except HttpError as err:
        print(err)


if __name__ == "__main__":
  main()