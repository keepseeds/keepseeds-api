"""
Request parsers for Register resource.
"""
from flask_restful import reqparse

def rp_post_register():
    """
    [POST] Register Parser

    Fields: firstName, lastName, email, password, passwordConfirm
    """
    parser = reqparse.RequestParser()
    parser.add_argument('firstName',
                        type=str,
                        required=True,
                        help='First Name is required.')
    parser.add_argument('lastName',
                        type=str,
                        required=True,
                        help='Last Name is required.')
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help='Email is required.')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='Password is required.')
    parser.add_argument('passwordConfirm',
                        type=str,
                        required=True,
                        help='Confirm Password is required.')
    return parser
