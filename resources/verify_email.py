
from flask_restful import Resource
from models.enums import TokenType
from models import User, UserToken
from helpers.errors import UnableToCompleteError
from helpers.reqparsers import rp_post_verify_email
from responses import DoneResponse


class VerifyEmail(Resource):

    post_parser = rp_post_verify_email()

    def post(self):
        args = self.post_parser.parse_args()
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
