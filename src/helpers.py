import tqdm
from pydub import AudioSegment
from .constants import SummarizerFormat, SummaryLength, SummaryContext


class CustomProgressBar(tqdm.tqdm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current = self.n  
    def update(self, n):
        super().update(n)
        self._current += n
        print("Audio Transcribe Progress: " + str(round(self._current/self.total*100))+ "%")

def convert_to_wav(file):
    audio = AudioSegment.from_file(file)
    audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    output_path = file.name.replace(".mp3", ".wav")
    audio.export(output_path, format="wav")
    return output_path

def summarize_notes(note_text, model, format=SummarizerFormat.PARAGRAPH, length=SummaryLength.SHORT, context=SummaryContext.GENERAL):
    notes_format = f'(1) {format.getPrompt()} (2) {context.getPrompt()} (3) {length.getPrompt()}'
    response = model.generate_content(f"You are a helpful, an intelligent and highly skilled assistant. Your task is to organise and summarize these notes into clear, concise and well-structured format. Ensure to follow the following 3 points when providing a summary. {notes_format} The notes from various sources (might or might not be related) are provided as follows:\n{note_text}")
    return response.text
