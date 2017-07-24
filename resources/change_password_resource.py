"""
Module for the ChangePassword class, this class interacts
with the database via SQLAlchemy.
"""
from flask_restful import Resource
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import jwt_required
from webargs.flaskparser import use_args

from args import put_change_password_args
from models import User
from helpers.errors import UnableToCompleteError, PasswordsDoNotMatchError
from responses import DoneResponse


class ChangePassword(Resource):
    """
    Represents a ChangePassword resource in the API.
    """
    @jwt_required
    @use_args(put_change_password_args)
    def put(self, args):
        email = args['email']
        password = args['password']
        password_confirm = args['passwordConfirm']
        old_password = args['oldPassword']

        user = User.find_by_email(email)

        if not user or not user.verify_password(old_password):
            raise UnableToCompleteError

        if not safe_str_cmp(password, password_confirm):
            raise PasswordsDoNotMatchError

        if User.update_password(email, password):
            return DoneResponse().json(), 204

        raise UnableToCompleteError
