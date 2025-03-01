from lccapp import app
from lccapp import db
from flask import redirect, render_template, request, session, url_for, flash
from flask_bcrypt import Bcrypt
import re
import os
import time
from werkzeug.utils import secure_filename
from functools import wraps

# Create an instance of the Bcrypt class for password hashing
flask_bcrypt = Bcrypt(app)

def login_required(f):
    """Decorator to ensure user is logged in before accessing a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/profile')
@login_required
def profile():
    """User Profile page endpoint.

    Shows the user's profile information and allows them to edit it.
    """
    # Retrieve user profile from the database.
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT username, email, first_name, last_name, location, role, profile_image 
            FROM users WHERE user_id = %s
        ''', (session['user_id'],))
        profile = cursor.fetchone()
        
        # Debug output for profile image
        if profile and profile['profile_image']:
            image_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], profile['profile_image'])
            print(f"Profile image from DB: {profile['profile_image']}")
            print(f"Full image path: {image_path}")
            print(f"Image file exists: {os.path.exists(image_path)}")
            print(f"Static URL: {url_for('static', filename='uploads/' + profile['profile_image'])}")

    return render_template('profile.html', profile=profile)

@app.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    """Update user profile details."""
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    location = request.form.get('location')
    
    # Validate email format
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return render_template('profile.html', 
                             profile={'username': session['username'], 
                                     'email': email,
                                     'first_name': first_name,
                                     'last_name': last_name,
                                     'location': location,
                                     'role': session['role']},
                             email_error='Invalid email format')
    
    # Update user profile in database
    with db.get_cursor() as cursor:
        cursor.execute('''
            UPDATE users 
            SET email = %s, first_name = %s, last_name = %s, location = %s
            WHERE user_id = %s
        ''', (email, first_name, last_name, location, session['user_id']))
    
    flash('Profile updated successfully', 'success')
    return redirect(url_for('profile'))

@app.route('/update-profile-image', methods=['POST'])
@login_required
def update_profile_image():
    """Update or remove user profile image."""
    # Check if user wants to remove their profile image
    if 'remove_image' in request.form:
        with db.get_cursor() as cursor:
            # Get current image filename
            cursor.execute('SELECT profile_image FROM users WHERE user_id = %s', (session['user_id'],))
            result = cursor.fetchone()
            current_image = result['profile_image'] if result else None
            
            # Remove file if it exists
            if current_image:
                image_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], current_image)
                try:
                    if os.path.exists(image_path):
                        os.remove(image_path)
                        print(f"Removed image file: {image_path}")
                except Exception as e:
                    print(f"Error removing file: {str(e)}")
            
            # Update database
            cursor.execute('UPDATE users SET profile_image = NULL WHERE user_id = %s', (session['user_id'],))
        
        flash('Profile image removed', 'success')
        return redirect(url_for('profile'))
    
    # Handle file upload
    if 'profile_image' not in request.files:
        flash('No file selected', 'warning')
        return redirect(url_for('profile'))
    
    file = request.files['profile_image']
    if file.filename == '':
        flash('No file selected', 'warning')
        return redirect(url_for('profile'))
    
    if file and allowed_file(file.filename):
        # Generate secure filename
        filename = secure_filename(f"user_{session['user_id']}_{int(time.time())}_{file.filename}")
        
        # Ensure upload directory exists
        upload_dir = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
        os.makedirs(upload_dir, exist_ok=True)
        print(f"Upload directory: {upload_dir}")
        
        # Save file
        file_path = os.path.join(upload_dir, filename)
        try:
            file.save(file_path)
            print(f"Saved file to: {file_path}")
            
            # Check if file was saved successfully
            if not os.path.exists(file_path):
                flash('Error saving image file', 'danger')
                return redirect(url_for('profile'))
                
        except Exception as e:
            print(f"Error saving file: {str(e)}")
            flash('Error saving image file', 'danger')
            return redirect(url_for('profile'))
        
        # Update database with new filename
        with db.get_cursor() as cursor:
            # Get old image if exists
            cursor.execute('SELECT profile_image FROM users WHERE user_id = %s', (session['user_id'],))
            result = cursor.fetchone()
            current_image = result['profile_image'] if result else None
            
            # Remove old file if it exists and is different from the new one
            if current_image:
                old_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], current_image)
                try:
                    if os.path.exists(old_path) and old_path != file_path:
                        os.remove(old_path)
                        print(f"Removed old image file: {old_path}")
                except Exception as e:
                    print(f"Error removing old file: {str(e)}")
            
            # Update with new image - only store the filename, not the full path
            cursor.execute('UPDATE users SET profile_image = %s WHERE user_id = %s', 
                         (filename, session['user_id']))
            print(f"Updated database with new image: {filename}")
        
        flash('Profile image updated', 'success')
    else:
        flash('Invalid file type. Please upload an image file (PNG, JPG, JPEG, GIF).', 'warning')
    
    return redirect(url_for('profile'))

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password."""
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    # Retrieve current user info
    with db.get_cursor() as cursor:
        cursor.execute('SELECT * FROM users WHERE user_id = %s', (session['user_id'],))
        user = cursor.fetchone()
    
    # Check if current password matches
    if not flask_bcrypt.check_password_hash(user['password_hash'], current_password):
        flash('Current password is incorrect', 'danger')
        return redirect(url_for('profile'))
    
    # Check if new password meets requirements
    if len(new_password) < 8:
        flash('New password must be at least 8 characters long', 'danger')
        return redirect(url_for('profile'))
    
    # Check if passwords match
    if new_password != confirm_password:
        flash('New passwords do not match', 'danger')
        return redirect(url_for('profile'))
    
    # Check if new password is different from current
    if current_password == new_password:
        flash('New password must be different from current password', 'danger')
        return redirect(url_for('profile'))
    
    # Hash new password and update
    password_hash = flask_bcrypt.generate_password_hash(new_password)
    with db.get_cursor() as cursor:
        cursor.execute('UPDATE users SET password_hash = %s WHERE user_id = %s', 
                      (password_hash, session['user_id']))
    
    flash('Password changed successfully', 'success')
    return redirect(url_for('profile'))

# Helper function for file uploads
def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']