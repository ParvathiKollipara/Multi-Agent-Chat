import google.generativeai as genai
import os

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def respond(user_input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_input)
    return response.text
