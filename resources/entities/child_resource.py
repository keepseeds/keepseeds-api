"""
Resource module for the ChildResource class.
"""
from flask_restful import Resource, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from webargs.flaskparser import use_args


from services import ChildService
from resources._args import put_child_args
from resources._marshallers import single_child_marshal

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
        result = ChildService.find_child(_id=child_id, user_id=user_id)

        return result, 200


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

    @jwt_required
    def delete(self, child_id):
        """
        Mark a Child entity as deleted.
        """
        user_id = get_jwt_identity()
        result = ChildService.delete_child(child_id, user_id)

        return result, 204
