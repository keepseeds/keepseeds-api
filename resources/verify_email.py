
from flask_restful import Resource
from webargs.flaskparser import use_args

from args import post_verify_email_args
from models.enums import TokenType
from models import User, UserToken
from helpers.errors import UnableToCompleteError
from responses import DoneResponse


class VerifyEmail(Resource):

    @use_args(post_verify_email_args)
    def post(self, args):
        email = args['email']
        token = args['token']

        user = User.find_by_email(email)

        if not user:
            raise UnableToCompleteError

        vr = UserToken.validate_token(user.id, token, TokenType.VerifyEmail)

        if not vr.is_valid:
            raise UnableToCompleteError

        if user.set_is_verified_email():
            vr.user_token.expire()

        return DoneResponse().json(), 204
