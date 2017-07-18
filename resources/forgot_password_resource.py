
from flask_restful import Resource
from werkzeug.security import safe_str_cmp

from models import User
from helpers.errors import UnableToCompleteError, PasswordsDoNotMatchError
from helpers.reqparsers import rp_put_forgot_password, rp_post_forgot_password

class ForgotPassword(Resource):
    """
    Resource for recovering a forgotten password.

    The pattern for this endpoint:
    1. User submits email to the PUT endpoint, this send the user an email with
       a generated token that is saved to the database with an expiry date (24h).
    2. User retrieves the token from their email and submits it to the POST
       endpoint along with their username, new password and matching confirmation.
    """
    put_parser = rp_put_forgot_password()
    post_parser = rp_post_forgot_password()

    def post(self):
        args = self.post_parser.parse_args()
        email = args['email']
        password = args['password']
        password_confirm = args['passwordConfirm']
        token = args['token']

        user = User.find_by_email(email)

        if not user:
            raise UnableToCompleteError

        # 1. Validate email token
        if not safe_str_cmp(token, 'f0ca1654-3b50-41f3-9cc9-64b6db5f3c20'):
            raise UnableToCompleteError

        if not safe_str_cmp(password, password_confirm):
            raise PasswordsDoNotMatchError

        if User.update_password(email, password):
            return 204

        return 500

    def put(self):
        args = self.put_parser.parse_args()

        user = User.find_by_email(args['email'])

        if not user:
            raise UnableToCompleteError

        # 1. Create email reset token here.

        return 202
