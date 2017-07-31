"""
Test class for access_token_utils
"""
import unittest
import mock

from services.utils.access_token_utils import get_access_token

class TestAccessTokenUtils(unittest.TestCase):

    @mock.patch('services.utils.access_token_utils.create_access_token')
    def test__get_access_token__valid(self, create_access_token):
        create_access_token.return_value = 'test-token'
        result = get_access_token(1)

        assert result['accessToken'] == 'test-token'
