"""
Module for the Register class, this class interacts
with the database via SQLAlchemy.
"""
from flask_restful import Resource
from werkzeug.security import safe_str_cmp
from webargs.flaskparser import use_args

from args import post_register_args
from models import User
from helpers.errors import UnableToCompleteError, PasswordsDoNotMatchError


class Register(Resource):
    """
    Represents a Registration resource in the API.
    """

    @use_args(post_register_args)
    def post(self, args):
        """
        Registration request.
        """
        email = args['email']
        first = args['firstName']
        last = args['lastName']
        password = args['password']
        password_confirm = args['passwordConfirm']

        if User.find_by_email(email):
            raise UnableToCompleteError

        if not safe_str_cmp(password, password_confirm):
            raise PasswordsDoNotMatchError

        create_user_result = User.create(email, first, last, password)

        return create_user_result, 201
