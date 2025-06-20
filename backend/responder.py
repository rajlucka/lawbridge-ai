import os
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai  # ✅ Correct import for latest google-genai

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Missing GEMINI_API_KEY in .env file.")

# ✅ Create client with API key (NEW API)
client = genai.Client(api_key=api_key)

# ✅ Load template based on role
def load_prompt_template(role):
    try:
        with open(Path("prompts/role_templates.json"), "r") as f:
            templates = json.load(f)
        return templates.get(role, templates.get("Client", "You are a helpful legal assistant."))
    except FileNotFoundError:
        print("Warning: role_templates.json not found. Using default template.")
        return "You are a helpful legal assistant. Based on this clause: {clause}\n\nAnswer this question: {query}"

# ✅ Format prompt
def format_prompt(clause, query, role):
    template = load_prompt_template(role)
    return template.format(clause=clause, query=query)

# ✅ Generate content using the new API
def generate_answer(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",  # Use latest model
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't generate a response. Please try again."

# ✅ Alternative with streaming (optional)
def generate_answer_stream(prompt):
    try:
        response_chunks = []
        for chunk in client.models.generate_content_stream(
            model="gemini-2.0-flash-001",
            contents=prompt
        ):
            if chunk.text:
                response_chunks.append(chunk.text)
        return "".join(response_chunks).strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't generate a response. Please try again."