from enum import Enum


MAX_FILES = 5
MAX_FILE_SIZE_MB = 16
MAX_NOTE_LENGTH = 16000

class SummarizerFormat(Enum):
    PARAGRAPH = "Paragraph"
    BULLET_POINTS = "Bullet points"
    STUDY_GUIDE = "Study guide"

    def getPrompt(self):
        if self == SummarizerFormat.PARAGRAPH:
            return "Summarize the text in paragraphs."
        elif self == SummarizerFormat.BULLET_POINTS:
            return "Summarize the text in bullet points."
        elif self == SummarizerFormat.STUDY_GUIDE:
            return "Summarize the text in a study guide format, providing a plan to cover the topics."

class SummaryContext(Enum):
    GENERAL = "General"
    ACADEMIC = "Academic"
    BUSINESS = "Business"
    CASUAL = "Casual"

    def getPrompt(self):
        return f"Adapt the tone and style to be {self.value.lower()}."

class SummaryLength(Enum):
    SHORT = "Short"
    MEDIUM = "Medium"
    LONG = "Long"

    def getPrompt(self):
        return f"Use a {self.value.lower()} level of detail, balancing conciseness with comprehensiveness."

class ExportFileFormat(Enum):
    DOCX = "docx"
    PDF = "pdf"
    TXT = "txt"

    def get_extension(self):
        if self == ExportFileFormat.DOCX:
            return ".docx"
        elif self == ExportFileFormat.PDF:
            return ".pdf"
        elif self == ExportFileFormat.TXT:
            return ".txt"
