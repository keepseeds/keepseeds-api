
from flask_restful import Resource
from webargs.flaskparser import use_args

from helpers import UnableToCompleteError
from models import User, UserToken
from models.enums import TokenType
from services import AccountService

from .args import post_verify_email_args


class VerifyEmail(Resource):

    account_service = AccountService()

    @use_args(post_verify_email_args)
    def post(self, args):
        email = args['email']
        token = args['token']

        self.account_service.verify_email(email, token)

        return {'message': 'Done'}, 204
