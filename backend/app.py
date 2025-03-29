# # from flask import Flask, request, send_file, jsonify
# # from flask_cors import CORS, cross_origin
# # import os
# # import gspread
# # import pandas as pd
# # from werkzeug.utils import secure_filename
# # from dotenv import load_dotenv
# # from oauth2client.service_account import ServiceAccountCredentials

# # # Custom imports
# # from convert_audio import convert_to_wav
# # from create_spectogram import generate_spectrogram
# # from prediction import predict_bird


# # load_dotenv()
# # app = Flask(__name__)
# # CORS(app)  # Enable CORS for all routes


# # SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# # creds_data = {
# #     "type": os.getenv("TYPE"),
# #     "project_id": os.getenv("PROJECT_ID"),
# #     "private_key_id": os.getenv("PRIVATE_KEY_ID"),
# #     "private_key": os.getenv("PRIVATE_KEY").replace("\\n", "\n"),
# #     "client_email": os.getenv("CLIENT_EMAIL"),
# #     "client_id": os.getenv("CLIENT_ID"),
# #     "auth_uri": os.getenv("AUTH_URI"),
# #     "token_uri": os.getenv("TOKEN_URI"),
# #     "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
# #     "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
# #     "universe_domain": os.getenv("UNIVERSE_DOMAIN"),
# # }



# # # Google Sheets API setup
# # scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# # # creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
# # creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, scope)
# # client = gspread.authorize(creds)

# # # Open Google Sheet safely
# # try:
# #     spreadsheet = client.open_by_key(SHEET_ID)
# #     print("✅ Successfully connected to Google Sheets!")
# # except Exception as e:
# #     print(f"❌ Google Sheets API Error: {e}")
# #     spreadsheet = None  # Avoid crashes if API fails

# # app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB limit


# # # Route to Fetch Bird Data
# # @app.route("/birds", methods=["GET"])
# # @cross_origin()
# # def get_bird_data():
# #     if not spreadsheet:
# #         return jsonify({"error": "Unable to connect to Google Sheets"}), 500

# #     all_data = {}

# #     try:
# #         for sheet in spreadsheet.worksheets():
# #             records = sheet.get_all_records()

# #             # Remove empty values from each record
# #             filtered_records = []
# #             for record in records:
# #                 cleaned_record = {k: v for k, v in record.items() if v != ""}
# #                 if cleaned_record:  # Only add non-empty records
# #                     filtered_records.append(cleaned_record)

# #             all_data[sheet.title] = filtered_records

# #             bird_names = [
# #             row.get("bird name", "Unknown bird")
# #             for row in spreadsheet.get_worksheet(0).get_all_records()
# #         ]
# #         print("Bird names fetched:", bird_names)  # Debugging line

# #         return jsonify(all_data)

# #     except Exception as e:
# #         return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500



# # # Audio Conversion Route
# # @app.route("/convert", methods=["POST"])
# # @cross_origin()
# # def upload_and_convert():
# #     if "audio" not in request.files:
# #         return jsonify({"error": "No file uploaded"}), 400

# #     audio_file = request.files["audio"]

# #     if audio_file.filename == "":
# #         return jsonify({"error": "No selected file"}), 400

# #     filename = secure_filename(audio_file.filename)

# #     try:
# #         # Convert audio to WAV in memory
# #         wav_io = convert_to_wav(audio_file)
# #     except Exception as e:
# #         return jsonify({"error": f"Conversion failed: {str(e)}"}), 500

# #     return send_file(
# #         wav_io,
# #         mimetype="audio/wav",
# #         as_attachment=True,
# #         download_name=f"{filename.rsplit('.', 1)[0]}.wav"
# #     )


# # # Spectrogram Generation Route
# # @app.route("/spectrogram", methods=["POST"])
# # @cross_origin()
# # def generate_spectrogram_route():
# #     if "wavFile" not in request.files:
# #         return jsonify({"error": "No file uploaded"}), 400

# #     wav_file = request.files["wavFile"]

# #     if wav_file.filename == "":
# #         return jsonify({"error": "No selected file"}), 400

