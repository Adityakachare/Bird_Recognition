# import torch
# import torch.nn as nn
# import torchvision.models as models
# import torchvision.transforms as transforms
# from torchvision.models import ConvNeXt_Tiny_Weights
# import numpy as np
# import cv2
# import librosa
# import matplotlib.pyplot as plt
# import io
# from PIL import Image
# import os
# import matplotlib
# matplotlib.use('Agg')  # Use non-GUI backend to prevent threading issues

# # ✅ Setup: Device selection & model path
# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# model_path = "ConvNeXt-Tiny_bird_classification.pth"
# num_classes = 101

# # 🛠️ Load Model Once (Improved Memory Management)
# if not hasattr(torch, 'bird_model'):
#     model = models.convnext_tiny(weights=ConvNeXt_Tiny_Weights.DEFAULT)
#     model.classifier[2] = nn.Linear(model.classifier[2].in_features, num_classes)
#     model.load_state_dict(torch.load(model_path, map_location=DEVICE))
#     model.to(DEVICE)
#     model.eval()
#     torch.bird_model = model  # Cache model globally

#     print(model.classifier[2])
#     missing_keys, unexpected_keys = model.load_state_dict(
#     torch.load(model_path, map_location=DEVICE), strict=False)
#     print("Missing keys:", missing_keys)
#     print("Unexpected keys:", unexpected_keys)


# else:
#     model = torch.bird_model

# # 🎯 Spectrogram Generation Function 
# # def generate_spectrogram(audio_file_path):
# #     try:
# #         with open(audio_file_path, 'rb') as audio_buffer:
# #             y, sr = librosa.load(audio_buffer, sr=None)

# #         if y is None or len(y) == 0:
# #             raise ValueError("Invalid or empty audio file.")

# #         # Generate Mel spectrogram and convert to dB scale
# #         spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
# #         spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)

# #         # Create the plot with an accurate "coolwarm" color map
# #         fig, ax = plt.subplots(figsize=(10, 4))
# #         img = librosa.display.specshow(spectrogram_db, sr=sr, x_axis='time', y_axis='mel', cmap='coolwarm', ax=ax)
        
# #         # Improved axis labels and color bar styling
# #         ax.set_title("Spectrogram")
# #         ax.set_xlabel("Time")
# #         ax.set_ylabel("Hz")
        
# #         plt.colorbar(img, ax=ax, format='%+2.0f dB')
# #         # cbar.set_label('Intensity (dB)')

# #         # Ensure the color bar ranges correctly from min to max dB
# #         img.set_clim(vmin=np.min(spectrogram_db), vmax=np.max(spectrogram_db))

# #         # Save spectrogram to memory buffer
# #         img_buffer = io.BytesIO()
# #         plt.savefig(img_buffer, format="png", bbox_inches="tight", pad_inches=0)
# #         plt.close(fig)

# #         img_buffer.seek(0)
# #         return Image.open(img_buffer).convert("RGB")

# #     except Exception as e:
# #         raise ValueError(f"Error generating spectrogram: {e}")


# # 🎯 High-Quality Spectrogram Generation (Same Dimensions)
# def generate_spectrogram(audio_file_path):
#     try:
#         with open(audio_file_path, 'rb') as audio_buffer:
#             y, sr = librosa.load(audio_buffer, sr=None)

#         if y is None or len(y) == 0:
#             raise ValueError("Invalid or empty audio file.")

#         # Generate Mel spectrogram and convert to dB scale
#         spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
#         spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)

#         # 📌 Keep dimensions, but enhance quality
#         fig, ax = plt.subplots(figsize=(10, 4), dpi=300)  # Higher DPI for sharper output
#         img = librosa.display.specshow(spectrogram_db, sr=sr, x_axis='time', y_axis='mel', cmap='coolwarm', ax=ax)

#         # ✅ Maintain existing styling
#         ax.set_title("Spectrogram")
#         ax.set_xlabel("Time")
#         ax.set_ylabel("Hz")
#         plt.colorbar(img, ax=ax, format='%+2.0f dB')

