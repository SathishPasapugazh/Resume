from flask import Flask, request, render_template, jsonify
from docx import Document
from pypdf import PdfReader
import os
from resumeparser import process_resume, query_resume  # Change import here


UPLOAD_PATH = r"__DATA__"
app = Flask(__name__)

# Global variable to hold resume content
resume_content = ""

@app.route('/')
def index():
    return render_template('chat.html')  # The main page for the chatbot

@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    global resume_content
    doc = request.files.get('doc')

    if not doc:
        return jsonify({"response": "No file uploaded!"}), 400

    # Create the upload path if it doesn't exist
    if not os.path.exists(UPLOAD_PATH):
        os.makedirs(UPLOAD_PATH)

    file_extension = doc.filename.split('.')[-1].lower()
    file_path = os.path.join(UPLOAD_PATH, doc.filename)
    doc.save(file_path)  # Save the uploaded file

    # Handle the file based on its extension
    if file_extension == 'pdf':
        resume_content = _read_pdf_from_path(file_path)
    elif file_extension == 'docx':
        resume_content = _read_docx_from_path(file_path)
    else:
        return jsonify({"response": "Unsupported file format. Please upload a PDF or DOCX file."}), 400

    # Process the uploaded resume and start the chat
    response = process_resume(resume_content)
    return jsonify({"response": response})

@app.route("/chat", methods=["POST"])
def chat():
    """Handles user messages and sends them to the Gemini AI."""
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"response": "Please provide a message."}), 400

    response = query_resume(user_message)  # Send user's message to the AI
    return jsonify({"response": response})

# Helper function to read PDF files
def _read_pdf_from_path(path):
    reader = PdfReader(path)
    data = ""
    for page in reader.pages:
        data += page.extract_text()
    return data

# Helper function to read DOCX files
def _read_docx_from_path(path):
    try:
        doc = Document(path)
        data = "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip() != ""])
        if not data:
            return "No readable content found in the DOCX file."
        return data
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
        return "Error reading DOCX file."

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_PATH):
        os.makedirs(UPLOAD_PATH)
    app.run(port=8000, debug=True)