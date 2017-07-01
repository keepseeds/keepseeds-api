"""
Main entry point for the application, this is
accessed as '__main__' when developing locally.
"""
import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET', '')

api = Api(app)

jwt = JWT(app, authenticate, identity)

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
