"""
Module for the Register class, this class interacts
with the database via SQLAlchemy.
"""
from flask_restful import Resource
from webargs.flaskparser import use_args

from services import AccountService
from ..args import post_register_args


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
        first = args['first_name']
        last = args['last_name']
        password = args['password']
        password_confirm = args['password_confirm']

        create_user_result = AccountService.register_user(
            email,
            first,
            last,
            password,
            password_confirm
        )

        return create_user_result, 201
