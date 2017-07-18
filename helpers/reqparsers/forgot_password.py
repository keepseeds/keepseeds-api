from flask_restful import reqparse

def rp_put_forgot_password():
    """
    [PUT] Forgot Password Parser

    Fields: email
    """
    parser = reqparse.RequestParser()

    parser.add_argument('email', required=True, type=str, help='Email is required.')

    return parser

def rp_post_forgot_password():
    """
    [PUT] Forgot Password Parser

    Fields: email, token, password, passwordConfirm
    """
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, type=str, help='Email is required.')
    parser.add_argument('token', required=True, type=str, help='Token is required.')
    parser.add_argument('password', required=True, type=str, help='Password is required.')
    parser.add_argument('passwordConfirm', required=True, type=str, help='Password Confirmation is required.')

    return parser
