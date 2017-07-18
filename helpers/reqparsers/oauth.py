"""
Request parsers for OAuth resource.
"""

from flask_restful import reqparse

def rp_post_oauth():
    """
    [POST] OAuth Authentication Parser

    Fields: grantType, token
    """
    parser = reqparse.RequestParser()
    parser.add_argument('grantType',
                        required=True,
                        type=str,
                        help='Grant Type is required.')
    parser.add_argument('token',
                        required=True,
                        type=str,
                        help='Token is required.')
    return parser
