
from app import flask_app

if __name__ == "__main__":
    flask_app.run(debug=True, port=5001)

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'uploads')
    ALLOWED_EXTENSIONS = {'pdf'}

