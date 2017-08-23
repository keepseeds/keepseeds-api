"""
Helper module containing generic useful classes and functions.
"""
import base64
import urllib
from flask_restful import marshal
from .resource_exceptions import *


def marshal_collection(collection, fields):
    """
    Marshal a collection using the system default envelope.

    :type collection: Any
    :type fields: {items}
    :rtype: Union[OrderedDict, list]
    """
    return marshal(collection, fields, envelope='data')

def get_token_url(path, email, token):
    """
    Get website URL for token.
    """
    payload = get_email_token_payload(email, token)
    root = 'http://keepseeds.com' # TODO: Get from environ.
    return '{root}/{path}/{payload}'.format(
        root=root,
        path=path,
        payload=payload
    )

def get_email_token_payload(email, token):
    """
    Provided with an email and token, generate payload.
    """
    json_string = '{{ "email": "{email}", "token": "{token}" }}'.format(
        email=email,
        token=token
    )
    base_payload = base64.b64encode(json_string)
    return urllib.quote(base_payload)
