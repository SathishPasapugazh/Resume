import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

class GeminiAI:
    def __init__(self, model_name):
        self.model_name = model_name
        self.api_key = os.getenv("GOOGLE_API_KEY")

        # Configure the API with the API key
        genai.configure(api_key=self.api_key)

        # Initialize the generative model
        self.model = genai.GenerativeModel(self.model_name)
        self.chat = None  # Chat session will be initialized later

    def start_chat(self, resume_content):
        """Start a conversation with the resume context."""
        # Start the chat with the initial resume content
        self.chat = self.model.start_chat(
            history=[
                {"role": "user", "parts": f"Here is a resume: {resume_content}"},
                {"role": "model", "parts": "Got it! How can I assist with this resume?"}
            ]
        )

    def send_message(self, user_input):
        """Send a message to the AI chat and get a response."""
        if not self.chat:
            return "Chat session has not been started with resume content."

        response = self.chat.send_message(user_input)
        return response.text