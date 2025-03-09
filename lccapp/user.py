from lccapp import app
from lccapp import db
from flask import redirect, render_template, request, session, url_for, flash
from flask_bcrypt import Bcrypt
import re

# Bcrypt for password hashing
flask_bcrypt = Bcrypt(app)

# Default role for new users
DEFAULT_USER_ROLE = 'visitor'
DEFAULT_USER_STATUS = 'active'

def user_home_url():
    """Return appropriate homepage URL based on user role."""
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
    """Redirect to role-appropriate homepage or login."""
    return redirect(user_home_url())

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user authentication and login."""
    if 'loggedin' in session:
         return redirect(user_home_url())

    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        # Get login info
        username = request.form['username']
        password = request.form['password']

        # Validate info against database
        with db.get_cursor() as cursor:
            # Find account with matching username
            cursor.execute('''
                           SELECT user_id, username, password_hash, role, status
                           FROM users
                           WHERE username = %s;
                           ''', (username,))
            account = cursor.fetchone()
            
            if account is not None:
                # Check if account is inactive
                if account['status'] == 'inactive':
                    # Temporarily set user data in session to show appropriate access denied page
                    session['temp_username'] = account['username']
                    return render_template('access_denied.html', inactive=True), 403
                
                # Verify password against stored hash
                password_hash = account['password_hash']
                
                if flask_bcrypt.check_password_hash(password_hash, password):
                    # Set session data on successful login
                    session['loggedin'] = True
                    session['user_id'] = account['user_id']
                    session['username'] = account['username']
                    session['role'] = account['role']

                    return redirect(user_home_url())
                else:
                    # Password incorrect - redisplay form
                    return render_template('login.html',
                                           username=username,
                                           password_invalid=True)
            else:
                # Username not found - redisplay form
                return render_template('login.html', 
                                       username=username,
                                       username_invalid=True)

    # Initial GET request or invalid POST
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    """Handle new user registration."""
    if 'loggedin' in session:
         return redirect(user_home_url())
    
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form:
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form.get('confirm_password', '')
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        location = request.form.get('location', '')

        # Initialize validation error trackers
        username_error = None
        email_error = None
        password_error = None
        confirm_password_error = None
        first_name_error = None
        last_name_error = None
        location_error = None

        # Check if username already exists
        with db.get_cursor() as cursor:
            cursor.execute('SELECT user_id FROM users WHERE username = %s;',
                           (username,))
            account_already_exists = cursor.fetchone() is not None
        
        # Username validation
        if account_already_exists:
            username_error = 'An account already exists with this username.'
        elif len(username) > 20:
            username_error = 'Your username cannot exceed 20 characters.'
        elif not re.match(r'[A-Za-z0-9]+', username):
            username_error = 'Your username can only contain letters and numbers.'            

        # Email validation
        if len(email) > 320:
            email_error = 'Your email address cannot exceed 320 characters.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            email_error = 'Invalid email address.'
                
        # Password strength validation
        if len(password) < 8:
            password_error = 'Password must be at least 8 characters long.'
        elif not re.search(r'[A-Za-z]', password):
            password_error = 'Password must include at least one letter.'
        elif not re.search(r'[0-9]', password):
            password_error = 'Password must include at least one number.'
        elif not re.search(r'[^A-Za-z0-9]', password):
            password_error = 'Password must include at least one symbol.'
        
        # Password match validation
        if password != confirm_password:
            confirm_password_error = 'Passwords do not match.'
        
        # Required field validation
        if not first_name:
            first_name_error = 'First name is required.'
        if not last_name:
            last_name_error = 'Last name is required.'
        if not location:
            location_error = 'Location is required.'
                
        if (username_error or email_error or password_error or confirm_password_error or 
            first_name_error or last_name_error or location_error):
            # Return form with validation errors
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
            # Hash password and create account
            password_hash = flask_bcrypt.generate_password_hash(password)
            
            try:
                with db.get_cursor() as cursor:
                    cursor.execute('''
                                   INSERT INTO users (username, password_hash, email, role, status, first_name, last_name, location)
                                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                                   ''',
                                   (username, password_hash, email, DEFAULT_USER_ROLE, DEFAULT_USER_STATUS, first_name, last_name, location))
                
                # Show success message
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

    # Initial GET request
    return render_template('signup.html')

@app.route('/logout')
def logout():
    """End user session and redirect to login page."""
    # Remove session data
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    session.pop('temp_username', None)  # Also clear any temporary session data
    
    return redirect(url_for('login'))