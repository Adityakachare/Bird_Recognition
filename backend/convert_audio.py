from pydub import AudioSegment
import io

def convert_to_wav(input_file):
    # Read the file into an AudioSegment object
    audio = AudioSegment.from_file(input_file)

    # Convert and save to an in-memory buffer
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)  # Reset pointer to the beginning

    return wav_io
