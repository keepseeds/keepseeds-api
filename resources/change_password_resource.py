"""
Module for the ChangePassword class, this class interacts
with the database via SQLAlchemy.
"""
from flask_restful import Resource
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import jwt_required
from webargs.flaskparser import use_args

from helpers import validate_password
from helpers.errors import UnableToCompleteError
from models import User
from .args import put_change_password_args


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

        validate_password(password, password_confirm)

        if User.update_password(email, password):
            return {'message': 'Done.'}, 204

        raise UnableToCompleteError
