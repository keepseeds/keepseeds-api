"""
Webarg definitions for oauth_resource.
"""
from marshmallow.fields import Str

post_oauth_args = {
    'grantType': Str(required=True),
    'token': Str(required=True)
}
