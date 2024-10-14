# resumeparser.py
from gemini import GeminiAI

# Initialize GeminiAI model
model_name = "gemini-1.5-flash"
your_ai = GeminiAI(model_name=model_name)

# Function to process the resume and start the AI conversation
def process_resume(resume_context=None):
    """Reformat the resume and initialize the chat with the resume content."""
    if resume_context is None:
        resume_context = []
    your_ai.start_chat(resume_context)
    return "Resume uploaded and chat started. You can now ask questions about the resume."


def query_resume(user_query):
    """Send a user query about the resume to the AI."""
    # Query the AI based on the user's question
    return your_ai.send_message(user_query)
