"""
Request parsers for OAuth resource.
"""
from flask_restful import reqparse


def rp_put_change_password():
    """
    [PUT] Change Password Parser

    Fields: email, oldPassword, password, passwordConfirm
    """
    parser = reqparse.RequestParser()

    parser.add_argument('email', required=True, type=str, help='Email is required.')
    parser.add_argument('oldPassword', required=True, type=str, help='Old Password is required.')
    parser.add_argument('password', required=True, type=str, help='Password is required.')
    parser.add_argument('passwordConfirm', required=True, type=str, help='Password Confirm is required.')

    return parser
