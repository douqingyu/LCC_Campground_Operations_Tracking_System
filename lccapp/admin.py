from lccapp import app, db, bcrypt
from flask import redirect, render_template, request, session, url_for, flash
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('login'))
        if session['role'] != 'admin':
            return render_template('access_denied.html'), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/home')
@admin_required
def admin_home():
    """Admin dashboard with issue statistics and active issues."""
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
        
        # Fetch active issues with user info
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

    return render_template('admin_home.html',
                         active_issues=active_issues,
                         new_count=status_counts['new'],
                         open_count=status_counts['open'],
                         stalled_count=status_counts['stalled'],
                         resolved_count=status_counts['resolved'])

@app.route('/admin/users', methods=['GET'])
@admin_required
def manage_users():
    """User management with optional search functionality."""
    search = request.args.get('search', '')
    
    with db.get_cursor() as cursor:
        if search:
            cursor.execute('''
                SELECT * FROM users 
                WHERE username LIKE %s 
                OR first_name LIKE %s 
                OR last_name LIKE %s
            ''', (f'%{search}%', f'%{search}%', f'%{search}%'))
        else:
            cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        
        # Get issue statistics
        cursor.execute('''
            SELECT status, COUNT(*) as count
            FROM issues
            GROUP BY status
        ''')
        status_results = cursor.fetchall()
        
        status_counts = {
            'new': 0,
            'open': 0,
            'stalled': 0,
            'resolved': 0
        }
        for row in status_results:
            if row['status'] in status_counts:
                status_counts[row['status']] = row['count']

    return render_template('admin_home.html', 
                           users=users, 
                           search=search,
                           show_users=True,
                           new_count=status_counts['new'],
                           open_count=status_counts['open'],
                           stalled_count=status_counts['stalled'],
                           resolved_count=status_counts['resolved'])

@app.route('/admin/users/<int:user_id>/status', methods=['POST'])
@admin_required
def change_user_status(user_id):
    """Toggle user active/inactive status."""
    new_status = request.form.get('status')
    if new_status not in ['active', 'inactive']:
        flash('Invalid status value', 'error')
        return redirect(url_for('manage_users'))

    with db.get_cursor() as cursor:
        cursor.execute('''
            UPDATE users 
            SET status = %s 
            WHERE user_id = %s
        ''', (new_status, user_id))

    flash('User status updated successfully', 'success')
    return redirect(url_for('manage_users'))

@app.route('/admin/users/<int:user_id>/role', methods=['POST'])
@admin_required
def change_user_role(user_id):
    """Update user permission role."""
    new_role = request.form.get('role')
    if new_role not in ['visitor', 'helper', 'admin']:
        flash('Invalid role value', 'error')
        return redirect(url_for('manage_users'))

    with db.get_cursor() as cursor:
        cursor.execute('''
            UPDATE users 
            SET role = %s 
            WHERE user_id = %s
        ''', (new_role, user_id))

    flash('User role updated successfully', 'success')
    return redirect(url_for('manage_users'))

@app.route('/admin/issue/<int:issue_id>/status', methods=['POST'])
@admin_required
def change_issue_status(issue_id):
    """Update issue workflow status."""
    new_status = request.form.get('status')
    if new_status not in ['new', 'open', 'stalled', 'resolved']:
        flash('Invalid status value', 'error')
        return redirect(url_for('admin_home'))

    with db.get_cursor() as cursor:
        cursor.execute('''
            UPDATE issues 
            SET status = %s 
            WHERE issue_id = %s
        ''', (new_status, issue_id))

    flash('Issue status updated successfully', 'success')
    return redirect(url_for('admin_home'))