"""
Module for the UserResource class, this class interacts
with the database via SQLAlchemy.
"""
from flask_restful import Resource
from models.user_model import UserModel
from core.rest_response import NotFoundResponse, SuccessResponse

class UserResource(Resource):
    """
    Represents a User resource in the API.
    """

    def get(self, id):
        return SuccessResponse('')

    def post(self, id):
        return NotFoundResponse().json()

    def put(self, id):
        pass

    def delete(self, id):
        pass

    def patch(self, id):
        pass
