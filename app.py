import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
import googletrans
from time import sleep
from random import Random
from io import BytesIO
from src.constants import SummarizerFormat, SummaryContext, SummaryLength, ExportFileFormat
from src.file import export_summary, extract_text, extract_text_from_url
from src.voiceover import Voiceover


load_dotenv()
API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
translator = googletrans.Translator()
voiceover = Voiceover()
rng = Random()


st.set_page_config(page_title="Note Summarizer", page_icon=':spiral_note_pad:', layout="centered")

if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'history' not in st.session_state:
    st.session_state.history = []

def summarize_notes(note_text, format=SummarizerFormat.PARAGRAPH, length=SummaryLength.SHORT, context=SummaryContext.GENERAL):
    notes_format = f'{format.getPrompt()}. {context.getPrompt()}, {length.getPrompt()}'
    response = model.generate_content(f"You are a helpful assistant. Your task is to summarize these notes into clear and concise format. {notes_format}. The notes are: {note_text}")
    return response.text

@st.dialog("Delete summary")
def delete_summary(ind):
    st.write(f"Are you sure you want to delete this summary?")
    if st.button("Confirm"):
        st.session_state.history.pop(ind)
        st.rerun()

st.title("Note Summarizer")
st.write("This app summarizes your notes into clear and concise format. You can upload files, enter notes or provide a webpage URL to summarize. You can also generate voiceovers and export your summaries.")
tab1, tab2 = st.tabs(["Summarization", "History"])
with tab1:
    uploaded_files = st.file_uploader("Upload files", type=["docx", "pdf", "png", "txt", "mp3"], accept_multiple_files=True)
    url_text = st.text_input("Enter a webpage URL to summarize:", "")
    user_text = st.text_area("Enter your notes here:", "")
    col1, col2, col3 = st.columns([4, 1, 1], gap="small")
    with col1:
        st.empty()
    with col2:
        with st.popover("Options", help="Options for summarization"):
            format_selection = st.radio("Choose summary style:", [i.value for i in SummarizerFormat], horizontal=True)
            summary_length = st.radio("Choose summary length:", [i.value for i in SummaryLength], horizontal=True)
            context_selection = st.selectbox("Choose summary context:", [i.value for i in SummaryContext])
    with col3:
        if st.button("Summarize"):
            st.session_state.summary = None
            note_texts = []
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    try:
                        note_texts.append(extract_text(uploaded_file))
                    except Exception as e:
                        print(e)
                        st.toast(f"Error reading {uploaded_file.name}")
            url_webpage_text = extract_text_from_url(url_text) if url_text else None
            note_text = '\n'.join(note_texts + ([user_text] if user_text else []) + ([url_webpage_text] if url_webpage_text else []))
            if note_text:
                with st.spinner(''):
                    st.session_state.summary = summarize_notes(note_text, format=SummarizerFormat(format_selection), length=SummaryLength(summary_length), context=SummaryContext(context_selection))
                    st.session_state.history.append(st.session_state.summary)
            else:
                st.toast("Please provide notes to summarize.")
    st.divider()
    st.subheader("Summary:")
    if st.session_state.summary:
        with st.container(border=True):
            st.write(st.session_state.summary)
        col11, col12, col13 = st.columns([7, 3, 2])
        with col11:
            st.empty()
        with col12:
            selection = st.segmented_control("Download file format", [i.value for i in ExportFileFormat], selection_mode="single", default=ExportFileFormat.TXT.value, key=f"selection")
        with col13:
            st.write('')
            st.download_button(label="Download", use_container_width=True, data=export_summary(st.session_state.summary, ExportFileFormat(selection)), file_name=f"summary_{str(rng.random())[2:]}{ExportFileFormat(selection).get_extension()}", key="download")
    col4, col5, col6 = st.columns([5, 6, 2])
    with col4:
        st.empty()
    with col5:
        target_lang = st.selectbox("Choose a target language:", googletrans.LANGUAGES.values(), placeholder="Choose a language", label_visibility="collapsed")
        voice_option = st.selectbox("Choose a voiceover", voiceover.voices.keys(), placeholder="Choose a voiceover", label_visibility="collapsed")
    with col6:
        if st.button("Translate", disabled=(not st.session_state.summary)):
            st.session_state.summary = translator.translate(st.session_state.summary, dest=target_lang).text
        if st.button("Voiceover", disabled=(not st.session_state.summary)):
            voiceover.output_voiceover(st.session_state.summary, voice_option)
with tab2:
    summaries = st.session_state.history
    for ind, summary in enumerate(summaries):
        with st.container():
            with st.expander(f'{summary[:50]} ...'):
                col21, col22, col23, col24 = st.columns([6, 4, 3, 2])
                with col21:
                    st.empty()
                with col22:
                    selection = st.segmented_control("Download file format", [i.value for i in ExportFileFormat], selection_mode="single", default=ExportFileFormat.TXT.value, label_visibility="collapsed", key=f"selection_{ind}")
                with col23:
                    st.download_button(label="Download", use_container_width=True, data=export_summary(summary, ExportFileFormat(selection)), file_name=f"summary_{str(rng.random())[2:]}{ExportFileFormat(selection).get_extension()}", key=f"download_{ind}")
                with col24:
                    if st.button("Delete", use_container_width=True, key=f"delete_{ind}"):
                        delete_summary(ind)
                st.write(summary)
if st.button("Reset", key="reset_button", use_container_width=True, type="primary"):
    st.cache_data.clear()
    st.session_state.clear() + st.rerun()
st.markdown("""
    <style>
    #reset_button button {
        background-color: red !important;
    }
    </style>
    """, unsafe_allow_html=True)
