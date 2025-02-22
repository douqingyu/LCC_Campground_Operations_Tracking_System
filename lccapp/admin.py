from lccapp import app, db, bcrypt
from flask import redirect, render_template, request, session, url_for, flash

# Helper function to check admin access
def is_admin():
    """Check if the current user is an admin"""
    return 'loggedin' in session and session['role'] == 'admin'

@app.route('/admin/home')
def admin_home():
    """Admin Homepage endpoint.
    
    Shows list of all issues with management options and user management links.
    Requires admin role.
    """
    if not is_admin():
        return render_template('access_denied.html'), 403

    # Get all issues for admin view
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT i.*, u.username, u.role, u.profile_image
            FROM issues i
            JOIN users u ON i.user_id = u.user_id
            ORDER BY i.status, i.created_at DESC
        ''')
        issues = cursor.fetchall()

    return render_template('admin/home.html', issues=issues)

@app.route('/admin/users', methods=['GET'])
def manage_users():
    """User management page.
    
    Allows searching users and viewing their details.
    Search by username, first name, or last name.
    """
    if not is_admin():
        return render_template('access_denied.html'), 403

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

    return render_template('admin/users.html', users=users, search=search)

@app.route('/admin/users/<int:user_id>/status', methods=['POST'])
def change_user_status(user_id):
    """Change user's active/inactive status"""
    if not is_admin():
        return render_template('access_denied.html'), 403

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
def change_user_role(user_id):
    """Change user's role (visitor/helper/admin)"""
    if not is_admin():
        return render_template('access_denied.html'), 403

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

@app.route('/admin/issues/<int:issue_id>/status', methods=['POST'])
def change_issue_status(issue_id):
    """Change issue status"""
    if not is_admin():
        return render_template('access_denied.html'), 403

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