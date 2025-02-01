import os
import sys
import streamlit as st
from docx import Document
from PyPDF2 import PdfReader, PdfWriter
from fpdf import FPDF
from PIL import Image
import pytesseract
import tempfile
import whisper
from newspaper import Article
from io import BytesIO
from .constants import ExportFileFormat
from .helpers import CustomProgressBar


def _extract_text_from_docx(file):
    document = Document(file)
    full_text = [paragraph.text for paragraph in document.paragraphs]
    return "\n".join(full_text)

def _extract_text_from_pdf(file):
    document = PdfReader(file)
    full_text = [paragraph.extract_text() for paragraph in document.pages]
    return "\n".join(full_text)

def _extract_text_from_txt(file):
    return file.getvalue().decode("utf-8")

def _extract_text_from_image(file):
    image = Image.open(file)
    return pytesseract.image_to_string(image)

def _extract_text_from_audio(file):
    temp_dir = os.path.join(os.getcwd(), "temp_files")
    os.makedirs(temp_dir, exist_ok=True)
    temp_audio_fd, temp_audio_path = tempfile.mkstemp(suffix=".mp3", dir=temp_dir)
    with os.fdopen(temp_audio_fd, 'wb') as temp_audio:
        temp_audio.write(file.read())
    model = whisper.load_model("small")
    result = model.transcribe(temp_audio_path, verbose=None, fp16=False)
    os.remove(temp_audio_path)
    return result["text"]

def extract_text(file):
    if file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return _extract_text_from_docx(file)
    elif file.type == "application/pdf":
        return _extract_text_from_pdf(file)
    elif file.type == "image/png":
        return _extract_text_from_image(file)
    elif file.type == "text/plain":
        return _extract_text_from_txt(file)
    elif file.type == "audio/mpeg":
        return _extract_text_from_audio(file)
    else:
        raise ValueError("Please upload a valid file format.")

@st.cache_data
def extract_text_from_url(file):
    article = Article(file)
    article.download()
    article.parse()
    return article.text

def export_summary(summary, file_format):
    if file_format == ExportFileFormat.PDF:
        writer = PdfWriter()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        max_chars_per_page = 2000
        summary_parts = [summary[i:i + max_chars_per_page] for i in range(0, len(summary), max_chars_per_page)]
        for i, part in enumerate(summary_parts):
            if i > 0:
                pdf.add_page()
            pdf.multi_cell(0, 10, part)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf_file:
            pdf.output(temp_pdf_file.name)
            temp_pdf_file.close()
            reader = PdfReader(temp_pdf_file.name)
            for page in reader.pages:
                writer.add_page(page)
            buffer = BytesIO()
            writer.write(buffer)
            buffer.seek(0)
            return buffer
    elif file_format == ExportFileFormat.DOCX:
        doc = Document()
        doc.add_paragraph(summary)
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer
    elif file_format == ExportFileFormat.TXT:
        return summary.encode("utf-8")
    else:
        raise ValueError("Invalid file format.")