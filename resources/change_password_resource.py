"""
Module for the ChangePassword class, this class interacts
with the database via SQLAlchemy.
"""
from flask_restful import Resource
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import jwt_required

from models.model import User
from helpers.reqparsers.change_password import put_request_parser
from core.exceptions.resource_exceptions import UnableToCompleteError,\
                                                PasswordsDoNotMatchError

class ChangePassword(Resource):
    """
    Represents a ChangePassword resource in the API.
    """
    put_parser = put_request_parser()

    @jwt_required
    def put(self):
        args = self.put_parser.parse_args()

        email = args['email']
        password = args['password']
        password_confirm = args['passwordConfirm']
        old_password = args['oldPassword']

        user = User.find_by_email(email)

        if not user:
            raise UnableToCompleteError

        if not user.verify_password(old_password):
            raise UnableToCompleteError

        if not safe_str_cmp(password, password_confirm):
            raise PasswordsDoNotMatchError

        if User.update_password(email, password):
            return 204

        raise UnableToCompleteError
