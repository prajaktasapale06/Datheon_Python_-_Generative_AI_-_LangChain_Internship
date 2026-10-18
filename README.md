
# Structured LLM Prompt Pipeline & JSON Extractor

## Project Overview

This project extracts structured information from unstructured resume text using Python and Google's Gemini API.

The extracted information is validated using Pydantic and saved as a JSON file.

## Features

- AI-powered resume information extraction
- Parameterized prompt template
- Few-shot prompting
- Structured JSON output
- Pydantic data validation
- Secure API key management using environment variables
- Error handling
- Automatic JSON file generation

## Technologies Used

- Python 3
- Google Gemini API
- Google Gen AI SDK
- Pydantic
- python-dotenv
- JSON

## Extracted Information

The application extracts:
- Name
- Email
- Education
- Skills
- Years of experience
- Projects

## Project Structure

```text
llm-json-extractor/
├── main.py
├── sample_resume.txt
├── requirements.txt
├── README.md
├── .gitignore
└── .env  (not uploaded to GitHub)
```

The application generates `output.json` when it runs.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_REPOSITORY_FOLDER
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the Gemini API

Create a `.env` file in the project folder and add:

```text
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=your_supported_gemini_model
```

Replace the placeholders with your actual API key and an available model ID. Never upload the real API key.

### 5. Run the application

Add resume text to `sample_resume.txt` and run:

```bash
python main.py
```

The extracted information will be displayed in the terminal and saved to `output.json`.

## Validation

Pydantic validates the generated JSON against the defined data model. Extracted information should also be checked against the original resume for accuracy.

## Limitations

- Internet access is required to call the Gemini API.
- API access and usage quotas depend on your account.
- AI-generated results may contain errors.
- The current version extracts resume information using a predefined schema.

## Future Improvements

- Support invoice information extraction
- Add automated unit tests
- Improve retry and error handling
- Add a simple user interface

## Author

Prajakta Sapale
