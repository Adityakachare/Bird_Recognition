# # Run this script to test the connection to Google Sheets API


# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import os

# # Path to Service Account JSON Key
# CREDS_FILE = os.path.join(os.path.dirname(__file__), "birdrecognition-453108-104136d02cca.json")
# SHEET_ID = "1-JaaQ-4hNawlJwdHQ9u-HxguSB_C6wJpY0vVQtDYad0"  # Make sure this is correct


# # Check if credentials file exists
# if not os.path.exists(CREDS_FILE):
#     print(f"❌ Error: Credentials file '{CREDS_FILE}' not found!")
#     exit(1)

# # Define API Scope
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
# client = gspread.authorize(creds)

# try:
#     # ✅ FIX: Use open_by_key with correct ID
#     spreadsheet = client.open_by_key(SHEET_ID)
#     print("✅ Successfully connected to Google Sheets!")

#     # List all worksheet names to confirm access
#     sheet_names = [sheet.title for sheet in spreadsheet.worksheets()]
#     print(f"📄 Available Sheets: {sheet_names}")

#     # Fetch data from the first sheet
#     first_sheet = spreadsheet.worksheets()[0]  # Get the first worksheet
#     records = first_sheet.get_all_records()

#     # Display a sample of the data
#     if records:
#         print(f"📊 First 5 records: {records[:5]}")
#     else:
#         print("⚠️ No data found in the first sheet.")

# except gspread.exceptions.APIError as e:
#     print(f"❌ Google Sheets API Error: {e}")
# except Exception as e:
#     print(f"❌ Unexpected Error: {type(e).__name__}: {e}")

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Fetch credentials from .env
sheet_id = os.getenv("GOOGLE_SHEET_ID")
private_key = os.getenv("PRIVATE_KEY").replace('\\n', '\n')  # Ensure line breaks are preserved
creds_data = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": private_key,
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN")
}

# Define API Scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

try:
    # ✅ Use credentials from env as a JSON object
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, scope)
    client = gspread.authorize(creds)

    # ✅ Connect to the Google Sheet
    spreadsheet = client.open_by_key(sheet_id)
    print("✅ Successfully connected to Google Sheets!")

    # List all worksheet names to confirm access
    sheet_names = [sheet.title for sheet in spreadsheet.worksheets()]
    print(f"📄 Available Sheets: {sheet_names}")

    # Fetch data from the first sheet
    first_sheet = spreadsheet.worksheets()[0]  # Get the first worksheet
    records = first_sheet.get_all_records()

    # Display a sample of the data
    if records:
        print(f"📊 First 5 records: {records[:5]}")
    else:
        print("⚠️ No data found in the first sheet.")

except gspread.exceptions.APIError as e:
    print(f"❌ Google Sheets API Error: {e}")
except Exception as e:
    print(f"❌ Unexpected Error: {type(e).__name__}: {e}")
