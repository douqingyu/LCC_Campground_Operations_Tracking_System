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
    """Helper Homepage endpoint.
    
    Shows active issues requiring attention.
    """
    # Get issue statistics
    with db.get_cursor() as cursor:
        # Get counts for each status
        cursor.execute('''
            SELECT status, COUNT(*) as count
            FROM issues
            GROUP BY status
        ''')
        status_results = cursor.fetchall()
        
        # Convert to dictionary
        status_counts = {
            'new': 0,
            'open': 0,
            'stalled': 0,
            'resolved': 0
        }
        for row in status_results:
            if row['status'] in status_counts:
                status_counts[row['status']] = row['count']
        
        # Get active issues with creator info
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
        
        # Add status colors for easier display
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
    """Change issue status"""
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
    return redirect(url_for('helper_home'))