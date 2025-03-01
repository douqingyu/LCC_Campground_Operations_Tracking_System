from lccapp import app, db
from flask import render_template, redirect, url_for, session, request, flash
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

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

@app.route('/issue/<int:issue_id>')
@login_required
def view_issue(issue_id):
    """View a specific issue and its comments.
    
    All users can view issues, but visitors can only view their own issues.
    """
    with db.get_cursor() as cursor:
        # Get issue details
        cursor.execute('''
            SELECT i.*, u.username, u.role, u.profile_image
            FROM issues i
            JOIN users u ON i.user_id = u.user_id
            WHERE i.issue_id = %s
        ''', (issue_id,))
        issue = cursor.fetchone()
        
        if not issue:
            flash('Issue not found', 'error')
            return redirect(url_for('admin_home' if session['role'] == 'admin' else 'visitor_home'))
        
        # Check permission - visitors can only view their own issues
        if session['role'] == 'visitor' and issue['user_id'] != session['user_id']:
            return render_template('access_denied.html'), 403
        
        # Get comments for this issue
        cursor.execute('''
            SELECT c.*, u.username, u.role, u.profile_image
            FROM comments c
            JOIN users u ON c.user_id = u.user_id
            WHERE c.issue_id = %s
            ORDER BY c.created_at
        ''', (issue_id,))
        comments = cursor.fetchall()
        
    return render_template('view_issue.html', 
                          issue=issue, 
                          comments=comments,
                          user_role=session['role'],
                          user_id=session['user_id'])

@app.route('/issue/<int:issue_id>/comment', methods=['POST'])
@login_required
def add_comment(issue_id):
    """Add a comment to an issue.
    
    All users can comment on issues they reported themselves.
    """
    content = request.form.get('content')
    if not content:
        flash('Comment cannot be empty', 'error')
        return redirect(url_for('view_issue', issue_id=issue_id))
    
    with db.get_cursor() as cursor:
        # Get the issue to check permission
        cursor.execute('SELECT * FROM issues WHERE issue_id = %s', (issue_id,))
        issue = cursor.fetchone()
        
        if not issue:
            flash('Issue not found', 'error')
            return redirect(url_for('admin_home' if session['role'] == 'admin' else 'visitor_home'))
        
        # Check permission - visitors can only comment on their own issues
        # Allow all users to comment on issues they reported themselves
        is_reporter = issue['user_id'] == session['user_id']
        is_staff = session['role'] in ['helper', 'admin']
        
        if not is_reporter and not is_staff:
            return render_template('access_denied.html'), 403
        
        # Add the comment
        cursor.execute('''
            INSERT INTO comments (issue_id, user_id, content, created_at)
            VALUES (%s, %s, %s, NOW())
        ''', (issue_id, session['user_id'], content))
    
    flash('Comment added successfully', 'success')
    return redirect(url_for('view_issue', issue_id=issue_id))

@app.route('/report', methods=['GET', 'POST'])
@login_required
def report_issue():
    """Report a new issue.
    
    This endpoint is accessible to all authenticated users regardless of their role.
    All issues must have a brief summary and a longer description.
    Issues always begin in 'new' status.
    """
    if request.method == 'POST':
        summary = request.form.get('summary')
        description = request.form.get('description')
        
        if not summary or not description:
            flash('Please provide both summary and description', 'danger')
            return render_template('report_issue.html')
        
        with db.get_cursor() as cursor:
            cursor.execute('''
                INSERT INTO issues (user_id, summary, description, status, created_at)
                VALUES (%s, %s, %s, 'new', NOW())
            ''', (session['user_id'], summary, description))
        
        flash('Issue reported successfully', 'success')
        
        # Redirect to the appropriate home page based on role
        return redirect(user_home_url())
        
    return render_template('report_issue.html')

@app.route('/resolved-issues')
@login_required
def resolved_issues():
    """View all resolved issues.
    
    This endpoint is restricted to helper and admin roles.
    """
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