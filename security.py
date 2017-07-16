"""
Security definition for the API.
"""
from flask_jwt_extended import create_access_token

def get_access_token(identifier):
    return {'accessToken': create_access_token(identity=identifier)}
