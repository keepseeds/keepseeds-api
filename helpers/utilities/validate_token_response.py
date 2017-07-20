

class ValidateTokenResponse(object):
    def __init__(self, is_valid, user_token):
        self.is_valid = is_valid
        self.user_token = user_token
