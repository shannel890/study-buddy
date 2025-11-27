import google.genai as genai
import os
from google.genai import types

# 1. Configure the Gemini API client
# It's best practice to set the key as an environment variable
os.environ["GEMINI_API_KEY"] = "AIzaSyBh5hPZUy8ylQypu7sZRwESPszhBBLDQfo"
client = genai.Client()

def summarize_notes(notes_text: str):
    """Generates a concise summary from a block of text using the Gemini API."""
    
    # 2. Define the Prompt
    # A clear, specific prompt is key to a good summary.
    prompt = f"""
    You are an expert study buddy. Summarize the following study notes. 
    The summary must be 5 concise bullet points covering the key topics and definitions.
    
    --- NOTES ---
    {notes_text}
    ---
    """
    
    # 3. Call the Gemini API
    # Using 'gemini-2.5-flash' for fast and high-quality text tasks.
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"An error occurred during summarization: {e}"

# --- Example Usage ---
example_notes = """
The first law of thermodynamics, also known as the Law of Conservation of Energy, 
states that energy cannot be created or destroyed in an isolated system. It can 
only be converted from one form to another. For example, the chemical energy 
in food is converted into kinetic energy when a person runs. The change in 
internal energy (ΔU) of a system equals the net heat supplied to the system (Q) 
minus the net work done by the system (W). The formula is ΔU = Q - W. This law 
is fundamental to all physical sciences.
"""

summary = summarize_notes(example_notes)
print("🧠 **Generated Summary**")
print(summary)