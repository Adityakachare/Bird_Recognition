# from flask import Flask, request, send_file, jsonify
# from flask_cors import CORS  # Import CORS
# import os
# from convert_audio import convert_to_wav
# from werkzeug.utils import secure_filename
# from flask_cors import cross_origin
# from create_spectogram import generate_spectrogram
# import gspread
# import pandas as pd
# from oauth2client.service_account import ServiceAccountCredentials

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Load Google Sheets API credentials
# # CREDS_FILE = "backend/service_account.json"  # Ensure this path is correct
# # CREDS_FILE = os.path.join(os.path.dirname(__file__), "service_account.json")
# CREDS_FILE = os.path.join(os.path.dirname(__file__), "service_account.json")

# SHEET_ID = "1sp7MEKa0fsKJHin7a6IhisijZy3_Cd4y"  # Replace with actual Google Sheet ID

# # Google Sheets API setup
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
# client = gspread.authorize(creds)

# # Open the Google Spreadsheet
# spreadsheet = client.open_by_key(SHEET_ID)


# # New Route to Fetch Bird Data
# @app.route("/birds", methods=["GET"])
# @cross_origin()
# def get_bird_data():
#     all_data = {}

#     for sheet in spreadsheet.worksheets():
#         records = sheet.get_all_records()
#         df = pd.DataFrame(records) if records else pd.DataFrame(columns=["No data available"])
#         all_data[sheet.title] = df.to_dict(orient="records")

#     return jsonify(all_data)


# # Existing Audio Conversion Route
# @app.route("/convert", methods=["POST"])
# @cross_origin()
# def upload_and_convert():
#     if "audio" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     audio_file = request.files["audio"]

#     if audio_file.filename == "":
#         return jsonify({"error": "No selected file"}), 400

#     filename = secure_filename(audio_file.filename)

#     try:
#         # Convert audio to WAV in memory
#         wav_io = convert_to_wav(audio_file)
#     except Exception as e:
#         return jsonify({"error": f"Conversion failed: {str(e)}"}), 500

#     return send_file(
#         wav_io,
#         mimetype="audio/wav",
#         as_attachment=True,
#         download_name=f"{filename.rsplit('.', 1)[0]}.wav"
#     )


# # Existing Spectrogram Generation Route
# @app.route("/spectrogram", methods=["POST"])
# @cross_origin()
# def generate_spectrogram_route():
#     if "wavFile" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     wav_file = request.files["wavFile"]

#     if wav_file.filename == "":
#         return jsonify({"error": "No selected file"}), 400

#     filename = secure_filename(wav_file.filename)

#     try:
#         # Generate the spectrogram in memory
#         spectrogram_img = generate_spectrogram(wav_file)
#     except Exception as e:
#         return jsonify({"error": f"Spectrogram generation failed: {str(e)}"}), 500

#     return send_file(
#         spectrogram_img,
#         mimetype="image/png",
#         as_attachment=True,
#         download_name=f"{filename.rsplit('.', 1)[0]}_spectrogram.png"
#     )


# if __name__ == "__main__":
#     app.run(debug=True, use_reloader=False)

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS  # Import CORS
import os
from convert_audio import convert_to_wav
from werkzeug.utils import secure_filename
from flask_cors import cross_origin
from create_spectogram import generate_spectrogram
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load Google Sheets API credentials
CREDS_FILE = os.path.join(os.path.dirname(__file__), "birdrecognition-453108-104136d02cca.json")
SHEET_ID = "1-JaaQ-4hNawlJwdHQ9u-HxguSB_C6wJpY0vVQtDYad0"  # Use correct Google Sheet ID

# Check if credentials file exists
if not os.path.exists(CREDS_FILE):
    print(f"❌ Error: Credentials file '{CREDS_FILE}' not found!")
    exit(1)

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
client = gspread.authorize(creds)

# Open Google Sheet safely
try:
    spreadsheet = client.open_by_key(SHEET_ID)
    print("✅ Successfully connected to Google Sheets!")
except Exception as e:
    print(f"❌ Google Sheets API Error: {e}")
    spreadsheet = None  # Avoid crashes if API fails

# Route to Fetch Bird Data
@app.route("/birds", methods=["GET"])
@cross_origin()
def get_bird_data():
    if not spreadsheet:
        return jsonify({"error": "Unable to connect to Google Sheets"}), 500

    all_data = {}

    try:
        for sheet in spreadsheet.worksheets():
            records = sheet.get_all_records()
            df = pd.DataFrame(records) if records else pd.DataFrame(columns=["No data available"])
            all_data[sheet.title] = df.to_dict(orient="records")

        return jsonify(all_data)

    except Exception as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500


# Audio Conversion Route
@app.route("/convert", methods=["POST"])
@cross_origin()
def upload_and_convert():
    if "audio" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    audio_file = request.files["audio"]

    if audio_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(audio_file.filename)

    try:
        # Convert audio to WAV in memory
        wav_io = convert_to_wav(audio_file)
    except Exception as e:
        return jsonify({"error": f"Conversion failed: {str(e)}"}), 500

    return send_file(
        wav_io,
        mimetype="audio/wav",
        as_attachment=True,
        download_name=f"{filename.rsplit('.', 1)[0]}.wav"
    )


# Spectrogram Generation Route
@app.route("/spectrogram", methods=["POST"])
@cross_origin()
def generate_spectrogram_route():
    if "wavFile" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    wav_file = request.files["wavFile"]

    if wav_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(wav_file.filename)

    try:
        # Generate the spectrogram in memory
        spectrogram_img = generate_spectrogram(wav_file)
    except Exception as e:
        return jsonify({"error": f"Spectrogram generation failed: {str(e)}"}), 500

    return send_file(
        spectrogram_img,
        mimetype="image/png",
        as_attachment=True,
        download_name=f"{filename.rsplit('.', 1)[0]}_spectrogram.png"
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
