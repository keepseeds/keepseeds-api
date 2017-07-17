from flask_restful import Resource
from models.model import User
from werkzeug.security import safe_str_cmp

from core.exceptions.resource_exceptions import UnableToCompleteError,\
                                                PasswordsDoNotMatchError

from helpers.reqparsers.forgot_password import put_request_parser,\
                                               post_request_parser

class ForgotPassword(Resource):
    put_parser = put_request_parser()
    post_parser = post_request_parser()

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
