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
from lccapp import (user, visitor, helper, admin,issue)

# 在__init__.py文件中更新配置
import os

# 确保应用的根目录下有static/uploads目录
upload_folder = os.path.join('static', 'uploads')
static_folder = 'static'

# 配置应用
app.static_folder = static_folder
app.config.update(
    UPLOAD_FOLDER=upload_folder,
    ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'gif'}
)

# 创建上传目录（如果不存在）
os.makedirs(os.path.join(app.root_path, upload_folder), exist_ok=True)
print(f"Upload directory: {os.path.join(app.root_path, upload_folder)}")
























































