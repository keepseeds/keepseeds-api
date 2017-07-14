"""
Security definition for the API.
"""
from models.user import User
from flask_jwt_extended import create_access_token

def get_access_token(grantType, identifier, token):
    user = None

    if grantType == 'account':
        user = User.find_by_email(identifier)

        if not user:
            return {'message': 'Unable to authenticate user.'}
    else:
        user = None # Lookup from grants.

    return {'accessToken': create_access_token(identifier=identifier)}
