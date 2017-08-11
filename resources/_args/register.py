"""
Webarg definitions for register_resource.
"""
from marshmallow.fields import Str

post_register_args = {
    'first_name': Str(required=True),
    'last_name': Str(required=True),
    'email': Str(required=True),
    'password': Str(required=True),
    'password_confirm': Str(required=True)
}
