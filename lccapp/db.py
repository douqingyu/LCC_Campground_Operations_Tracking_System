"""MySQL database connectivity for Flask web applications.

Provides database connection handling for Flask requests based on the Flask tutorial pattern.
Uses mysqlclient package which is compatible with Windows 10/11 and PythonAnywhere.

Basic usage:
1. Initialize: db.init_db(app, 'username', 'password', 'host', 'database')
2. Get connection: db = db.get_db()
3. Get cursor: cursor = db.get_cursor() or with get_cursor() as cursor: ...

Database connections are automatically closed at the end of requests.
Remember to close any cursors you create.
"""
from flask import Flask, g
from mysql.connector.pooling import MySQLConnectionPool

# Connection pool (created by init_db)
connection_pool: MySQLConnectionPool

def init_db(app: Flask, user: str, password: str, host: str, database: str,
            pool_name: str = "flask_db_pool", autocommit: bool = True):
    """Set up MySQL connection pool for a Flask app.
    
    Args:
        app: Flask application
        user: MySQL username
        password: MySQL password
        host: MySQL server host
        database: Database name
        pool_name: Connection pool name
        autocommit: Whether to enable auto-commit
    """
    # Create connection pool
    global connection_pool
    connection_pool = MySQLConnectionPool(
        user=user,
        password=password,
        host=host,
        database=database,
        pool_name=pool_name,
        autocommit=autocommit)

    # Register cleanup function to run after each request
    app.teardown_appcontext(close_db)

def get_db():
    """Get a MySQL connection for the current Flask request.
    
    Returns the same connection if called multiple times in one request.
    Connection is automatically returned to the pool after the request.
    
    Returns:
        A database connection from the pool
    """
    if 'db' not in g:
        g.db = connection_pool.get_connection()
    
    return g.db

def get_cursor():
    """Get a new MySQL dictionary cursor for the current request.
    
    All cursors from this function share the same connection.
    Always close these cursors when finished.
    
    Returns:
        A new MySQL cursor with dictionary result format
    """
    return get_db().cursor(dictionary=True)

def close_db(exception = None):
    """Close the current request's database connection.
    
    Called automatically at the end of each Flask request.
    
    Args:
        exception: Exception that ended the request (if any)
    """
    # Get and remove db from application context
    db = g.pop('db', None)
    
    if db is not None:
        db.close()