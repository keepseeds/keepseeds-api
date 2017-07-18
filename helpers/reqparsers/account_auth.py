"""
Request parsers for AccountAuthentication resource.
"""
from flask_restful import reqparse

def rp_post_account_authentication():
    """
    [POST] Account Authentication Parser

    Fields: email, password
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

    return parser
