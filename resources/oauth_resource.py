
from flask_restful import Resource
from webargs.flaskparser import use_args

from models import User
from security import get_access_token
from helpers import InvalidCredentialsError

from .args import post_oauth_args

class OAuth(Resource):
    """
    Resource for OAuth authentication.
    """
    @use_args(post_oauth_args)
    def post(self, args):
        grant_type = args['grantType']
        token = args['token']

        if not grant_type in ('facebook',):
            raise InvalidCredentialsError

        # 1. Ensure we support grantType provided
        # 2. Look up user based on token via 3rd party, ensure the access token
        #    belongs to our app and they have granted required permissions.
        # 3. Look up user id locally in user_grants.
        # 4. If the user doesn't exist we need to create it and get the id.
        # 5. Finally, return an access token using get_access_token and our
        #    local user id.

        # Handle req parse
        raise NotImplementedError
