"""
Exceptions in this module relate to Resource errors.

Most commonly this will include exceptions to be thrown via Flask-RESTful
and should therefore be added to resource_errors.
"""
from flask_restful import HTTPException

#
# Custom Exception Types
#

class UnableToCompleteError(HTTPException):
    """
    Generic error message, no specific detail provided.
    """
    code = 400


class PasswordsDoNotMatchError(HTTPException):
    """
    Password comparison has failed.
    """
    code = 400

class UnmetPasswordRequirementsError(HTTPException):
    """
    The provided password and/plus confirmation are not eligible.
    """
    code = 400

    def __init__(self, data):
        HTTPException.__init__(self)
        self.data = {'error_data': data}

class InvalidCredentialsError(HTTPException):
    """
    Provided credentials are not valid.
    """
    code = 401

#
# Dictionary of Exception Types
#

resource_errors = {
    'UnableToCompleteError': {
        'error_code': 'UNABLE_TO_COMPLETE',
        'message': 'Unable to complete the request.',
        'status': 400
    },
    'PasswordsDoNotMatchError': {
        'error_code': 'NO_PASSWORD_MATCH',
        'message': 'Passwords do not match.',
        'status': 400
    },
    'InvalidCredentialsError': {
        'error_code': 'INVALID_CREDENTIALS',
        'message': 'The provided credentials are not valid.',
        'status': 401
    },
    'UnmetPasswordRequirementsError': {
        'error_code': 'UNMET_PASSWORD_REQUIREMENTS',
        'message': 'The provided password and/or confirmation are not eligible.',
        'status': 400
    }
}
