from enum import Enum


class SummarizerFormat(Enum):
    PARAGRAPH = "Paragraph"
    BULLET_POINTS = "Bullet points"
    STUDY_GUIDE = "Study guide"

    def getPrompt(self):
        if self == SummarizerFormat.PARAGRAPH:
            return "Summarize the text in paragraph format."
        elif self == SummarizerFormat.BULLET_POINTS:
            return "Summarize the text in bullet points."
        elif self == SummarizerFormat.STUDY_GUIDE:
            return "Summarize the text in a study guide format."

class SummaryContext(Enum):
    GENERAL = "General"
    ACADEMIC = "Academic"
    BUSINESS = "Business"
    CASUAL = "Casual"

    def getPrompt(self):
        if self == SummaryContext.GENERAL:
            return "Summarize with a general tone."
        elif self == SummaryContext.ACADEMIC:
            return "Summarize with an academic tone."
        elif self == SummaryContext.BUSINESS:
            return "Summarize with a business tone."
        elif self == SummaryContext.CASUAL:
            return "Summarize with a casual tone."

class SummaryLength(Enum):
    SHORT = "Short"
    MEDIUM = "Medium"
    LONG = "Long"

    def getPrompt(self):
        if self == SummaryLength.SHORT:
            return "Summarize the text in a short length."
        elif self == SummaryLength.MEDIUM:
            return "Summarize the text in a medium length."
        elif self == SummaryLength.LONG:
            return "Summarize the text in a long length."

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
