"""
Module for all request parser functions.

Naming pattern: rp_[METHOD]_[RESOURCE]
"""
from helpers.reqparsers.account_auth import rp_post_account_authentication
from helpers.reqparsers.oauth import rp_post_oauth
from helpers.reqparsers.change_password import rp_put_change_password
from helpers.reqparsers.forgot_password import rp_post_forgot_password, rp_put_forgot_password
from helpers.reqparsers.register import rp_post_register
