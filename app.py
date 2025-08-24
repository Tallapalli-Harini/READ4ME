import os
import pytesseract
from PIL import Image
from gtts import gTTS
import streamlit as st

# Path to tesseract.exe (Update if different)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# App title
st.title("📖 READ4ME - Image to Speech OCR")

# Upload multiple images
uploaded_files = st.file_uploader("Upload screenshots", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

output_folder = "audio_outputs"
os.makedirs(output_folder, exist_ok=True)

if uploaded_files:
    full_text = ""
    for idx, uploaded_file in enumerate(uploaded_files, start=1):
        # Open image
        img = Image.open(uploaded_file)
        st.image(img, caption=f"Uploaded Image {idx}", use_column_width=True)

        # OCR
        text = pytesseract.image_to_string(img).strip()
        
        if text:
            st.subheader(f"📄 Extracted Text from Image {idx}:")
            st.text_area(f"Text {idx}", text, height=200)

            # Save audio
            audio_path = os.path.join(output_folder, f"output_{idx}.mp3")
            tts = gTTS(text=text, lang="en")
            tts.save(audio_path)

            st.audio(audio_path)

            # Append to combined
            full_text += f"\n\n--- Image {idx} ---\n{text}"
        else:
            st.warning(f"No text detected in Image {idx}")

    # Combined Output
    if full_text.strip():
        st.subheader("📘 Combined Extracted Text")
        st.text_area("All Text", full_text, height=300)

        combined_audio_path = os.path.join(output_folder, "combined_output.mp3")
        tts = gTTS(text=full_text, lang="en")
        tts.save(combined_audio_path)
        st.success("🎧 Combined audio ready!")
        st.audio(combined_audio_path)