# #     filename = secure_filename(wav_file.filename)

# #     try:
# #         # Generate the spectrogram in memory
# #         spectrogram_img = generate_spectrogram(wav_file)
# #     except Exception as e:
# #         return jsonify({"error": f"Spectrogram generation failed: {str(e)}"}), 500

# #     return send_file(
# #         spectrogram_img,
# #         mimetype="image/png",
# #         as_attachment=True,
# #         download_name=f"{filename.rsplit('.', 1)[0]}_spectrogram.png"
# #     )

# # # Bird Species Prediction Route
# # # @app.route("/predict", methods=["POST"])
# # # @cross_origin()
# # # def bird_prediction():
# # #     try:
# # #         # audio_file = request.files.get("fileInput")
# # #         # if not audio_file:
# # #         #     return jsonify({"error": "No audio file uploaded"}), 400
# # #         if "fileInput" not in request.files:
# # #             return jsonify({"error": "No file received by server"}), 400

# # #         audio_file = request.files["fileInput"]

# # #         if audio_file.filename == "":
# # #             return jsonify({"error": "No file selected"}), 400


# # #         # Save the audio to a temporary file
# # #         temp_audio_path = "temp_audio.wav"
# # #         audio_file.save(temp_audio_path)

# # #         # Fetch bird names from the first worksheet in Google Sheets
# # #         bird_names = [
# # #             row.get("bird name", "Unknown bird")
# # #             for row in spreadsheet.get_worksheet(0).get_all_records()
# # #         ]

# # #         # Call the prediction function, passing the **file path** instead of file object
# # #         prediction_result = predict_bird(temp_audio_path, bird_names)

# # #         if "error" in prediction_result:
# # #             return jsonify({"error": prediction_result["error"]}), 500

# # #         return jsonify({"bird_species": prediction_result["bird_species"]})

# # #     except Exception as e:
# # #         return jsonify({"error": str(e)}), 500

# # #     finally:
# # #         # Ensure temp file gets removed after processing
# # #         if os.path.exists("temp_audio.wav"):
# # #             os.remove("temp_audio.wav")

# # # Bird Species Prediction Route (Improved Version)
# # @app.route("/predict", methods=["POST"])
# # @cross_origin()
# # def bird_prediction():
# #     try:
# #         # Check if audio file is present
# #         if "fileInput" not in request.files:
# #             return jsonify({"error": "No file received by server"}), 400

# #         audio_file = request.files["fileInput"]

# #         if audio_file.filename == "":
# #             return jsonify({"error": "No file selected"}), 400

# #         # Save the audio to a temporary file
# #         temp_audio_path = "temp_audio.wav"
# #         audio_file.save(temp_audio_path)

# #         # ✅ Refetch bird names from Google Sheets on each call
# #         try:
# #             bird_names_sheet = spreadsheet.get_worksheet(0).get_all_records()
# #             bird_names = [row.get("bird name", "Unknown bird") for row in bird_names_sheet]
# #             print("✅ Fresh Bird Names Fetched:", bird_names)  # Debug line to verify refresh
# #         except Exception as e:
# #             print(f"⚠️ Failed to refresh bird names: {e}")
# #             bird_names = ["Unknown bird"] * 101  # Fallback to ensure prediction still works

# #         # 🔥 Call the prediction function
# #         prediction_result = predict_bird(temp_audio_path, bird_names)

# #         if "error" in prediction_result:
# #             return jsonify({"error": prediction_result["error"]}), 500

# #         # Return bird species and confidence as JSON
# #         return jsonify({
# #             "bird_species": prediction_result["bird_species"],
# #             "confidence": prediction_result["confidence"]
# #         })

# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# #     finally:
# #         # 🧹 Ensure temp file gets removed after processing
# #         if os.path.exists("temp_audio.wav"):
# #             os.remove("temp_audio.wav")


# # if __name__ == "__main__":
# #     app.run(debug=True, use_reloader=False)

# from flask import Flask, request, send_file, jsonify
# from flask_cors import CORS, cross_origin
# import os
# import gspread
# import pandas as pd
# from werkzeug.utils import secure_filename
# from dotenv import load_dotenv
# from oauth2client.service_account import ServiceAccountCredentials

