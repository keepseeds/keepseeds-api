"""
Webarg definitions for change_password_resource.
"""
from marshmallow.fields import Str

put_change_password_args = {
    'old_password': Str(required=True),
    'password': Str(required=True),
    'password_confirm': Str(required=True)
}
