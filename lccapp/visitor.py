from lccapp import app, db
from flask import redirect, render_template, session, url_for, request, flash
from functools import wraps

def visitor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('login'))
        if session['role'] != 'visitor':
            return render_template('access_denied.html'), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/visitor/home')
@visitor_required
def visitor_home():
    """Visitor Homepage endpoint.
    
    Shows recent issues reported by the visitor and provides
    a quick link to report new issues.
    """
    with db.get_cursor() as cursor:
        # Get recent issues reported by this visitor
        cursor.execute('''
            SELECT i.*, 
                  (SELECT COUNT(*) FROM comments WHERE issue_id = i.issue_id) AS comment_count
            FROM issues i
            WHERE i.user_id = %s
            ORDER BY i.created_at DESC
            LIMIT 5
        ''', (session['user_id'],))
        recent_issues = cursor.fetchall()
        
        # Add status colors for easier display
        for issue in recent_issues:
            issue['status_color'] = {
                'new': 'danger',
                'open': 'primary',
                'stalled': 'warning',
                'resolved': 'success'
            }.get(issue['status'], 'secondary')

    return render_template('visitor_home.html', recent_issues=recent_issues)

# Updated to use the common report_issue.html template
@app.route('/visitor/report', methods=['GET', 'POST'])
@visitor_required
def visitor_report():
    """Report a new issue."""
    if request.method == 'POST':
        summary = request.form.get('summary')
        description = request.form.get('description')
        
        if not summary or not description:
            flash('Please provide both summary and description', 'danger')
            return render_template('report_issue.html')  # Changed from visitor_report.html
        
        with db.get_cursor() as cursor:
            cursor.execute('''
                INSERT INTO issues (user_id, summary, description, status, created_at)
                VALUES (%s, %s, %s, 'new', NOW())
            ''', (session['user_id'], summary, description))
        
        flash('Issue reported successfully', 'success')
        return redirect(url_for('visitor_home'))
        
    return render_template('report_issue.html')  # Changed from visitor_report.html

@app.route('/visitor/issues')
@visitor_required
def my_issues():
    """View all issues reported by the current visitor."""
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT i.*, 
                  (SELECT COUNT(*) FROM comments WHERE issue_id = i.issue_id) AS comment_count
            FROM issues i
            WHERE i.user_id = %s
            ORDER BY i.created_at DESC
        ''', (session['user_id'],))
        issues = cursor.fetchall()
        
        # Add status colors for easier display
        for issue in issues:
            issue['status_color'] = {
                'new': 'danger',
                'open': 'primary',
                'stalled': 'warning',
                'resolved': 'success'
            }.get(issue['status'], 'secondary')
    
    return render_template('visitor_issues.html', issues=issues)