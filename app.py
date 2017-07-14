"""
Main entry point for the application, this is
accessed as '__main__' when developing locally.
"""
import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.authentication_resource import AccountAuthentication, OAuthAuthentication

# Constants
DB_KEY = 'DATABASE_URL'
DB_LOCAL_PATH = 'sqlite:///data.db'

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET', '')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(DB_KEY, DB_LOCAL_PATH)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

JWTManager(app)

api.add_resource(AccountAuthentication, '/auth')
api.add_resource(OAuthAuthentication, '/oauth')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
