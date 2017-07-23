"""
Module for all request parser functions.

Naming pattern: rp_[METHOD]_[RESOURCE]
"""
from .account_auth import rp_post_account_authentication
from .oauth import rp_post_oauth
from .change_password import rp_put_change_password
from .reset_password import rp_post_reset_password, rp_put_reset_password
from .register import rp_post_register
from .verify_email import rp_post_verify_email
