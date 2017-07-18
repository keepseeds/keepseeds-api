"""
Module for the Register class, this class interacts
with the database via SQLAlchemy.
"""
from exceptions import UnableToCompleteError, PasswordsDoNotMatchError
from flask_restful import Resource
from werkzeug.security import safe_str_cmp

from models import User
from helpers.reqparsers.register import post_request_parser

class Register(Resource):
    """
    Represents a Registration resource in the API.
    """
    parser = post_request_parser()

    def post(self):
        """
        Registration request.
        """
        args = self.parser.parse_args()

        email = args['email']
        first = args['firstName']
        last = args['lastName']
        password = args['password']
        password_confirm = args['passwordConfirm']

        if User.find_by_email(email):
            raise UnableToCompleteError

        if not safe_str_cmp(password, password_confirm):
            raise PasswordsDoNotMatchError

        User.create(email, first, last, password)

        return 201
