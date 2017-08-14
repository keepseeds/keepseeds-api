"""
Module for the ChildrenResource class, this class interacts
with the database via ChildService.
"""
from flask_restful import Resource, marshal_with, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from webargs.flaskparser import use_args

from services import ChildService
from resources._args import post_children_args
from resources._marshallers import list_child_marshal, single_child_marshal


class Children(Resource):
    """
    Represents the Children resource in the API.
    """

    @jwt_required
    def get(self):
        """
        Get all children for the current user.
        """
        result = ChildService.find_users_children(get_jwt_identity())

        return {
            'owned': marshal(result['owned'], list_child_marshal),
            'included': marshal(result['included'], list_child_marshal)
        }, 200

    @jwt_required
    @marshal_with(single_child_marshal)
    @use_args(post_children_args)
    def post(self, args):
        """
        Add a new Child entity.
        """
        first = args['first_name']
        last = args['last_name']
        dob = args['date_of_birth']
        gender_id = args['gender_id']
        middle = args.get('middle_name', None)

        result = ChildService.create(
            first=first,
            last=last,
            dob=dob,
            gender_id=gender_id,
            created_by=get_jwt_identity(),
            middle=middle)

        return result, 201
