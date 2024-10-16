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

    def start_chat(self, resume_context):
        """Start a conversation with the resume context."""
        # Start the chat with the initial resume content
        self.chat = self.model.start_chat(history=resume_context)

    def send_message(self, user_input):
        """Send a message to the AI chat and get a response."""
        if not self.chat:
            # Create a generic session if no resume content is available
            self.chat = self.model.start_chat(history=[])  # Initialize with an empty history if no resume
        response = self.chat.send_message(user_input)
        print(response)
        return response.text
