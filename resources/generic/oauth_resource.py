"""
OAuth based authentication resource. This typically uses a token and a grant
type to define which oauth provider to query for verification.
"""
from flask_restful import Resource
from webargs.flaskparser import use_args

from services import AccountService
from ..args import post_oauth_args


class OAuth(Resource):
    """
    Resource for OAuth authentication.
    """

    @use_args(post_oauth_args)
    def post(self, args):
        grant_type = args['grant_type']
        token = args['token']

        result = AccountService.authenticate_oauth(grant_type, token)

        # Handle req parse
        return result, 200
