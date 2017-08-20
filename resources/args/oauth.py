"""
Webarg definitions for oauth_resource.
"""
from marshmallow.fields import Str

get_oauth_args = {
    'token': Str(required=True)
}

post_oauth_args = {
    'grant_type': Str(required=True),
    'token': Str(required=True)
}
