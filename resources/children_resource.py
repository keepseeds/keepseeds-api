"""
Module for the ChildrenResource class, this class interacts
with the database via ChildService.
"""
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from webargs.flaskparser import use_args

from services import ChildService
from .args import post_children_args

class Children(Resource):
    """
    Represents the Children resource in the API.
    """

    @jwt_required
    def get(self):
        """
        Get all children for the current user.
        """
        return ChildService.find_children(get_jwt_identity()), 200

    @jwt_required
    @use_args(post_children_args)
    def post(self, args):
        """
        Add a new Child entity.
        """
        first = args['first_name']
        last = args['last_name']
        dob = args['date_of_birth']
        gender = args['gender']
        middle = args['middle_name']

        result = ChildService.create(first, last, dob, gender, middle)

        return result, 201
