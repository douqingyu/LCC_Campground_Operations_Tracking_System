# Main initialization file for the 'lccapp' module
# Automatically executes when imported

from flask import Flask
from flask_bcrypt import Bcrypt
import os

# Create Flask app
app = Flask(__name__)

# Set secret key for sessions
app.secret_key = 'e7a8f52c40b96d7e28c612f8a159dd307f18e90a42c16b87dfc9846a'

# Configure static and upload folders
static_folder = 'static'
upload_folder = os.path.join('static', 'uploads')

# Set app configuration
app.static_folder = static_folder
app.config.update(
    UPLOAD_FOLDER=upload_folder,
    ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'gif'}
)

# Create upload directory if needed
os.makedirs(os.path.join(app.root_path, upload_folder), exist_ok=True)
print(f"Upload directory: {os.path.join(app.root_path, upload_folder)}")

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Set up database
from lccapp import connect
from lccapp import db
db.init_db(app, connect.dbuser, connect.dbpass, connect.dbhost, connect.dbname)

# Import route modules
from lccapp import (user, visitor, helper, admin, issue, profile)























































