"""
Module containing all resource endpoint webargs definitions.
"""
from .account_auth import post_account_auth_args
from .change_password import put_change_password_args
from .oauth import post_oauth_args
from .register import post_register_args
from .reset_password import post_reset_password_args, put_reset_password_args
from .verify_email import post_verify_email_args
