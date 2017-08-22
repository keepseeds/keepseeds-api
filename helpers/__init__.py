"""
Helper module containing generic useful classes and functions.
"""
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
    root = 'http://keepseeds.com' # TODO: Get from environ.
    return '{root}/{path}/{email}?token={token}'.format(
        root=root,
        path=path,
        email=email,
        token=token
    )
