import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torchvision.models import ConvNeXt_Tiny_Weights
import numpy as np
import cv2
import librosa
import matplotlib.pyplot as plt
import io
from PIL import Image
import os

# Load Model Setup
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model_path = "ConvNeXt-Tiny_bird_classification.pth"

# ✅ Define the model architecture
model = models.convnext_tiny(weights=ConvNeXt_Tiny_Weights.DEFAULT)

num_classes = 101  # Change this to match your number of bird classes
model.classifier[2] = nn.Linear(model.classifier[2].in_features, num_classes)

# ✅ Load the state_dict properly
model.load_state_dict(torch.load(model_path, map_location=DEVICE))
model.to(DEVICE)
model.eval()


# 🎯 Spectrogram Generation Function (Built-in)
def generate_spectrogram(audio_file_path):
    try:
        # Load the audio file
        y, sr = librosa.load(audio_file_path, sr=None)

        # Generate Mel spectrogram
        spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
        spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)

        # Plot spectrogram without axes
        plt.figure(figsize=(10, 4))
        plt.imshow(spectrogram_db, aspect='auto', origin='lower', cmap='viridis')
        plt.axis('off')

        # Save spectrogram to an in-memory file
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format="png", bbox_inches='tight', pad_inches=0)
        plt.close()

        # Reset buffer position
        img_buffer.seek(0)

        # Convert buffer to PIL Image for model prediction
        spectrogram_img = Image.open(img_buffer).convert("RGB")
        return spectrogram_img

    except Exception as e:
        raise ValueError(f"Error generating spectrogram: {e}")


# 🛠️ Image preprocessing function
def preprocess_image(image):
    if isinstance(image, np.ndarray):  # Convert OpenCV image to PIL format
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    return transform(image).unsqueeze(0).to(DEVICE)


# 🚀 Prediction Logic
def predict_bird(audio_file_path, bird_names):
    try:
        # 🔥 Generate spectrogram directly
        spectrogram_img = generate_spectrogram(audio_file_path)

        if spectrogram_img is None:
            return {"error": "Failed to generate spectrogram"}

        # ✅ Preprocess the spectrogram image
        input_tensor = preprocess_image(spectrogram_img)

        # 🔥 Perform prediction
        with torch.no_grad():
            output = model(input_tensor)
            _, predicted_class = torch.max(output, 1)

        # ✅ Handle bird name retrieval safely
        predicted_label = bird_names[predicted_class.item()] if predicted_class.item() < len(bird_names) else "Unknown bird"

        return {"bird_species": predicted_label}

    except Exception as e:
        return {"error": f"Error generating prediction: {str(e)}"}

    finally:
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)
