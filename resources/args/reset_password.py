"""
Webarg definitions for reset_password_resource.
"""
from marshmallow.fields import Str

put_reset_password_args = {
    'email': Str(required=True)
}

post_reset_password_args = {
    'email': Str(required=True),
    'token': Str(required=True),
    'password': Str(required=True),
    'password_confirm': Str(required=True)
}
