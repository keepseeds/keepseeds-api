"""
Resource module for the ChildResource class.
"""
from flask_restful import Resource, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from webargs.flaskparser import use_args

from services import ChildService
from ..args import patch_child_args
from ..marshals import single_child_marshal


class Child(Resource):
    """
    Represents a Child resource in the API.
    """

    @jwt_required
    @marshal_with(single_child_marshal)
    def get(self, child_id):
        """
        Get a specific Child entity.
        """
        user_id = get_jwt_identity()
        result = ChildService.find_child(identifier=child_id, user_id=user_id)

        return result, 200

    @jwt_required
    @use_args(patch_child_args)
    @marshal_with(single_child_marshal)
    def patch(self, args, child_id):
        """
        Update a Child entity.
        """
        user_id = get_jwt_identity()
        result = ChildService.update(child_id, user_id, args)

        return result, 200

    @jwt_required
    def delete(self, child_id):
        """
        Mark a Child entity as deleted.
        """
        user_id = get_jwt_identity()
        result = ChildService.delete_child(child_id, user_id)

        return result, 204
