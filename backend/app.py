from flask import Flask, request, send_file, jsonify
import io
from convert_audio import convert_to_wav
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
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

    # Return the converted file as a download
    return send_file(
        wav_io,
        mimetype="audio/wav",
        as_attachment=True,
        download_name=f"{filename.rsplit('.', 1)[0]}.wav"
    )

if __name__ == "__main__":
    app.run(debug=True)
