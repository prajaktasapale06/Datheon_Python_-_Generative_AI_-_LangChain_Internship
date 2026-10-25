# Task 3: Multi-Tool Autonomous AI Agent

## Overview
A console-based autonomous AI agent built using Python, LangChain, and Groq. The agent selects and uses different tools to answer user queries.

## Features
- **Web Search:** Searches the web using DuckDuckGo.
- **Python Calculator:** Performs mathematical calculations safely.
- **Local File Reader:** Reads information from a local text file.
- **Autonomous Tool Selection:** Chooses tools based on the user's question.
- **Interactive Console:** Accepts multiple questions until the user exits.

## Technology Stack
- Python
- LangChain
- Groq LLM API
- DuckDuckGo Search
- python-dotenv

## Project Structure
```text
Task-3-Multi-Tool-AI-Agent/
├── main.py
├── sample.txt
├── requirements.txt
├── README.md
└── .env
```

The `.env` file contains the API key and must not be committed to GitHub.

## Setup Instructions

1. Clone or download the repository.
2. Navigate to the Task 3 folder.
3. Create and activate a virtual environment.
4. Install dependencies:

   `pip install -r requirements.txt`

5. Create a `.env` file and add:

   `GROQ_API_KEY=your_groq_api_key`

6. Run the application:

   `python main.py`

## Example Queries
- `Calculate 245 * 18`
- `Read sample.txt and tell me the library opening hours.`
- `Search the web for artificial intelligence news.`

## Agent Execution Flow
**User Query → Agent Decision → Tool Execution → Observation → Final Answer**

## Learning Outcomes
- Working with LLMs through Groq
- Creating tools with LangChain
- Implementing tool-calling workflows
- Integrating web search, calculations, and local file access
- Building an interactive Python console application