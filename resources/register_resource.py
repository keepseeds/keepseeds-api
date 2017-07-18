"""
Module for the Register class, this class interacts
with the database via SQLAlchemy.
"""
from flask_restful import Resource
from werkzeug.security import safe_str_cmp

from models import User
from helpers.errors import UnableToCompleteError, PasswordsDoNotMatchError
from helpers.reqparsers import rp_post_register

class Register(Resource):
    """
    Represents a Registration resource in the API.
    """
    parser = rp_post_register()

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
