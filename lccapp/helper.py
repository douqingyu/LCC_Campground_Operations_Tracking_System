from lccapp import app, db
from flask import redirect, render_template, session, url_for, request, flash
from functools import wraps

def helper_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('login'))
        if session['role'] != 'helper':
            return render_template('access_denied.html'), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/helper/home')
@helper_required
def helper_home():
    """Dashboard for helpers showing active issues that need attention."""
    # Get issue statistics
    with db.get_cursor() as cursor:
        # Count issues by status
        cursor.execute('''
            SELECT status, COUNT(*) as count
            FROM issues
            GROUP BY status
        ''')
        status_results = cursor.fetchall()
        
        # Initialize status counts
        status_counts = {
            'new': 0,
            'open': 0,
            'stalled': 0,
            'resolved': 0
        }
        for row in status_results:
            if row['status'] in status_counts:
                status_counts[row['status']] = row['count']
        
        # Fetch active issues with user details
        cursor.execute('''
            SELECT i.*, u.username, u.profile_image
            FROM issues i
            JOIN users u ON i.user_id = u.user_id
            WHERE i.status != 'resolved'
            ORDER BY 
                CASE i.status
                    WHEN 'new' THEN 1
                    WHEN 'open' THEN 2
                    WHEN 'stalled' THEN 3
                END,
                i.created_at DESC
        ''')
        active_issues = cursor.fetchall()
        
        # Add color codes for status display
        for issue in active_issues:
            issue['status_color'] = {
                'new': 'danger',
                'open': 'primary',
                'stalled': 'warning',
                'resolved': 'success'
            }.get(issue['status'], 'secondary')

    return render_template('helper_home.html',
                         active_issues=active_issues,
                         new_count=status_counts['new'],
                         open_count=status_counts['open'],
                         stalled_count=status_counts['stalled'],
                         resolved_count=status_counts['resolved'])

@app.route('/helper/issue/<int:issue_id>/status', methods=['POST'])
@helper_required
def helper_change_issue_status(issue_id):
    """Update an issue's workflow status."""
    new_status = request.form.get('status')
    if new_status not in ['new', 'open', 'stalled', 'resolved']:
        flash('Invalid status value', 'error')
        return redirect(url_for('helper_home'))

    with db.get_cursor() as cursor:
        cursor.execute('''
            UPDATE issues 
            SET status = %s 
            WHERE issue_id = %s
        ''', (new_status, issue_id))

    flash('Issue status updated successfully', 'success')
    
    # Get the source parameter to determine where to redirect
    source = request.form.get('source')
    
    # Redirect based on source or referrer
    if source == 'my_issues':
        return redirect(url_for('helper_issues'))
    elif request.referrer:
        return redirect(request.referrer)
    else:
        return redirect(url_for('helper_home'))

@app.route('/helper/issues')
@helper_required
def helper_issues():
    """View issues reported by the current helper."""
    with db.get_cursor() as cursor:
        # Fetch issues reported by the current user
        cursor.execute('''
            SELECT i.*
            FROM issues i
            WHERE i.user_id = %s
            ORDER BY i.created_at DESC
        ''', (session['user_id'],))
        my_issues = cursor.fetchall()
        
        for issue in my_issues:
            issue['status_color'] = {
                'new': 'danger',
                'open': 'primary',
                'stalled': 'warning',
                'resolved': 'success'
            }.get(issue['status'], 'secondary')
            
        # Count issues by status
        cursor.execute('''
            SELECT status, COUNT(*) as count
            FROM issues
            GROUP BY status
        ''')
        status_results = cursor.fetchall()
        
        # Initialize status counts
        status_counts = {
            'new': 0,
            'open': 0,
            'stalled': 0,
            'resolved': 0
        }
        for row in status_results:
            if row['status'] in status_counts:
                status_counts[row['status']] = row['count']

    return render_template('helper_home.html',
                         my_issues=my_issues,
                         show_my_issues=True,
                         new_count=status_counts['new'],
                         open_count=status_counts['open'],
                         stalled_count=status_counts['stalled'],
                         resolved_count=status_counts['resolved'])