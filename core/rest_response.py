"""
Utility module to structure responses from the API.
"""

class RestResponse(object):
    """ Base class for a RESTful response. """
    def __init__(self, code, message, detail, data, is_success):
        self.code = code # Status code for the response
        self.message = message # Succinct message describing the response
        self.detail = detail # A more descriptive message of the response
        self.data = data # Payload relating to this response
        self.is_success = is_success # Is this response considered `expected`?

    def json(self):
        """ Return a dictionary representation of the RestResponse """
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
    """ Represents a 200 - Success response. """
    def __init__(self, data):
        RestResponse.__init__(200, None, None, data, True)

class NotFoundResponse(RestResponse):
    """ Represents a 404 - Not Found response. """
    def __init__(self):
        RestResponse.__init__(
            404,
            'Unable to find requested resource',
            'The requested resource could not be found. Please check endpoint.',
            None,
            False
        )
