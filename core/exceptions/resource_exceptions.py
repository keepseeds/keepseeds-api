class UnableToCompleteError(Exception):
    """
    Generic error message, no specific detail provided.
    """
    code = 400

class PasswordsDoNotMatchError(Exception):
    """
    Password comparison has failed.
    """
    code = 400

class InvalidCredentialsError(Exception):
    """
    Provided credentials are not valid.
    """
    code = 401

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
