
from flask_restful import Resource
from webargs.flaskparser import use_args

from services import AccountService
from .args import post_oauth_args

class OAuth(Resource):
    """
    Resource for OAuth authentication.
    """

    account_service = AccountService()

    @use_args(post_oauth_args)
    def post(self, args):
        grant_type = args['grantType']
        token = args['token']

        result = self.account_service.oauth_authentication(grant_type, token)

        # Handle req parse
        return result, 200
