from flask_restful import Resource, reqparse

class AccountAuthentication(Resource):
    """
    Resource for account authentication.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        required=True,
                        type=str,
                        help='Email is required.')
    parser.add_argument('password',
                        required=True,
                        type=str,
                        help='Password is required.')

    def post(self):
        args = self.parser.parse_args()

        # Handle req parse
        return {'accessToken': 'abc'}

class OAuthAuthentication(Resource):
    """
    Resource for OAuth authentication.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('grantType',
                        required=True,
                        type=str,
                        help='Grant Type is required.')
    parser.add_argument('user_id',
                        required=True,
                        type=int,
                        help='User ID is required.')
    parser.add_argument('token',
                        required=True,
                        type=str,
                        help='Token is required.')

    def post(self):
        args = self.parser.parse_args()

        # Handle req parse
        return {'accessToken': 'def'}
