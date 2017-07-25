"""
Module for the Register class, this class interacts
with the database via SQLAlchemy.
"""
from flask_restful import Resource
from werkzeug.security import safe_str_cmp
from webargs.flaskparser import use_args

from helpers import validate_password
from models import User
from helpers.errors import UnableToCompleteError
from .args import post_register_args


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

        validate_password(password, password_confirm)

        create_user_result = User.create(email, first, last, password)

        return create_user_result, 201