#         # 🎯 Ensure color scaling is accurate
#         img.set_clim(vmin=np.min(spectrogram_db), vmax=np.max(spectrogram_db))

#         # Save spectrogram to memory buffer
#         img_buffer = io.BytesIO()
#         plt.savefig(img_buffer, format="png", bbox_inches="tight", pad_inches=0, dpi=300)
#         plt.close(fig)

#         img_buffer.seek(0)
#         return Image.open(img_buffer).convert("RGB")

#     except Exception as e:
#         raise ValueError(f"Error generating high-quality spectrogram: {e}")


# # 🔥 Improved Image Preprocessing Function
# def preprocess_image(image):
#     if isinstance(image, np.ndarray):
#         image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

#     transform = transforms.Compose([
#         transforms.Resize((224, 224)),
#         transforms.ToTensor(),
#         transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
#     ])
#     return transform(image).unsqueeze(0).to(DEVICE)


# # 🚀 Enhanced Prediction Function with Auto-Alignment for Bird Names List
# def predict_bird(audio_file_path, bird_names):
#     try:
#         # 🎧 Generate spectrogram from audio
#         spectrogram_img = generate_spectrogram(audio_file_path)
#         if spectrogram_img is None:
#             return {"error": "Failed to generate spectrogram"}

#         spectrogram_img.show()
#         # 🛠️ Preprocess the spectrogram
#         input_tensor = preprocess_image(spectrogram_img)
#         print("🛠️ Preprocessed Tensor Shape:", input_tensor.shape)

#         # ✅ Ensure model is in evaluation mode
#         model.eval()

#         # 🔥 Log model structure and weights (optional — useful for debugging)
#         print("📥 Loaded Model Parameters:", model.state_dict().keys())

#         # 🚀 Run the model prediction
#         with torch.no_grad():
#             output = model(input_tensor)
#             probabilities = torch.nn.functional.softmax(output, dim=1)
#             confidence, predicted_class = torch.max(probabilities, 1)

#             # 🧠 Debug model output details
#             print("🔢 Raw Model Output:", output)
#             print("📊 Probabilities:", probabilities)
#             print("🔥 Predicted Class Index:", predicted_class.item())
#             print("🎯 Confidence:", confidence.item())

#         # 🛠️ Handle bird names mismatch with model output classes
#         if len(bird_names) != output.shape[1]:
#             print("⚠️ Bird names list length doesn't match model output classes!")
#             print("🔍 Number of bird names:", len(bird_names))
#             print("🔍 Model output classes:", output.shape[1])

#             # ✅ Auto-fix: Adjust bird names list length to match model classes
#             if len(bird_names) > output.shape[1]:
#                 bird_names = bird_names[: output.shape[1]]
#                 print("✂️ Trimmed bird names list to match model classes!")
#             else:
#                 bird_names += ["Unknown bird"] * (output.shape[1] - len(bird_names))
#                 print("➕ Padded bird names list to match model classes!")

#             print("🔧 Adjusted Bird Names Length:", len(bird_names))

#         # 🎯 Bird name retrieval with confidence check
#         if confidence.item() < 0.5:
#             predicted_label = "Uncertain bird species — try a clearer recording!"
#         else:
#             predicted_label = bird_names[predicted_class.item()] if predicted_class.item() < len(bird_names) else "Unknown bird"

#         # ✅ Return the final prediction and confidence percentage
#         return {"bird_species": predicted_label, "confidence": f"{confidence.item() * 100:.2f}%"}

#     except Exception as e:
#         # ❗ Handle errors gracefully
#         return {"error": f"Error generating prediction: {str(e)}"}

#     finally:
#         # 🧹 Ensure temporary audio file gets deleted
#         if os.path.exists(audio_file_path):
#             os.remove(audio_file_path)


# prediction.py
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
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend

# ✅ Setup: Device selection & model path
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model_path = "ConvNeXt-Tiny_bird_classification.pth"
num_classes = 101

