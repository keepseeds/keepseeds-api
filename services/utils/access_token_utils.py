
from flask_jwt_extended import create_access_token

def get_access_token(identifier):
    """
    Generate and return an access token using the
    provided identifier.

    :param identifier: Unique id to identify this user.
    :rtype: dict
    """
    return {'accessToken': create_access_token(identity=identifier)}