# # Custom imports
# from convert_audio import convert_to_wav
# from create_spectogram import generate_spectrogram
# from prediction import predict_bird

# load_dotenv()
# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# creds_data = {
#     "type": os.getenv("TYPE"),
#     "project_id": os.getenv("PROJECT_ID"),
#     "private_key_id": os.getenv("PRIVATE_KEY_ID"),
#     "private_key": os.getenv("PRIVATE_KEY").replace("\\n", "\n"),
#     "client_email": os.getenv("CLIENT_EMAIL"),
#     "client_id": os.getenv("CLIENT_ID"),
#     "auth_uri": os.getenv("AUTH_URI"),
#     "token_uri": os.getenv("TOKEN_URI"),
#     "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
#     "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
#     "universe_domain": os.getenv("UNIVERSE_DOMAIN"),
# }

# # Google Sheets API setup
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, scope)
# client = gspread.authorize(creds)

# # Open Google Sheet safely
# try:
#     spreadsheet = client.open_by_key(SHEET_ID)
#     print("✅ Successfully connected to Google Sheets!")
# except Exception as e:
#     print(f"❌ Google Sheets API Error: {e}")
#     spreadsheet = None  # Avoid crashes if API fails

# app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB limit


# # Route to Fetch Bird Data
# @app.route("/birds", methods=["GET"])
# @cross_origin()
# def get_bird_data():
#     if not spreadsheet:
#         return jsonify({"error": "Unable to connect to Google Sheets"}), 500

#     all_data = {}

#     try:
#         for sheet in spreadsheet.worksheets():
#             records = sheet.get_all_records()

#             # Remove empty values from each record
#             filtered_records = [
#                 {k: v for k, v in record.items() if v != ""}
#                 for record in records
#                 if any(record.values())
#             ]

#             all_data[sheet.title] = filtered_records

#         # Fetch bird names from the first worksheet
#         bird_names = [
#             row.get("bird name", "Unknown bird")
#             for row in spreadsheet.get_worksheet(0).get_all_records()
#         ]
#         print("✅ Bird names fetched:", bird_names)  # Debugging line

#         return jsonify(all_data)

#     except Exception as e:
#         return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500


# # Audio Conversion Route
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


# # Spectrogram Generation Route
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


# # Bird Species Prediction Route (Improved Version)
# @app.route("/predict", methods=["POST"])
# @cross_origin()
# def bird_prediction():
#     try:
#         # Check if audio file is present
#         if "fileInput" not in request.files:
#             return jsonify({"error": "No file received by server"}), 400

#         audio_file = request.files["fileInput"]

#         if audio_file.filename == "":
#             return jsonify({"error": "No file selected"}), 400

#         # Save the audio to a temporary file
#         temp_audio_path = "temp_audio.wav"
#         audio_file.save(temp_audio_path)

#         # ✅ Refetch bird names from Google Sheets on each call
#         # try:
#         #     bird_names_sheet = spreadsheet.get_worksheet(0).get_all_records()
#         #     bird_names = [row.get("bird name", "Unknown bird") for row in bird_names_sheet]
#         #     print("✅ Fresh Bird Names Fetched:", bird_names)  # Debug line to verify refresh
#         # except Exception as e:
#         #     print(f"⚠️ Failed to refresh bird names: {e}")
#         #     bird_names = ["Unknown bird"] * 101  # Fallback to ensure prediction still works

#         try:
#             bird_names = []  # Collect names from all sheets
        
#             for i in range(len(spreadsheet.worksheets())):
#                 sheet_data = spreadsheet.get_worksheet(i).get_all_records()
            
#                 # Extract bird names from each sheet, fallback to "Unknown bird"
#                 bird_names += [row.get("bird name", "Unknown bird") for row in sheet_data]

#             print("✅ Bird Names Fetched from All Sheets:", bird_names)  # Debug line

#         except Exception as e:
#             print(f"⚠️ Failed to fetch bird names: {e}")
#             bird_names = ["Unknown bird"] * 101  # Fallback to ensure prediction still works


