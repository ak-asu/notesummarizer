# notesummarizer
Summarize notes using gemini
## Setup Instructions for Windows

### 1. Create a Python Virtual Environment
1. Open Command Prompt or PowerShell.
2. Navigate to the project directory.
3. Create a virtual environment:
    ```sh
    python -m venv venv
    ```
4. Activate the virtual environment:
    - Command Prompt:
        ```sh
        venv\Scripts\activate
        ```
    - PowerShell:
        ```sh
        .\venv\Scripts\Activate
        ```

### 2. Install Required Packages
1. Ensure the virtual environment is activated.
2. Install the required packages using the `requirements.txt` file:
    ```sh
    pip install -r requirements.txt
    ```

### 3. Install Tesseract
1. Download the Tesseract installer from [here](https://github.com/UB-Mannheim/tesseract/wiki).
2. Run the installer and follow the installation instructions.
3. Add Tesseract to your system PATH:
    - Open the Start Menu, search for "Environment Variables", and select "Edit the system environment variables".
    - In the System Properties window, click on the "Environment Variables" button.
    - Under "System variables", find the `Path` variable, select it, and click "Edit".
    - Click "New" and add the path to the Tesseract executable (e.g., `C:\Program Files\Tesseract-OCR`).
    - Click "OK" to close all windows.

### 4. Run the Application
1. Ensure the virtual environment is activated.
2. If using PowerShell, set the execution policy when running as administrator:
    ```sh
    Set-ExecutionPolicy Unrestricted -Scope Process
    ```
3. Run the Streamlit app:
    ```sh
    streamlit run app.py
    ```
4. Use the files in `testcontent` folder or upload your own files for testing