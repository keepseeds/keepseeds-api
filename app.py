"""
Main entry point for the application, this is
accessed as '__main__' when developing locally.
"""
import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.authentication_resource import AccountAuthentication, OAuthAuthentication
from resources.register_resource import Register

# Constants
DB_KEY = 'DATABASE_URL'
DB_LOCAL_PATH = 'postgresql://localhost/andy'

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET', 'TEST_SECRET')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(DB_KEY, DB_LOCAL_PATH)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

JWTManager(app)

api.add_resource(AccountAuthentication, '/auth')
api.add_resource(OAuthAuthentication, '/oauth')
api.add_resource(Register, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        """
        Create tables if not found.
        """
        db.create_all()

    app.run(port=5000, debug=True)
