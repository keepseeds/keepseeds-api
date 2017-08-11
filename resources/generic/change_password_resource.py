"""
Module for the ChangePassword class, this class interacts
with the database via AccountService.
"""
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from webargs.flaskparser import use_args

from services import AccountService
from resources._args import put_change_password_args


class ChangePassword(Resource):
    """
    Represents a ChangePassword resource in the API.
    """

    @jwt_required
    @use_args(put_change_password_args)
    def put(self, args):
        old_password = args['old_password']
        password = args['password']
        password_confirm = args['password_confirm']

        AccountService.change_password(
            old_password,
            password,
            password_confirm,
            get_jwt_identity()
        )

        return {'message': 'Done.'}, 204
