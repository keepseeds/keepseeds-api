"""
Module for the ChangePassword class, this class interacts
with the database via SQLAlchemy.
"""
from flask_restful import Resource
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import jwt_required
from webargs.flaskparser import use_args

from helpers import validate_password, UnableToCompleteError
from models import User
from services import AccountService

from .args import put_change_password_args


class ChangePassword(Resource):
    """
    Represents a ChangePassword resource in the API.
    """

    @jwt_required
    @use_args(put_change_password_args)
    def put(self, args):
        old_password = args['oldPassword']
        password = args['password']
        password_confirm = args['passwordConfirm']

        AccountService.change_password(
            old_password,
            password,
            password_confirm
        )

        return {'message': 'Done.'}, 204
