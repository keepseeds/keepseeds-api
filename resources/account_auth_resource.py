"""
Account based authentication resource. This typically uses an email
and password.
"""
from flask_restful import Resource
from webargs.flaskparser import use_args

from models import User
from security import get_access_token
from helpers.errors import InvalidCredentialsError
from .args import post_account_auth_args


class AccountAuth(Resource):
    """
    Resource for account authentication.
    """

    @use_args(post_account_auth_args)
    def post(self, args):
        """
        Authenticate the provided email and password against the database.
        """
        user = User.find_by_email(args['email'])

        if user and user.verify_password(args['password']) and user.is_verified_email:
            return get_access_token(user.id), 200

        raise InvalidCredentialsError
