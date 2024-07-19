from flask import Flask, render_template
import sqlite3
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__, template_folder='../templates')
app.config['CAR_DATABASE'] = 'cars.db'
app.config['PROBLEM_DATABASE'] = 'problems.db'

def get_car_db():
    conn = sqlite3.connect(app.config['CAR_DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def get_problem_db():
    conn = sqlite3.connect(app.config['PROBLEM_DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def get_relationship_db():
    conn = sqlite3.connect('car_problems.db')
    conn.row_factory = sqlite3.Row
    return conn

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Internal server error: {error}')
    return render_template('500.html'), 500

# Set up logging
if not app.debug:
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)

# Import routes after initializing the app to avoid circular imports
from app import routes
