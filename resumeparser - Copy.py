from gemini import GeminiAI

# Initialize GeminiAI model
model_name = "gemini-1.5-flash"
your_ai = GeminiAI(model_name=model_name)


# Function to process the resume and start the AI conversation
def process_resume(resume_content):
    """Reformat the resume and initialize the chat with the resume content."""
    # Reformat the resume content and start the AI conversation
    input_text = f"Reformat the following resume: {resume_content}"

    # Start the AI chat with the resume content
    your_ai.start_chat(resume_content)
    return "Resume uploaded and chat started. You can now ask questions about the resume."


def query_resume(user_query):
    """Send a user query about the resume to the AI."""
    # Query the AI based on the user's question
    return your_ai.send_message(user_query)