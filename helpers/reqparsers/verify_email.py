"""
Request parsers for VerifyEmail resource.
"""
from flask_restful import reqparse


def rp_post_verify_email():
    """
    [PUT] Verify Email Parser

    Fields: email, token
    """
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, type=str, help='Email is required.')
    parser.add_argument('token', required=True, type=str, help='Token is required.')

    return parser
