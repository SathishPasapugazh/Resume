from flask import Flask, request, render_template, jsonify
from docx import Document
from pypdf import PdfReader
import os
from resumeparser import process_resume, query_resume  # Import functions from resumeparser.py
from gemini import GeminiAI  # Import GeminiAI class

UPLOAD_PATH = r"__DATA__"
app = Flask(__name__)

# Global variable to hold resume content
resume_content = ""
resume_context = []  # List to store resume content and other files

# Initialize GeminiAI model
model_name = "gemini-1.5-flash"
your_ai = GeminiAI(model_name=model_name)


@app.route('/')
def index():
    print("Index route accessed!")
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

    # Add the resume content to the resume context list
    resume_context.append({"role": "user", "parts": resume_content})

    # Process the uploaded resume and start the chat
    response = process_resume(resume_context)
    return jsonify({"response": response})


@app.route("/chat", methods=["POST"])
def chat():
    print("Chat route accessed!")
    global resume_context
    data = request.get_json()
    user_message = data['message']

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
    Please format the following resume content to NC style, Please note there is a section called government experience in NC style. The prpouse of that section is to give the glimpse of the candidate relevent government experience. Candidates full experiance should be listed in the Empolyment History section including government experiance.

    {resume_content}

    NC style:
    <Candidate Name>
    GOVERNMENT EXPERIENCE (Don't add responsibilities here)
    •	Company Name, City, State	Mon (first three alphabets) YYYY – Mon (first three alphabets) YYYY

    CERTIFICATIONS
    •	Certification 1
    •	Certification 2
    Employment History
    Company Name, City, State	Mon (first three alphabets) YYYY – Mon (first three alphabets) YYYY
    Job Title
    Responsibilities:
    •	Sample 1
    •	Sample 2
    Education
    •	Degree – University, City, State, Year
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


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_PATH):
        os.makedirs(UPLOAD_PATH)
    app.run(port=8000, debug=True)  # Start the server on port 8000