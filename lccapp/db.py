"""Implements simple MySQL database connectivity for a Flask web app."""
from flask import Flask, g
from mysql.connector.pooling import MySQLConnectionPool

# Connection pool created by init_db
connection_pool: MySQLConnectionPool

def init_db(app: Flask, user: str, password: str, host: str, database: str,
            pool_name: str = "flask_db_pool", autocommit: bool = True):
    """Sets up MySQL connectivity for the specified Flask app."""
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
    """Gets a MySQL database connection to use while serving the current Flask request."""
    if 'db' not in g:
        g.db = connection_pool.get_connection()
    
    return g.db

def get_cursor():
    """Gets a new MySQL dictionary cursor to use while serving the current Flask request."""
    return get_db().cursor(dictionary=True)

def close_db(exception = None):
    """Closes the MySQL database connection associated with the current Flask request."""
    # Get and remove db from application context
    db = g.pop('db', None)
    
    if db is not None:
        db.close()