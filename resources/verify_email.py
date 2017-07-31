
from flask_restful import Resource
from webargs.flaskparser import use_args

from services import AccountService
from .args import post_verify_email_args


class VerifyEmail(Resource):

    @use_args(post_verify_email_args)
    def post(self, args):
        email = args['email']
        token = args['token']

        AccountService.verify_email(email, token)

        return {'message': 'Done'}, 204
