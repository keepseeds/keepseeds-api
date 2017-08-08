from flask_restful import Resource
from flask_jwt_extended import jwt_required

class ChildrenResource(Resource):
    """
    Represents the Children resource in the API.
    """

    @jwt_required
    def get(self):
        """
        Get all children for the current user.
        """
        pass

    def post(self):
        """
        Add a new Child entity.
        """
        pass
