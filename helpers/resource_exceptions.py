"""
Exceptions in this module relate to Resource errors.

Most commonly this will include exceptions to be thrown via Flask-RESTful
and should therefore be added to resource_errors.
"""
from flask_restful import HTTPException

#
# Custom Exception Types
#


class ResourceError(HTTPException):
    def __init__(self, data={}):
        HTTPException.__init__(self)
        self.data = {'error_data': data}


class UnableToCompleteError(HTTPException):
    """
    Generic error message, no specific detail provided.
    """
    code = 400


class EmailAlreadyExistsError(ResourceError):
    """
    Error thrown when the provided email already exists.
    """
    code = 400

    def __init__(self, email):
        ResourceError.__init__(self, {'email': email})


class UserNotFoundError(ResourceError):
    """
    Error thrown when the user could not be found.
    """
    code = 400

    def __init__(self):
        ResourceError.__init__(self)


class InvalidTokenError(ResourceError):
    """
    Error thrown when the provided token was not found.
    """
    code = 400

    def __init__(self, token):
        ResourceError.__init__(self, {'token': token})


class PasswordsDoNotMatchError(HTTPException):
    """
    Password comparison has failed.
    """
    code = 400


class UnmetPasswordRequirementsError(ResourceError):
    """
    The provided password and/plus confirmation are not eligible.
    """
    code = 400

    def __init__(self, data):
        ResourceError.__init__(self, data)


class InvalidCredentialsError(HTTPException):
    """
    Provided credentials are not valid.
    """
    code = 401


class EmailNotVerifiedError(ResourceError):
    """
    Provided email is not verified.
    """
    code = 401

    def __init__(self, email):
        ResourceError.__init__(self, {'email': email})

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
    },
    'EmailAlreadyExistsError': {
        'error_code': 'EMAIL_ALREADY_EXISTS',
        'message': 'The provided email is already registered.',
        'status': 400
    },
    'UserNotFoundError': {
        'error_code': 'USER_NOT_FOUND',
        'message': 'Could not find the requested user.',
        'status': 400
    },
    'InvalidTokenError': {
        'error_code': 'INVALID_TOKEN',
        'message': 'Could not find the provided token.',
        'status': 400
    },
    'EmailNotVerifiedError': {
        'error_code': 'EMAIL_NOT_VERIFIED',
        'message': 'The provided email is not verified.',
        'status': 401
    }
}


__all__ = [
    'UnableToCompleteError',
    'UnmetPasswordRequirementsError',
    'InvalidCredentialsError',
    'UserNotFoundError',
    'EmailAlreadyExistsError',
    'InvalidTokenError',
    'EmailNotVerifiedError',
    'resource_errors'
]
