from flask_restful import HTTPException

##
## Custom Exception Types
##

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

class InvalidCredentialsError(HTTPException):
    """
    Provided credentials are not valid.
    """
    code = 401

##
## Dictionary of Exception Types
##

resource_errors = {
    'UnableToCompleteError': {
        'message': 'Unable to complete the request.',
        'status': 400
    },
    'PasswordsDoNotMatchError': {
        'message': 'Passwords do not match.',
        'status': 400
    },
    'InvalidCredentialsError': {
        'message': 'The provided credentials are not valid.',
        'status': 401
    }
}
