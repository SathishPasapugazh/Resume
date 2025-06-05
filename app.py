from flask import Flask, request, render_template, jsonify, session
import docx2txt
from pypdf import PdfReader
import os
import shutil
import mammoth
from resumeparser import process_resume, query_resume
from prompts import get_short_jd_prompt, get_change_tense_prompt, get_skill_matrix_prompt, get_format_to_nc_prompt, get_analyse_prompt
from gemini import GeminiAI
import json

UPLOAD_PATH = r"__DATA__"
ARCHIVE_PATH = r"archived"
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for using session

# Global variable to hold resume content
resume_content = ""
resume_context = []  # List to store resume content and other files

# Initialize GeminiAI model
#model_name = "gemini-1.5-pro-002"
#your_ai = GeminiAI(model_name=model_name)


@app.route('/')
def index():
    print("Index route accessed!")

    # Move the resume to archived folder if it exists in the session
    if 'resume_file' in session:
        move_resume_to_archived(session['resume_file'])

    # Clear the session to indicate the chat is refreshed
    session.clear()

    return render_template('chat.html')  # The main page for the chatbot

@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    print("Upload Resume route accessed!")
    global resume_content, resume_context
    doc = request.files.get('doc')

    if not doc:
        return jsonify({"response": "No file uploaded!"}), 400

    # Create the upload path if it doesn't exist
    if not os.path.exists(UPLOAD_PATH):
        os.makedirs(UPLOAD_PATH)

    # Create the archive path if it doesn't exist
    if not os.path.exists(ARCHIVE_PATH):
        os.makedirs(ARCHIVE_PATH)

    file_extension = doc.filename.split('.')[-1].lower()
    file_path = os.path.join(UPLOAD_PATH, doc.filename)
    doc.save(file_path)  # Save the uploaded file

    # Store the file path in session
    session['resume_file'] = file_path

    # Handle the file based on its extension
    if file_extension == 'pdf':
        resume_content = _read_pdf_from_path(file_path)
    elif file_extension == 'docx':
        resume_content = docx2txt.process(file_path)
    else:
        return jsonify({"response": "Unsupported file format. Please upload a PDF or DOCX file."}), 400

    # Add the resume content to the resume context list
    resume_context = [{"role": "user", "parts": resume_content}]  # Replace instead of append

    # Process the uploaded resume and start the chat
    response = process_resume(resume_context)
    return jsonify({"response": response})


@app.route("/short_jd", methods=["POST"])
def short_jd():
    print("Short Job Description route accessed!")
    user_message = get_short_jd_prompt()
    response = query_resume(user_message)
    return jsonify({"response": response})


@app.route("/chat", methods=["POST"])
def chat():
    print("Chat route accessed!")
    global resume_context
    data = request.get_json()
    user_message = data['message']

    response = query_resume(user_message)
    return jsonify({"response": response})


@app.route("/change_tense", methods=["POST"])
def change_tense():
    print("Change Past tense route accessed!")
    global resume_context
    user_message = get_change_tense_prompt()
    response = query_resume(user_message)
    return jsonify({"response": response})

@app.route("/analyse", methods=["POST"])
def analyse():
    print("Change analyse route accessed!")
    global resume_context
    user_message = get_analyse_prompt()
    response = query_resume(user_message)
    return jsonify({"response": response})

@app.route("/skill_matrix", methods=["POST"])
def skill_matrix():
    print("Skill Matrix route accessed!")
    global resume_context
    user_message = get_skill_matrix_prompt()
    response = query_resume(user_message)
    return jsonify({"response": response})


@app.route("/format_to_nc", methods=["POST"])
def format_to_nc():
    print("Format to NC route accessed!")
    global resume_content
    if not resume_content:
        return jsonify({"response": "Please upload a resume first."}), 400

    # Check if chat session is initialized
        # Use Gemini AI to format the resume
    user_message = get_format_to_nc_prompt(resume_content)

    response = query_resume(user_message)
    return jsonify({"response": response})  # Return the response


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


# Helper function to move resume to archived folder
def move_resume_to_archived(file_path):
    if os.path.exists(file_path):
        archive_file_path = os.path.join(ARCHIVE_PATH, os.path.basename(file_path))
        shutil.move(file_path, archive_file_path)  # Move file to the archived folder
        print(f"File moved to archived folder: {archive_file_path}")


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_PATH):
        os.makedirs(UPLOAD_PATH)
    if not os.path.exists(ARCHIVE_PATH):
        os.makedirs(ARCHIVE_PATH)
    app.run(port=8000, debug=True)  # Start the server on port 8000
