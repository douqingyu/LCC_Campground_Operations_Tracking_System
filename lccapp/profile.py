from lccapp import app
from lccapp import db
from flask import redirect, render_template, request, session, url_for, flash
from flask_bcrypt import Bcrypt
import re
import os
import time
from werkzeug.utils import secure_filename
from functools import wraps

# Bcrypt instance for password hashing
flask_bcrypt = Bcrypt(app)

def login_required(f):
    """Restrict route access to logged-in users only."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/profile')
@login_required
def profile():
    """Display user profile information."""
    # Get user data from database
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT username, email, first_name, last_name, location, role, profile_image 
            FROM users WHERE user_id = %s
        ''', (session['user_id'],))
        profile = cursor.fetchone()
        
        # Log profile image details for debugging
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
    """Save changes to user profile information."""
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
    
    # Save updated profile to database
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
    """Handle profile image upload or removal."""
    # Process image removal request
    if 'remove_image' in request.form:
        with db.get_cursor() as cursor:
            # Get current image filename
            cursor.execute('SELECT profile_image FROM users WHERE user_id = %s', (session['user_id'],))
            result = cursor.fetchone()
            current_image = result['profile_image'] if result else None
            
            # Delete image file if it exists
            if current_image:
                image_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], current_image)
                try:
                    if os.path.exists(image_path):
                        os.remove(image_path)
                        print(f"Removed image file: {image_path}")
                except Exception as e:
                    print(f"Error removing file: {str(e)}")
            
            # Clear image reference in database
            cursor.execute('UPDATE users SET profile_image = NULL WHERE user_id = %s', (session['user_id'],))
        
        flash('Profile image removed', 'success')
        return redirect(url_for('profile'))
    
    # Validate file upload
    if 'profile_image' not in request.files:
        flash('No file selected', 'warning')
        return redirect(url_for('profile'))
    
    file = request.files['profile_image']
    if file.filename == '':
        flash('No file selected', 'warning')
        return redirect(url_for('profile'))
    
    if file and allowed_file(file.filename):
        # Create unique filename
        filename = secure_filename(f"user_{session['user_id']}_{int(time.time())}_{file.filename}")
        
        # Ensure upload directory exists
        upload_dir = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
        os.makedirs(upload_dir, exist_ok=True)
        print(f"Upload directory: {upload_dir}")
        
        # Save uploaded file
        file_path = os.path.join(upload_dir, filename)
        try:
            file.save(file_path)
            print(f"Saved file to: {file_path}")
            
            # Verify file was saved
            if not os.path.exists(file_path):
                flash('Error saving image file', 'danger')
                return redirect(url_for('profile'))
                
        except Exception as e:
            print(f"Error saving file: {str(e)}")
            flash('Error saving image file', 'danger')
            return redirect(url_for('profile'))
        
        # Update database with new image
        with db.get_cursor() as cursor:
            # Get previous image if exists
            cursor.execute('SELECT profile_image FROM users WHERE user_id = %s', (session['user_id'],))
            result = cursor.fetchone()
            current_image = result['profile_image'] if result else None
            
            # Remove previous image file
            if current_image:
                old_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], current_image)
                try:
                    if os.path.exists(old_path) and old_path != file_path:
                        os.remove(old_path)
                        print(f"Removed old image file: {old_path}")
                except Exception as e:
                    print(f"Error removing old file: {str(e)}")
            
            # Update database with new filename
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
    """Update user password with validation checks."""
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    # Get current password hash
    with db.get_cursor() as cursor:
        cursor.execute('SELECT * FROM users WHERE user_id = %s', (session['user_id'],))
        user = cursor.fetchone()
    
    # Validate current password
    if not flask_bcrypt.check_password_hash(user['password_hash'], current_password):
        flash('Current password is incorrect', 'danger')
        return redirect(url_for('profile'))
    
    # Password validation checks
    if len(new_password) < 8:
        flash('New password must be at least 8 characters long', 'danger')
        return redirect(url_for('profile'))
    
    if new_password != confirm_password:
        flash('New passwords do not match', 'danger')
        return redirect(url_for('profile'))
    
    if current_password == new_password:
        flash('New password must be different from current password', 'danger')
        return redirect(url_for('profile'))
    
    # Update password in database
    password_hash = flask_bcrypt.generate_password_hash(new_password)
    with db.get_cursor() as cursor:
        cursor.execute('UPDATE users SET password_hash = %s WHERE user_id = %s', 
                      (password_hash, session['user_id']))
    
    flash('Password changed successfully', 'success')
    return redirect(url_for('profile'))

def allowed_file(filename):
    """Check if uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']