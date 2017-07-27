
from flask_restful import Resource
from webargs.flaskparser import use_args

from services import AccountService
from .args import put_reset_password_args, post_reset_password_args


class ResetPassword(Resource):
    """
    Resource for recovering a forgotten password.

    The pattern for this endpoint:
    1. User submits email to the PUT endpoint, this send the user an email with
       a generated token that is saved to the database with an expiry date (24h).
    2. User retrieves the token from their email and submits it to the POST
       endpoint along with their username, new password and matching confirmation.
    """

    account_service = AccountService()

    @use_args(post_reset_password_args)
    def post(self, args):
        email = args['email']
        password = args['password']
        password_confirm = args['passwordConfirm']
        token = args['token']

        result = self.account_service.resolve_password_reset(
            email,
            password,
            password_confirm,
            token
        )

        return result, 204


    @use_args(put_reset_password_args)
    def put(self, args):
        email = args['email']

        result = self.account_service.request_password_reset(email)

        # This currently returns the plain token but it will need to
        # send it as an email to the user.
        return result, 202
