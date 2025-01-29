import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
from docx import Document
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import pyttsx3
import threading
from enum import Enum
from time import sleep

class SummarizerFormat(Enum):
	PARAGRAPH = "Paragraph"
	BULLET_POINTS = "Bullet points"
	STUDY_GUIDE = "Study guide"

load_dotenv()
API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
engine = pyttsx3.init()
voices = engine.getProperty('voices')

warn = None

def summarize_note(note_text, format=SummarizerFormat.PARAGRAPH):
	notes_format = ''
	if format == SummarizerFormat.BULLET_POINTS:
		notes_format = "Give the summary in bullet points"
	elif format == SummarizerFormat.PARAGRAPH:
		notes_format = "Give the summary in paragraphs"
	elif format == SummarizerFormat.STUDY_GUIDE:
		notes_format = "Give the summary as a study guide. Create a proper plan, tasks and timeline for the study guide"
	prompt = prompt = f"You are a helpful assistant. Your task is to summarize these notes into clear and concise format. {notes_format}. The notes are: {note_text}"
	response = model.generate_content(prompt)
	return response.text

def extract_text_from_image(image):
	text = pytesseract.image_to_string(Image.open(image))
	return text	

def extract_text_from_docx(file):
	document = Document(file)
	full_text = [paragraph.text for paragraph in document.paragraphs]
	return "\n".join(full_text)

def extract_text_from_pdf(file):
	document = PdfReader(file)
	full_text = [paragraph.extract_text() for paragraph in document.pages]
	return "\n".join(full_text)

def output_voiceover(text, voice_option):
	def run():
		for voice in voices:
			if voice.name == voice_option:
				engine.setProperty('voice', voice.id)
				break
		engine.say(text)
		if engine._inLoop:
			engine.endLoop()
		else:
			engine.runAndWait()
	thread = threading.Thread(target=run)
	thread.start()

st.title("Note Summarizer")
st.write("This app summarizes your notes into clear and concise format.")

uploaded_file = st.file_uploader("Upload a file", type=["docx", "pdf", "png", "txt"])
if uploaded_file:
	if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
		note_text = extract_text_from_docx(uploaded_file)
	elif uploaded_file.type == "application/pdf":
		note_text = extract_text_from_pdf(uploaded_file)
	elif uploaded_file.type == "image/png":
		note_text = extract_text_from_image(uploaded_file)
	elif uploaded_file.type == "text/plain":
		note_text = uploaded_file.getvalue().decode("utf-8")	
	else:
		st.error("Please upload a valid file format.")
		note_text = None
else:
	note_text = st.text_area("Enter your notes here:", "")

format_selection = st.radio("Choose summary style:", [format.value for format in SummarizerFormat], horizontal=True)

if 'summary' not in st.session_state:
    st.session_state.summary = None

if st.button("Summarize"):
	if note_text:
		st.session_state.summary = summarize_note(note_text, format=SummarizerFormat(format_selection))
	else:
		warn = "Please enter your notes to summarize."

if st.session_state.summary:
	st.subheader("Summary")
	st.write(st.session_state.summary)

col1, col2 = st.columns([5, 1])
with col1:
	voice_option = st.selectbox("Choose a voiceover", [voice.name for voice in voices], placeholder="Choose a voiceover", label_visibility="collapsed")
with col2:
	if st.button("Voiceover", disabled=not st.session_state.summary):
		if st.session_state.summary:
			output_voiceover(st.session_state.summary, voice_option)
		else:
			warn = "Please summarize your notes before generating voiceover."

if warn:
	st.warning(warn)

if st.button("Reset"):
    st.session_state.clear() + st.rerun()