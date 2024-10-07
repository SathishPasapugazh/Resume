from google.cloud import aiplatform
from docx import Document
import os

def read_word_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    doc = Document(file_path)
    content = []
    for para in doc.paragraphs:
        content.append(para.text)
    return "\n".join(content)

def generate_text_with_gemini(project_id: str, model_name: str, prompt: str):
    aiplatform.init(project=project_id)

    model = aiplatform.Model(model_name=model_name)  # Use Model instead of VertexAIModel
    response = model.predict(prompt=prompt)

    return response.text

def main():
    file_path = "sample.docx"  # Update with your file path
    content = read_word_file(file_path)
    
    if content:
        project_id = os.getenv("GCP_PROJECT_ID")  # Set your Google Cloud project ID as an environment variable
        model_name = "gemini-pro"  # Or another Gemini model
        prompt = f"Summarize the following content:\n\n{content}"

        generated_summary = generate_text_with_gemini(project_id, model_name, prompt)
        
        if generated_summary:
            print("Summary:")
            print(generated_summary)

if __name__ == "__main__":
    main()
