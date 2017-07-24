
from .mixins import BaseResponse


class DoneResponse(BaseResponse):
    def __init__(self, is_success=True):
        super(DoneResponse, self).__init__(is_success, 'Done.')
