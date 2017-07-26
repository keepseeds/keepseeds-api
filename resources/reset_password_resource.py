
from flask_restful import Resource
from webargs.flaskparser import use_args

from helpers import validate_password, UnableToCompleteError
from models import User, Token, UserToken
from models.enums import TokenType

from .args import put_reset_password_args, post_reset_password_args


class ResetPassword(Resource):
    """
    Resource for recovering a forgotten password.

    The pattern for this endpoint:
    1. User submits email to the PUT endpoint, this send the user an email with
       a generated token that is saved to the database with an expiry date (24h).
    2. User retrieves the token from their email and submits it to the POST
       endpoint along with their username, new password and matching confirmation.
    """
    @use_args(post_reset_password_args)
    def post(self, args):
        email = args['email']
        password = args['password']
        password_confirm = args['passwordConfirm']
        token = args['token']

        user = User.find_by_email(email)

        if not user:
            raise UnableToCompleteError

        vr = UserToken.validate_token(user_id=user.id,
                                      token=token,
                                      token_type=TokenType.ResetPassword)

        if not vr.is_valid:
            raise UnableToCompleteError

        validate_password(password, password_confirm)

        if User.update_password(email, password):
            vr.user_token.expire()
            return {'message': 'Done.'}, 204

        raise UnableToCompleteError

    @use_args(put_reset_password_args)
    def put(self, args):
        user = User.find_by_email(args['email'])

        if not user:
            raise UnableToCompleteError

        token = Token.find_by_token_type(TokenType.ResetPassword)

        if not token:
            raise UnableToCompleteError

        new_user_token_id = UserToken.create(user, token)

        # This currently returns the plain token but it will need to
        # send it to the email provided.
        return {'userTokenId': new_user_token_id}, 202
