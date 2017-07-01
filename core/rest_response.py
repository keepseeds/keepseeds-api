"""
Utility module to structure responses from the API.
"""

class RestResponse(object):
    def __init__(self, code, message, detail, data, is_success):
        self.code = code
        self.message = message
        self.detail = detail
        self.data = data
        self.is_success = is_success

    def json(self):
        """
        Return a dictionary respresentation of the RestResponse
        """
        response = dict()

        if self.code:
            response['code'] = self.code

        if self.message:
            response['message'] = self.message

        if self.detail:
            response['detail'] = self.detail

        if self.is_success is not None:
            response['isSuccess'] = self.is_success

        if self.data:
            response['data'] = self.data

        if self.code is not None:
            return response, self.code

        return response

class SuccessResponse(RestResponse):
    def __init__(self, data):
        RestResponse.__init__(200, None, None, data, True)

class NotFoundResponse(RestResponse):
    def __init__(self):
        RestResponse.__init__(
            404,
            'Unable to find requested resource',
            'The requested resource could not be found. Please check endpoint.',
            None,
            False
        )
