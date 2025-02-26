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