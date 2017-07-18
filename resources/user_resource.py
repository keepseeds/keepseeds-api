"""
Module for the UserResource class, this class interacts
with the database via SQLAlchemy.
"""
from flask_restful import Resource
from models import User


class UserResource(Resource):
    """
    Represents a User resource in the API.
    """

    def get(self, id):
        pass

    def post(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

    def patch(self, id):
        pass
