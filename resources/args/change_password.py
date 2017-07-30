"""
Webarg definitions for change_password_resource.
"""
from marshmallow.fields import Str

put_change_password_args = {
    'oldPassword': Str(required=True),
    'password': Str(required=True),
    'passwordConfirm': Str(required=True)
}
