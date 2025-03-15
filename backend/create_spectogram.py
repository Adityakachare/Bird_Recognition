import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend to prevent threading issues
import numpy as np
import io
import librosa
import librosa.display
import soundfile as sf

def generate_spectrogram(wav_file):
    """
    Generates a spectrogram from a given WAV file and returns it as an in-memory image.
    """
    try:
        # Read the uploaded WAV file into memory
        with io.BytesIO(wav_file.read()) as audio_buffer:
            y, sr = librosa.load(audio_buffer, sr=None)  # Preserve original sample rate
        
        # Check if audio data is valid
        if y is None or len(y) == 0:
            raise ValueError("Invalid or empty audio file.")

        # Generate spectrogram
        fig, ax = plt.subplots(figsize=(10, 4))
        S = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        librosa.display.specshow(S, sr=sr, x_axis="time", y_axis="log", ax=ax)
        ax.set_title("Spectrogram")
        ax.set_xlabel("Time")
        ax.set_ylabel("Frequency")

        # Save the spectrogram to a BytesIO object
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format="png", bbox_inches="tight", pad_inches=0)
        plt.close(fig)

        # Move buffer to start
        img_buffer.seek(0)

        return img_buffer
    except Exception as e:
        raise RuntimeError(f"Error generating spectrogram: {str(e)}")
