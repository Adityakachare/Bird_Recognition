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
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

creds_data = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN"),
}



# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, scope)
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

            # Remove empty values from each record
            filtered_records = []
            for record in records:
                cleaned_record = {k: v for k, v in record.items() if v != ""}
                if cleaned_record:  # Only add non-empty records
                    filtered_records.append(cleaned_record)

            all_data[sheet.title] = filtered_records

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