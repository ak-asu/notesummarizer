# Note Summarizer Application
Summarize notes using gemini. This app summarizes your notes into clear and concise format. You can upload files, enter notes or provide a webpage URL to summarize. You can also generate voiceovers and export your summaries.

## Python Libraries Used

The Note Summarizer application utilizes the following Python libraries:

- `newspaper3k`: Used for extracting and parsing news articles.
- `lxml[html_clean]`: Used for processing and cleaning HTML content.
- `streamlit`: Used for creating the web interface of the application.
- `python-docx`: Used for reading and writing Microsoft Word documents.
- `PyPDF2`: Used for reading and manipulating PDF files.
- `google-generativeai`: Used for integrating with Google's generative AI services.
- `python-dotenv`: Used for loading environment variables from a `.env` file.
- `pytesseract`: Used for Optical Character Recognition (OCR) with Tesseract.
- `vosk`: Used for offline speech recognition.
- `fpdf`: Used for generating PDF documents.
- `pydub`: Used for audio processing and manipulation.
- `pyttsx3`: Used for text-to-speech conversion.
- `googletrans`: Used for translating text between different languages.

## Setup Guide

### 1. Install Tesseract
1. Download the Tesseract installer from the [official repository](https://github.com/tesseract-ocr/tesseract).
2. Run the installer and follow the on-screen instructions to complete the installation.
3. Add the Tesseract installation directory to your system's PATH environment variable:
    - Open the Start Menu and search for "Edit the system environment variables".
    - In the System Properties window, click on the "Environment Variables" button.
    - Under "System variables", find the `Path` variable, select it, and click "Edit".
    - Click "New" and add the path to the Tesseract installation directory (e.g., `C:\Program Files\Tesseract-OCR`).
    - Click "OK" to close all windows.
4. Verify the installation by opening Command Prompt or PowerShell and running:
    ```sh
    tesseract -v
    ```

### 2. Install FFmpeg
1. Download the FFmpeg zip file from the [official website](https://ffmpeg.org/download.html).
2. Extract the contents of the zip file to a directory of your choice (e.g., `C:\ffmpeg`).
3. Add the `bin` directory inside the extracted FFmpeg folder to your system's PATH environment variable:
    - Open the Start Menu and search for "Edit the system environment variables".
    - In the System Properties window, click on the "Environment Variables" button.
    - Under "System variables", find the `Path` variable, select it, and click "Edit".
    - Click "New" and add the path to the `bin` directory inside the extracted FFmpeg folder (e.g., `C:\ffmpeg\bin`).
    - Click "OK" to close all windows.
4. Verify the installation by opening Command Prompt or PowerShell and running:
    ```sh
    ffmpeg -version
    ```

### 3. Create Python Environment and Install Packages
1. Open Command Prompt or PowerShell.
2. Navigate to the project directory.
3. Create a virtual environment:
    ```sh
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```
5. Install the required packages (run as administrator as newspaper3k might cause problems):
    ```sh
    pip install -r requirements.txt
    ```
6. Create a `.env` file in the project directory and add your gemini API key:
    ```sh
    echo API_KEY=your_api_key_here > .env
    ```
    Replace `your_api_key_here` with your actual API key.

### 4. Run the Application
1. Ensure the virtual environment is activated:
    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```
2. Run the Streamlit app:
    ```sh
    streamlit run app.py
    ```
3. Use the files in the [testcontent](http://_vscodecontentref_/0) folder or upload your own files for testing.

### 5. Optional: Running via PowerShell on Windows
1. Open PowerShell as an administrator.
2. Set the execution policy:
    ```sh
    Set-ExecutionPolicy Unrestricted -Scope Process
    ```
3. Activate the virtual environment:
    ```sh
    .\venv\Scripts\activate
    ```
4. Run the Streamlit app:
    ```sh
    streamlit run app.py
    ```