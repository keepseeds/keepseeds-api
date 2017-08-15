"""
Helper module containing generic useful classes and functions.
"""
from .resource_exceptions import *


def data_info_helper(action, target, _id):
    return {
        'action': action,
        'target': target,
        'id': _id
    }
