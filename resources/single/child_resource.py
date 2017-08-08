"""
Resource module for the ChildResource class.
"""
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from webargs.flaskparser import use_args

from .args import put_child_args

class ChildResource(Resource):
    """
    Represents a Child resource in the API.
    """

    @jwt_required
    def get(self, child_id):
        """
        Get a specific Child entity.
        """
        pass


    @jwt_required
    @use_args(put_child_args)
    def put(self, args, child_id):
        """
        Update a Child entity.
        """
        return {
            'child_id': child_id,
            'args': args,
            'user': get_jwt_identity()
        }

    def delete(self, child_id):
        """
        Mark a Child entity as deleted.
        """
        pass

