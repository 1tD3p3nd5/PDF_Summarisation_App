
import os
import openai
from flask import render_template, request, jsonify
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename
from app import flask_app

# Set up the OpenAI API client
openai.api_key = os.environ["OPENAI_API_KEY"]

print(f"OpenAI API Key: {openai.api_key}")

flask_app.config['UPLOAD_FOLDER'] = './uploads'
flask_app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Create the uploads folder if it doesn't exist
uploads_folder = './uploads'
if not os.path.exists(uploads_folder):
    os.makedirs(uploads_folder)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in flask_app.config['ALLOWED_EXTENSIONS']

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        text = ""

        for page in range(num_pages):
            pdf_page = pdf_reader.pages[page]
            text += pdf_page.extract_text()

    return text

def split_text(text, max_length):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(' '.join(current_chunk) + ' ' + word) <= max_length:
            current_chunk.append(word)
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]

    chunks.append(' '.join(current_chunk))
    return chunks

def chat_with_gpt(prompt):
    # Truncate the prompt if it exceeds the token limit
    max_prompt_length = 4000  # Leave some tokens for the completion

    # Split the text into smaller parts
    chunks = split_text(prompt, max_prompt_length)

    summaries = []
    for chunk in chunks:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Please summarize the following text with bullet points:
{chunk}

Summary:",
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )
        summary = response.choices[0].text.strip()
        summary = summary.replace("
", "<br>")  # Replace line breaks with HTML line breaks
        summaries.append(summary)

    return '<br>'.join(summaries)

@flask_app.route("/")
def home():
    return render_template("index.html")

@flask_app.route("/upload", methods=["POST"])
def upload():
    if 'pdf_file' not in request.files:
        return "No file provided", 400

    file = request.files['pdf_file']

    if not allowed_file(file.filename):
        return "File type not allowed", 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(flask_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    text = extract_text_from_pdf(file_path)
    summary = chat_with_gpt(text)

    # Delete the uploaded file after processing
    os.remove(file_path)

    return jsonify({"response": summary})




