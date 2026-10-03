import os
from os import environ
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HOST = environ.get('HOST', '0.0.0.0')
PORT = int(environ.get('PORT', 5000))

MODEL = environ.get('MODEL', "yolov8x-world")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

JOURNAL_FILE = os.path.join(BASE_DIR, "journal.json")
