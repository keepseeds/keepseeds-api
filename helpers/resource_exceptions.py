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
    """
    Base exception for resource errors.
    """
    def __init__(self, data={}):
        HTTPException.__init__(self)
        self.data = {'error_data': data}


class UnableToCompleteError(HTTPException):
    """
    Generic error message, no specific detail provided.
    """
    code = 422


class EmailAlreadyExistsError(ResourceError):
    """
    Error thrown when the provided email already exists.
    """
    code = 422

    def __init__(self, email):
        ResourceError.__init__(self, {'email': email})


class OAuthUserExistsError(EmailAlreadyExistsError):
    """
    Error thrown when the provided email already exists for an OAuth user.
    """
    code = 401

    def __init__(self, email):
        EmailAlreadyExistsError.__init__(self, email)


class UserNotFoundError(ResourceError):
    """
    Error thrown when the user could not be found.
    """
    code = 422

    def __init__(self):
        ResourceError.__init__(self)


class InvalidTokenError(ResourceError):
    """
    Error thrown when the provided token was not found.
    """
    code = 422

    def __init__(self, token):
        ResourceError.__init__(self, {'token': token})


class PasswordsDoNotMatchError(HTTPException):
    """
    Password comparison has failed.
    """
    code = 422


class UnmetPasswordRequirementsError(ResourceError):
    """
    The provided password and/plus confirmation are not eligible.
    """
    code = 422

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


class FacebookInvalidPermissionsError(ResourceError):
    """
    The facebook user has not provided adequate permissions to the app.
    """
    code = 401

    def __init__(self, data):
        ResourceError.__init__(self, data)


class ChildNotFoundError(ResourceError):
    """
    The child entity required could not be found.
    """
    code = 404

    def __init__(self, data):
        ResourceError.__init__(self, data)


class PermissionDeniedError(ResourceError):
    """
    The resource requested requires elevated permissions.
    """
    code = 401

    def __init__(self, action, target, identifier):
        ResourceError.__init__(self, {'action': action, 'target': target, 'id': identifier})


class GenderNotFoundError(ResourceError):
    """
    The provided gender ID does not exist.
    """
    code = 422

    def __init__(self, _id):
        ResourceError.__init__(self, {'id': _id})

#
# Dictionary of Exception Types
#

resource_errors = {
    'UnableToCompleteError': {
        'error_code': 'UNABLE_TO_COMPLETE',
        'message': 'Unable to complete the request.',
        'status': 422
    },
    'PasswordsDoNotMatchError': {
        'error_code': 'NO_PASSWORD_MATCH',
        'message': 'Passwords do not match.',
        'status': 422
    },
    'InvalidCredentialsError': {
        'error_code': 'INVALID_CREDENTIALS',
        'message': 'The provided credentials are not valid.',
        'status': 401
    },
    'UnmetPasswordRequirementsError': {
        'error_code': 'UNMET_PASSWORD_REQUIREMENTS',
        'message': 'The provided password and/or confirmation are not eligible.',
        'status': 422
    },
    'EmailAlreadyExistsError': {
        'error_code': 'EMAIL_ALREADY_EXISTS',
        'message': 'The provided email is already registered.',
        'status': 422
    },
    'OAuthUserExistsError': {
        'error_code': 'OAUTH_USER_EXISTS',
        'message': 'The provided credentials already belong to oauth user.',
        'status': 401
    },
    'UserNotFoundError': {
        'error_code': 'USER_NOT_FOUND',
        'message': 'Could not find the requested user.',
        'status': 422
    },
    'InvalidTokenError': {
        'error_code': 'INVALID_TOKEN',
        'message': 'Could not find the provided token.',
        'status': 422
    },
    'EmailNotVerifiedError': {
        'error_code': 'EMAIL_NOT_VERIFIED',
        'message': 'The provided email is not verified.',
        'status': 401
    },
    'FacebookInvalidPermissionsError': {
        'error_code': 'FACEBOOK_INVALID_PERMISSIONS',
        'message': 'The facebook user has not provided adequate permissions.',
        'status': 401
    },
    'ChildNotFoundError': {
        'error_code': 'CHILD_NOT_FOUND',
        'message': 'The child entity required could not be found.',
        'status': 404
    },
    'PermissionDeniedError': {
        'error_code': 'PERMISSION_DENIED',
        'message': 'The resource requested requires elevated permissions.',
        'status': 401
    },
    'GenderNotFoundError': {
        'error_code': 'GENDER_NOT_FOUND',
        'message': 'The provided gender ID does not exist.',
        'status': 422
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
    'FacebookInvalidPermissionsError',
    'OAuthUserExistsError',
    'GenderNotFoundError',
    'resource_errors'
]
