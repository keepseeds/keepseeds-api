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