# Load Model (Correct and Efficient)
if not hasattr(torch, 'bird_model'):
    model = models.convnext_tiny(weights=ConvNeXt_Tiny_Weights.DEFAULT)
    model.classifier[2] = nn.Linear(model.classifier[2].in_features, num_classes)
    model.load_state_dict(torch.load(model_path, map_location=DEVICE))
    model.to(DEVICE)
    model.eval()
    torch.bird_model = model  # Cache

    print(model.classifier[2])  # Good practice
    # No need for strict=False check *after* successful load.
else:
    model = torch.bird_model



# 🎯 High-Quality Spectrogram Generation (Same Dimensions)
def generate_spectrogram(audio_file_path):
    try:
        with open(audio_file_path, 'rb') as audio_buffer:
            y, sr = librosa.load(audio_buffer, sr=None)

        if y is None or len(y) == 0:
            raise ValueError("Invalid or empty audio file.")

        # Generate Mel spectrogram and convert to dB scale
        spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
        spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)

        # 📌 Keep dimensions, but enhance quality
        fig, ax = plt.subplots(figsize=(10, 4), dpi=300)  # Higher DPI
        img = librosa.display.specshow(spectrogram_db, sr=sr, x_axis='time', y_axis='mel', cmap='coolwarm', ax=ax)

        # ✅ Maintain existing styling
        ax.set_title("Spectrogram")
        ax.set_xlabel("Time")
        ax.set_ylabel("Hz")
        plt.colorbar(img, ax=ax, format='%+2.0f dB')

        # 🎯 Ensure color scaling is accurate
        img.set_clim(vmin=np.min(spectrogram_db), vmax=np.max(spectrogram_db))

        # Save spectrogram to memory buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format="png", bbox_inches="tight", pad_inches=0, dpi=300)
        plt.close(fig)

        img_buffer.seek(0)
        return Image.open(img_buffer).convert("RGB")

    except Exception as e:
        raise ValueError(f"Error generating high-quality spectrogram: {e}")



# 🔥 Improved Image Preprocessing Function
def preprocess_image(image):
    if isinstance(image, np.ndarray):
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    transformed_image = transform(image)
    print("Shape before unsqueeze:", transformed_image.shape)  # Debug
    return transformed_image.unsqueeze(0).to(DEVICE)


# 🚀 Prediction Function
def predict_bird(audio_file_path, bird_names):
    try:
        spectrogram_img = generate_spectrogram(audio_file_path)
        if spectrogram_img is None:
            return {"error": "Failed to generate spectrogram"}

        spectrogram_img.show()

        input_tensor = preprocess_image(spectrogram_img)
        print("Preprocessed Tensor Shape:", input_tensor.shape)

        model.eval()  # Ensure eval mode
        print("Model in eval mode:", model.training)

        with torch.no_grad():
            print("Model device:", next(model.parameters()).device)
            print("Input tensor device:", input_tensor.device)
            output = model(input_tensor)
            probabilities = torch.nn.functional.softmax(output, dim=1)
            confidence, predicted_class = torch.max(probabilities, 1)

            print("Raw Model Output:", output)
            print("Probabilities:", probabilities)
            print("Predicted Class Index:", predicted_class.item())
            print("Confidence:", confidence.item())


        # ✅ NO TRIMMING NEEDED.  We assume bird_names is ALREADY the correct 101.
        if len(bird_names) != num_classes:
            print("Mismatch between bird names length and number of classes.")


        if confidence.item() < 0.5:
            predicted_label = "Uncertain bird species"
        else:
             # Correctly handle potential index out of bounds
            predicted_label = bird_names[predicted_class.item()] if predicted_class.item() < len(bird_names) else "Unknown Bird"


        return {"bird_species": predicted_label, "confidence": f"{confidence.item() * 100:.2f}%"}

    except Exception as e:
        return {"error": f"Prediction error: {str(e)}"}

    finally:
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)