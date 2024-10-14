from flask import Flask, request, render_template, jsonify, session
from docx import Document
from pypdf import PdfReader
import os
import shutil
import mammoth  # Add this for .doc file support
from resumeparser import process_resume, query_resume  # Import functions from resumeparser.py
from gemini import GeminiAI  # Import GeminiAI class

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
        resume_content = _read_docx_from_path(file_path)
    elif file_extension == 'doc':
        resume_content = _read_doc_from_path(file_path)  # Handle .doc file using mammoth
    else:
        return jsonify({"response": "Unsupported file format. Please upload a PDF, DOC, or DOCX file."}), 400

    # Add the resume content to the resume context list
    resume_context = [{"role": "user", "parts": resume_content}]  # Replace instead of append

    # Process the uploaded resume and start the chat
    response = process_resume(resume_context)
    return jsonify({"response": response})


@app.route("/short_jd", methods=["POST"])
def short_jd():
    print("Short Job Description route accessed!")
    user_message = f"""
    A job description will be given in the next prompt. Shorten it as much as possible. Reduce the responsibilities. Keep required, desired, preferred skills and certifications."""
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
    user_message = "Convert all listed responsibilities to past tense. Do not make any other changes."
    response = query_resume(user_message)
    return jsonify({"response": response})

@app.route("/skill_matrix", methods=["POST"])
def skill_matrix():
    print("Skill Matrix route accessed!")
    global resume_context
    user_message = f"""
A list of skills will be provided in the next prompt. Calculate the candidate's years of experience for each skill based solely on the resume. If the candidate has no experience with a skill, indicate 'NA'. Give only years don't give explanations.
"""
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
    user_message = f"""
    Please format the following resume content to NC style, while formatting follow the rules below:
     1. The Government Experience section aims to glimpse the candidate's relevant government experience.
     2. In the Employment History section, candidates' full experience should be listed in descending chronological order. Including government experience.
     3. You can rearrange the resume but do not add, remove, or modify any text content. Don't try to correct grammar errors, even if you find any.
     4. Give space before each employment.
     5. Don't remove any text content from employment history. if it doesn't fit the template leave it as it is.
     6. Always read these instructions carefully.

    {resume_content}

    NC style:
    <Candidate Name>
    GOVERNMENT EXPERIENCE (Don't add responsibilities here)
    •	Company Name, City, State	Mon(first three alphabets) YYYY – Mon(first three alphabets) YYYY

    CERTIFICATIONS
    •	Certification 1
    •	Certification 2
    
    Employment History
    Company Name, City, State	Mon (first three alphabets) YYYY – Mon (first three alphabets) YYYY
    Job Title
    Project Description:(if any)
    •	Sample 1
    Responsibilities:
    •	Sample 1
    •	Sample 2
    
    Education
    •	Degree – University, City, State, Passed out year
    """

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


# Helper function to read DOC files using mammoth
def _read_doc_from_path(path):
    try:
        with open(path, "rb") as doc_file:
            result = mammoth.convert_to_text(doc_file)  # Converts DOC to plain text
            return result.value  # Return the extracted text
    except Exception as e:
        print(f"Error reading DOC file: {e}")
        return "Error reading DOC file."


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
