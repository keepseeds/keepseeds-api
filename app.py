"""
Main entry point for the application, this is
accessed as '__main__' when developing locally.
"""
import os

from helpers import resource_errors
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

import resources as res

# Constants
DB_KEY = 'DATABASE_URL'
DB_LOCAL_PATH = 'postgresql://localhost/andy'

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET', 'TEST_SECRET')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(DB_KEY, DB_LOCAL_PATH)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app, errors=resource_errors)

JWTManager(app)

# Authentication Resources
api.add_resource(res.AccountAuth, '/auth')
api.add_resource(res.OAuth, '/oauth')
api.add_resource(res.Register, '/register')
api.add_resource(res.ChangePassword, '/change-password')
api.add_resource(res.ResetPassword, '/reset-password')
api.add_resource(res.VerifyEmail, '/verify-email')

# Collection Resources
api.add_resource(res.Children, '/children')

# Single Entity Resources
api.add_resource(res.Child, '/child/<int:child_id>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    app.run(port=5000, debug=True)
