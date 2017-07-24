class BaseResponse(object):
    def __init__(self, is_success=True, message=None):
        self.is_success = is_success
        self.message = message

    def json(self):
        return {
            'isSuccess': self.is_success,
            'message': self.message
        }