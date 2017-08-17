import unittest
import mock

from services.utils.oauth_utils import validate_oauth_token

@mock.patch('services.utils.oauth_utils.FacebookService')
class TestOAuthUtils(unittest.TestCase):

    def test__validate_oauth_token__facebook(self, facebook):
        """
        Should return dictionary of user details.
        """
        fb_result = {
            'id': 242142410,
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@user.com'
        }

        # Arrange
        facebook.get_user_details_by_token.return_value = fb_result

        # Act
        result = validate_oauth_token('facebook', 'test-token')

        # Assert
        assert result == fb_result, 'should return dictionary of user details'
        facebook.get_user_details_by_token.assert_any_call('test-token'), 'should call fb func'

    def test__validate_oauth_token__invalid_grant(self, facebook):
        """
        Should return False if grant is invalid.
        """
        facebook.get_user_details_by_token.return_value = None

        result = validate_oauth_token('nonsense-grant-type', 'test-token')

        assert not result, 'should return False for invalid token type'
        assert not facebook.get_user_details_by_token.called, 'should not hit fb func'
