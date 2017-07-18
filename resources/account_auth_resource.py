"""
Account based authentication resource. This typically uses an email
and password.
"""
from flask_restful import Resource

from models import User
from security import get_access_token
from helpers.errors import InvalidCredentialsError
from helpers.reqparsers import rp_post_account_authentication

class AccountAuth(Resource):
    """
    Resource for account authentication.
    """
    parser = rp_post_account_authentication()

    def post(self):
        """
        Authenticate the provided email and password against the database.
        """
        args = self.parser.parse_args()

        user = User.find_by_email(args['email'])

        if user and user.verify_password(args['password']):
            return get_access_token(user.id), 200

        raise InvalidCredentialsError
