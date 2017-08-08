"""
Module containing all RESTful API Resources.
"""
# Security / Generic resources
from .change_password_resource import ChangePassword
from .reset_password_resource import ResetPassword
from .register_resource import Register
from .account_auth_resource import AccountAuth
from .oauth_resource import OAuth
from .verify_email import VerifyEmail

# Collection Entity resources
from .children_resource import ChildrenResource

# Single Entity resources
from .single import ChildResource
