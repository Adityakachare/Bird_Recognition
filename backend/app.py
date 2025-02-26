from flask import Flask, request, send_file, jsonify
from flask_cors import CORS  # Import CORS
import io
from convert_audio import convert_to_wav
from werkzeug.utils import secure_filename
from flask_cors import cross_origin
from create_spectogram import generate_spectrogram

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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

    # Return the converted file as a downloadable attachment
    return send_file(
        wav_io,
        mimetype="audio/wav",
        as_attachment=True,
        download_name=f"{filename.rsplit('.', 1)[0]}.wav"  # ✅ Removed `headers` argument
    )

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

    # Return the spectrogram image as a downloadable file
    return send_file(
        spectrogram_img,
        mimetype="image/png",
        as_attachment=True,
        download_name=f"{filename.rsplit('.', 1)[0]}_spectrogram.png"
    )


if __name__ == "__main__":
    app.run(debug=True)
