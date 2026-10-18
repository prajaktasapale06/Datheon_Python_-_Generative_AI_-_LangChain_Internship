
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, ConfigDict, Field

# Load the API key from the .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "sample_resume.txt"
OUTPUT_FILE = BASE_DIR / "output.json"


# Define the expected JSON structure
class ResumeInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    email: str | None = None
    education: str | None = None
    skills: list[str] = Field(default_factory=list)
    experience_years: float | None = None
    projects: list[str] = Field(default_factory=list)


# Parameterized prompt template with a few-shot example
PROMPT_TEMPLATE = """
You are an information extraction assistant.

Extract information from the supplied resume.

Rules:
1. Extract only facts present in the resume.
2. Never invent missing information.
3. Use null for missing single values.
4. Use an empty list for missing skills or projects.
5. Return a JSON object with exactly these keys:
   name, email, education, skills,
   experience_years, projects.
6. experience_years must be a number or null.

Example:
Input:
Name: Anita
Skills: Python, SQL
Experience: 2 years

Output:
{{"name": "Anita", "email": null,
"education": null, "skills": ["Python", "SQL"],
"experience_years": 2, "projects": []}}

Now extract information from this resume:

{resume_text}
"""


def extract_resume_information(resume_text: str) -> ResumeInfo:
    """Extract resume details using Gemini and validate the result."""

    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    if not api_key:
        raise ValueError(
            "API key not found. Check your .env file."
        )

    client = genai.Client(api_key=api_key)

    prompt = PROMPT_TEMPLATE.format(
        resume_text=resume_text
    )

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    # Parse and validate the response against our schema
    resume = ResumeInfo.model_validate_json(response.text)

    return resume


def main():
    if not INPUT_FILE.exists():
        print(f"Error: Cannot find {INPUT_FILE.name}")
        return

    resume_text = INPUT_FILE.read_text(
        encoding="utf-8"
    ).strip()

    if not resume_text:
        print("Error: The resume file is empty.")
        return

    try:
        print("Extracting resume information...")

        resume = extract_resume_information(resume_text)

        result = resume.model_dump()

        json_output = json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )

        OUTPUT_FILE.write_text(
            json_output,
            encoding="utf-8"
        )

        print("\nValidated JSON output:\n")
        print(json_output)
        print(f"\nOutput saved to: {OUTPUT_FILE.name}")

    except Exception as error:
        print(f"\nError: {error}")
        print(
            "Check your API key, internet connection, "
            "model access, and API quota."
        )


if __name__ == "__main__":
    main()
