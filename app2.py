import os
import pytesseract
from PIL import Image
from gtts import gTTS
import streamlit as st
import fitz  # PyMuPDF (for PDFs)
import docx  # for Word files

# Path to tesseract.exe (Update if different)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# App title
st.title("📖 READ4ME - Universal OCR & Text-to-Speech")

# Upload multiple files (any type)
uploaded_files = st.file_uploader(
    "Upload files (Images, PDFs, Word Docs, etc.)",
    type=None,  # allows ANY file type
    accept_multiple_files=True
)

output_folder = "audio_outputs"
os.makedirs(output_folder, exist_ok=True)

def extract_text_from_file(file):
    """Extract text depending on file type"""
    if file.type.startswith("image/"):  # Images
        img = Image.open(file)
        return pytesseract.image_to_string(img), img

    elif file.type == "application/pdf":  # PDFs
        pdf_text = ""
        doc = fitz.open(stream=file.read(), filetype="pdf")
        for page in doc:
            pdf_text += page.get_text("text") + "\n"
        return pdf_text, None

    elif file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                       "application/msword"]:  # Word Docs
        doc = docx.Document(file)
        doc_text = "\n".join([para.text for para in doc.paragraphs])
        return doc_text, None

    else:
        return None, None


if uploaded_files:
    full_text = ""
    for idx, uploaded_file in enumerate(uploaded_files, start=1):
        text, img = extract_text_from_file(uploaded_file)

        if img:  # show only for images
            st.image(img, caption=f"Uploaded Image {idx}", use_column_width=True)

        if text and text.strip():
            st.subheader(f"📄 Extracted Text from File {idx}:")
            st.text_area(f"Text {idx}", text, height=200)

            # Save audio
            audio_path = os.path.join(output_folder, f"output_{idx}.mp3")
            tts = gTTS(text=text, lang="en")
            tts.save(audio_path)

            st.audio(audio_path)

            # Append to combined
            full_text += f"\n\n--- File {idx} ---\n{text}"
        else:
            st.warning(f"⚠️ No text detected in File {idx}")

    # Combined Output
    if full_text.strip():
        st.subheader("📘 Combined Extracted Text")
        st.text_area("All Text", full_text, height=300)

        combined_audio_path = os.path.join(output_folder, "combined_output.mp3")
        tts = gTTS(text=full_text, lang="en")
        tts.save(combined_audio_path)
        st.success("🎧 Combined audio ready!")
        st.audio(combined_audio_path)
