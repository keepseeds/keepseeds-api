"""
Module for the Register class, this class interacts
with the database via SQLAlchemy.
"""
from flask_restful import Resource
from werkzeug.security import safe_str_cmp

from models.model import User
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
            return {'message': 'Unable to create user.'}

        if not safe_str_cmp(password, password_confirm):
            return {'message': 'Passwords do not match.'}

        user_id = User.create(email, first, last, password)

        return {'message': 'Created successfully, please log in.', "id": user_id}, 201
