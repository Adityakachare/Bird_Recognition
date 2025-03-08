from pydub import AudioSegment
import io

# Ensure correct FFmpeg path
AudioSegment.converter = "C:/ffmpeg-2025-02-20-git-bc1a3bfd2c-essentials_build/bin/ffmpeg.exe"

def convert_to_wav(input_file):
    try:
        # Read the file into an AudioSegment
        audio = AudioSegment.from_file(input_file)

        # Convert and save to an in-memory buffer
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)  # Reset pointer to the beginning

        return wav_io
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        raise e  # Rethrow exception for Flask to catch
