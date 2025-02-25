# This script runs automatically when our `lccapp` module is first loaded,
# and handles all the setup for our Flask app.
from flask import Flask
from flask_bcrypt import Bcrypt
import os

# Initialize Flask app
app = Flask(__name__)

# Set session key for user login and role tracking
app.secret_key = 'your-secret-key-here'

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Set up database connection
from lccapp import connect
from lccapp import db
db.init_db(app, connect.dbuser, connect.dbpass, connect.dbhost, connect.dbname)

# Import all modules that define our Flask route-handling functions
from lccapp import (user, visitor, helper, admin, comment,issue)

app.config.update(
    UPLOAD_FOLDER=os.path.join('static', 'uploads'),
    ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'gif'}
)