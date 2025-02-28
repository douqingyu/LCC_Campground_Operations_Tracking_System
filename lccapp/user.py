from lccapp import app
from lccapp import db
from flask import redirect, render_template, request, session, url_for, flash
from flask_bcrypt import Bcrypt
import re
import os
import time
import re
from werkzeug.utils import secure_filename

# Create an instance of the Bcrypt class, which we'll be using to hash user
# passwords during login and registration.
flask_bcrypt = Bcrypt(app)

# Default role assigned to new users upon registration.
DEFAULT_USER_ROLE = 'visitor'

def user_home_url():
    """Generates a URL to the homepage for the currently logged-in user."""
    role = session.get('role', None)

    if role == 'visitor':  
        home_endpoint = 'visitor_home'
    elif role == 'helper':  
        home_endpoint = 'helper_home'
    elif role == 'admin':
        home_endpoint = 'admin_home'
    else:
        home_endpoint = 'login'
    
    return url_for(home_endpoint)

@app.route('/')
def root():
    """Root endpoint (/)
    
    Methods:
    - get: Redirects guests to the login page, and redirects logged-in users to
        their own role-specific homepage.
    """
    return redirect(user_home_url())

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page endpoint.

    Methods:
    - get: Renders the login page.
    - post: Attempts to log the user in using the credentials supplied via the
        login form, and either:
        - Redirects the user to their role-specific homepage (if successful)
        - Renders the login page again with an error message (if unsuccessful).
    
    If the user is already logged in, both get and post requests will redirect
    to their role-specific homepage.
    """
    if 'loggedin' in session:
         return redirect(user_home_url())

    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        # Get the login details submitted by the user.
        username = request.form['username']
        password = request.form['password']

        # Attempt to validate the login details against the database.
        with db.get_cursor() as cursor:
            # Try to retrieve the account details for the specified username.
            #
            # Note: we use a Python multiline string (triple quote) here to
            # make the query more readable in source code. This is just a style
            # choice: the line breaks are ignored by MySQL, and it would be
            # equally valid to put the whole SQL statement on one line like we
            # do at the beginning of the `signup` function.
            cursor.execute('''
                           SELECT user_id, username, password_hash, role
                           FROM users
                           WHERE username = %s;
                           ''', (username,))
            account = cursor.fetchone()
            
            if account is not None:
                # We found a matching account: now we need to check whether the
                # password they supplied matches the hash in our database.
                password_hash = account['password_hash']
                
                if flask_bcrypt.check_password_hash(password_hash, password):
                    # Password is correct. Save the user's ID, username, and role
                    # as session data, which we can access from other routes to
                    # determine who's currently logged in.
                    # 
                    # Users can potentially see and edit these details using their
                    # web browser. However, the session cookie is signed with our
                    # app's secret key. That means if they try to edit the cookie
                    # to impersonate another user, the signature will no longer
                    # match and Flask will know the session data is invalid.
                    session['loggedin'] = True
                    session['user_id'] = account['user_id']
                    session['username'] = account['username']
                    session['role'] = account['role']

                    return redirect(user_home_url())
                else:
                    # Password is incorrect. Re-display the login form, keeping
                    # the username provided by the user so they don't need to
                    # re-enter it. We also set a `password_invalid` flag that
                    # the template uses to display a validation message.
                    return render_template('login.html',
                                           username=username,
                                           password_invalid=True)
            else:
                # We didn't find an account in the database with this username.
                # Re-display the login form, keeping the username so the user
                # can see what they entered (otherwise, they might just keep
                # trying the same thing). We also set a `username_invalid` flag
                # that tells the template to display an appropriate message.
                #
                # Note: In this example app, we tell the user if the user
                # account doesn't exist. Many websites (e.g. Google, Microsoft)
                # do this, but other sites display a single "Invalid username
                # or password" message to prevent an attacker from determining
                # whether a username exists or not. Here, we accept that risk
                # to provide more useful feedback to the user.
                return render_template('login.html', 
                                       username=username,
                                       username_invalid=True)

    # This was a GET request, or an invalid POST (no username and/or password),
    # so we just render the login form with no pre-populated details or flags.
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    """Signup (registration) page endpoint.

    Methods:
    - get: Renders the signup page.
    - post: Attempts to create a new user account using the details supplied
        via the signup form, then renders the signup page again with a welcome
        message (if successful) or one or more error message(s) explaining why
        signup could not be completed.

    If the user is already logged in, both get and post requests will redirect
    to their role-specific homepage.
    """
    if 'loggedin' in session:
         return redirect(user_home_url())
    
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form:
        # Get the details submitted via the form on the signup page, and store
        # the values in temporary local variables for ease of access.
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form.get('confirm_password', '')
        
        # Get the new required fields
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        location = request.form.get('location', '')

        # We start by assuming that everything is okay. If we encounter any
        # errors during validation, we'll store an error message in one or more
        # of these variables so we can pass them through to the template.
        username_error = None
        email_error = None
        password_error = None
        confirm_password_error = None
        first_name_error = None
        last_name_error = None
        location_error = None

        # Check whether there's an account with this username in the database.
        with db.get_cursor() as cursor:
            cursor.execute('SELECT user_id FROM users WHERE username = %s;',
                           (username,))
            account_already_exists = cursor.fetchone() is not None
        
        # Validate the username, ensuring that it's unique (as we just checked
        # above) and meets the naming constraints of our web app.
        if account_already_exists:
            username_error = 'An account already exists with this username.'
        elif len(username) > 20:
            # The user should never see this error during normal conditions,
            # because we set a maximum length of 20 on the input field in the
            # template. However, a user or attacker could easily override that
            # and submit a longer value, so we need to handle that case.
            username_error = 'Your username cannot exceed 20 characters.'
        elif not re.match(r'[A-Za-z0-9]+', username):
            username_error = 'Your username can only contain letters and numbers.'            

        # Validate the new user's email address. Note: The regular expression
        # we use here isn't a perfect check for a valid address, but is
        # sufficient for this example.
        if len(email) > 320:
            # As above, the user should never see this error under normal
            # conditions because we set a maximum input length in the template.
            email_error = 'Your email address cannot exceed 320 characters.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            email_error = 'Invalid email address.'
                
        # Enhanced password validation to check for strength requirements
        if len(password) < 8:
            password_error = 'Password must be at least 8 characters long.'
        elif not re.search(r'[A-Za-z]', password):
            password_error = 'Password must include at least one letter.'
        elif not re.search(r'[0-9]', password):
            password_error = 'Password must include at least one number.'
        elif not re.search(r'[^A-Za-z0-9]', password):
            password_error = 'Password must include at least one symbol.'
        
        # Check that passwords match
        if password != confirm_password:
            confirm_password_error = 'Passwords do not match.'
        
        # Validate required fields
        if not first_name:
            first_name_error = 'First name is required.'
        if not last_name:
            last_name_error = 'Last name is required.'
        if not location:
            location_error = 'Location is required.'
                
        if (username_error or email_error or password_error or confirm_password_error or 
            first_name_error or last_name_error or location_error):
            # One or more errors were encountered, so send the user back to the
            # signup page with their username and email address pre-populated.
            # For security reasons, we never send back the password they chose.
            return render_template('signup.html',
                                   username=username,
                                   email=email,
                                   first_name=first_name,
                                   last_name=last_name,
                                   location=location,
                                   username_error=username_error,
                                   email_error=email_error,
                                   password_error=password_error,
                                   confirm_password_error=confirm_password_error,
                                   first_name_error=first_name_error,
                                   last_name_error=last_name_error,
                                   location_error=location_error)
        else:
            # The new account details are valid. Hash the user's new password
            # and create their account in the database.
            password_hash = flask_bcrypt.generate_password_hash(password)
            
            try:
                with db.get_cursor() as cursor:
                    cursor.execute('''
                                   INSERT INTO users (username, password_hash, email, role, first_name, last_name, location)
                                   VALUES (%s, %s, %s, %s, %s, %s, %s);
                                   ''',
                                   (username, password_hash, email, DEFAULT_USER_ROLE, first_name, last_name, location))
                
                # Return to signup page with successful registration indicator
                return render_template('signup.html', signup_successful=True)
                
            except Exception as e:
                # Handle database errors
                password_error = f'Registration failed: {str(e)}'
                return render_template('signup.html',
                                      username=username,
                                      email=email,
                                      first_name=first_name,
                                      last_name=last_name,
                                      location=location,
                                      password_error=password_error)

    # This was a GET request, or an invalid POST (no username, email, and/or
    # password). Render the signup page with no pre-populated form fields or
    # error messages.
    return render_template('signup.html')

@app.route('/profile')
def profile():
    """User Profile page endpoint.

    Shows the user's profile information and allows them to edit it.
    """
    if 'loggedin' not in session:
         return redirect(url_for('login'))

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
def update_profile():
    """Update user profile details."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
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
def update_profile_image():
    """Update or remove user profile image."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
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
def change_password():
    """Change user password."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
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
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/report', methods=['GET', 'POST'])
def report_issue():
    """Report a new issue.
    
    This endpoint is accessible to all authenticated users regardless of their role.
    All issues must have a brief summary and a longer description.
    Issues always begin in 'new' status.
    """
    if 'loggedin' not in session:
         return redirect(url_for('login'))
         
    if request.method == 'POST':
        summary = request.form.get('summary')
        description = request.form.get('description')
        
        if not summary or not description:
            flash('Please provide both summary and description', 'danger')
            return render_template('report_issue.html')  # Make sure this matches the template name
        
        with db.get_cursor() as cursor:
            cursor.execute('''
                INSERT INTO issues (user_id, summary, description, status, created_at)
                VALUES (%s, %s, %s, 'new', NOW())
            ''', (session['user_id'], summary, description))
        
        flash('Issue reported successfully', 'success')
        
        # Redirect to the appropriate home page based on role
        return redirect(user_home_url())
        
    return render_template('report_issue.html')  # Make sure this matches the template name