#         # 🔥 Call the prediction function
#         prediction_result = predict_bird(temp_audio_path, bird_names)

#         if "error" in prediction_result:
#             return jsonify({"error": prediction_result["error"]}), 500

#         # Return bird species and confidence as JSON
#         return jsonify({
#             "bird_species": prediction_result["bird_species"],
#             "confidence": prediction_result["confidence"]
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

#     finally:
#         # 🧹 Ensure temp file gets removed after processing
#         if os.path.exists("temp_audio.wav"):
#             os.remove("temp_audio.wav")


# if __name__ == "__main__":
#     app.run(debug=True, use_reloader=False)



from flask import Flask, request, send_file, jsonify
from flask_cors import CORS, cross_origin
import os
import gspread
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

# Custom imports
from convert_audio import convert_to_wav
from create_spectogram import generate_spectrogram
from prediction import predict_bird

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
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, scope)
client = gspread.authorize(creds)

# Open Google Sheet safely
try:
    spreadsheet = client.open_by_key(SHEET_ID)
    print("✅ Successfully connected to Google Sheets!")
except Exception as e:
    print(f"❌ Google Sheets API Error: {e}")
    spreadsheet = None  # Avoid crashes if API fails

app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB limit


# Route to Fetch Bird Data (remains unchanged)
@app.route("/birds", methods=["GET"])
@cross_origin()
def get_bird_data():
    if not spreadsheet:
        return jsonify({"error": "Unable to connect to Google Sheets"}), 500

    all_data = {}

    try:
        for sheet in spreadsheet.worksheets():
            records = sheet.get_all_records()

            # Remove empty values from each record, but only if the *entire* record is empty
            filtered_records = [
                {k: v for k, v in record.items() if v != ""}
                for record in records
                if any(record.values())  # Keep record if *any* value is non-empty
            ]

            all_data[sheet.title] = filtered_records

        return jsonify(all_data)

    except Exception as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500



# Audio Conversion Route (remains unchanged)
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


# Spectrogram Generation Route (remains unchanged)
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


# Bird Species Prediction Route
@app.route("/predict", methods=["POST"])
@cross_origin()
def bird_prediction():
    try:
        # Check if audio file is present
        if "fileInput" not in request.files:
            return jsonify({"error": "No file received by server"}), 400

        audio_file = request.files["fileInput"]

        if audio_file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        # Save the audio to a temporary file
        temp_audio_path = "temp_audio.wav"
        audio_file.save(temp_audio_path)

        # ✅ Fetch bird names from ALL worksheets, handling duplicates
        try:
            bird_names_set = set()  # Use a set for uniqueness
            for sheet in spreadsheet.worksheets():
                records = sheet.get_all_records()
                for row in records:
                    name = row.get("bird name", "Unknown bird")
                    if name:  # Add only non-empty names
                        bird_names_set.add(name)
                    else:
                        bird_names_set.add("Unknown bird") # if empty add Unknown bird

            bird_names = list(bird_names_set)  # Convert back to a list

            # Adjust the length to match the model's output (101)
            if len(bird_names) > 101:
                print("⚠️ More than 101 unique bird names. Truncating to 101.")
                bird_names = bird_names[:101]
            elif len(bird_names) < 101:
                print("⚠️ Less than 101 unique bird names. Padding with 'Unknown bird'.")
                bird_names.extend(["Unknown bird"] * (101 - len(bird_names)))

            print("✅ Bird Names Fetched from All Sheets:", bird_names)  # Debug
            print("✅ Number of Bird Names:", len(bird_names))

        except Exception as e:
            print(f"⚠️ Failed to fetch bird names: {e}")
            bird_names = ["Unknown bird"] * 101  # Fallback

        # Call the prediction function
        prediction_result = predict_bird(temp_audio_path, bird_names)

        if "error" in prediction_result:
            return jsonify({"error": prediction_result["error"]}), 500

        # Return bird species and confidence
        return jsonify({
            "bird_species": prediction_result["bird_species"],
            "confidence": prediction_result["confidence"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)