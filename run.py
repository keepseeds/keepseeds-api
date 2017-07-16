"""
Entry point for hoisted application.
"""
from app import app
from db import db

db.init_app(app)

@app.before_first_request
def create_tables():
    """
    Create tables if not found.
    """
    db.create_all()