@app.route('/resolved-issues')
def resolved_issues():
    """View all resolved issues.
    
    This endpoint is restricted to helper and admin roles.
    """
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    # Only allow helpers and admins to view resolved issues
    if session['role'] not in ['helper', 'admin']:
        flash('Access denied. You do not have permission to view resolved issues.', 'danger')
        return redirect(user_home_url())
    
    with db.get_cursor() as cursor:
        # Get resolved issues
        cursor.execute('''
            SELECT i.*, u.username, u.profile_image,
                  (SELECT COUNT(*) FROM comments WHERE issue_id = i.issue_id) AS comment_count
            FROM issues i
            JOIN users u ON i.user_id = u.user_id
            WHERE i.status = 'resolved'
            ORDER BY i.created_at DESC
        ''')
        resolved_issues = cursor.fetchall()
        
        # Add status colors for easier display
        for issue in resolved_issues:
            issue['status_color'] = {
                'new': 'danger',
                'open': 'primary',
                'stalled': 'warning',
                'resolved': 'success'
            }.get(issue['status'], 'secondary')
    
    return render_template('resolved_issues.html', resolved_issues=resolved_issues)

@app.route('/logout')
def logout():
    """Logout endpoint.

    Methods:
    - get: Logs the current user out (if they were logged in to begin with),
        and redirects them to the login page.
    """
    # Note that nothing actually happens on the server when a user logs out: we
    # just remove the cookie from their web browser. They could technically log
    # back in by manually restoring the cookie we've just deleted. In a high-
    # security web app, you may need additional protections against this (e.g.
    # keeping a record of active sessions on the server side).
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    
    return redirect(url_for('login'))