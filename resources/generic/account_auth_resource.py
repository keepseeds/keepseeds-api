"""
Account based authentication resource. This typically uses an email
and password.
"""
from flask_restful import Resource
from webargs.flaskparser import use_args

from services import AccountService
from ..args import post_account_auth_args


class AccountAuth(Resource):
    """
    Resource for account authentication.
    """

    @use_args(post_account_auth_args)
    def post(self, args):
        """
        Authenticate the provided email and password against the database.
        """
        email = args['email']
        password = args['password']

        result = AccountService.authenticate_user(email, password)

        return result, 200
        