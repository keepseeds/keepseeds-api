import unittest
import mock
import pytest
import facebook

from helpers import resource_exceptions as res_exc
from services import FacebookService

success_get_object = [{
    'data': {
        'user_id': 1425125215,
        'is_valid': True
    }
}, {
    'id': 1425125215,
    'first_name': 'Test',
    'last_name': 'User',
    'email': 'test@user.com'
}]

invalid_debug_object = [{
    'data': {
        'is_valid': False
    }
}]

def raise_graph_api_error(id, input_token):
    raise facebook.GraphAPIError(None)

class TestFacebookService(unittest.TestCase):

    @mock.patch('services.facebook_service.FacebookService.get_graph')
    def test__get_user_details_by_token__valid(self, get_graph):
        """
        Should return the users details.
        """
        # Arrange
        mock_get_object = mock.MagicMock(side_effect=success_get_object)
        mock_graph = mock.MagicMock()
        mock_graph.get_object = mock_get_object
        get_graph.return_value = mock_graph

        # Act
        result = FacebookService.get_user_details_by_token('test-token')

        # Assert
        assert result == {
            'id': 1425125215,
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@user.com'
        },\
        'should return the user details.'

        assert mock_get_object.has_any_call(
            'debug_token',
            input_token='test-token'),\
            'should debug the token'
        assert mock_get_object.has_any_call(
            id=1425125215,
            fields='first_name,last_name,email'),\
            'should get the details for the user id'

    @mock.patch('services.facebook_service.FacebookService.get_graph')
    def test__get_user_details_by_token__invalid_token(self, get_graph):
        """
        Should debug the token but raise error.
        """
        # Arrange
        mock_get_object = mock.MagicMock(side_effect=invalid_debug_object)
        mock_graph = mock.MagicMock()
        mock_graph.get_object = mock_get_object
        get_graph.return_value = mock_graph

        with pytest.raises(res_exc.InvalidCredentialsError):
            FacebookService.get_user_details_by_token('test-token')

        assert mock_get_object.has_any_call(
            'debug_token',
            input_token='test-token'),\
            'should debug the token'

    @mock.patch('services.facebook_service.FacebookService.get_graph')
    def test__get_user_details_by_token__graph_error(self, get_graph):
        # Arrange
        mock_get_object = mock.MagicMock(side_effect=raise_graph_api_error)
        mock_graph = mock.MagicMock()
        mock_graph.get_object = mock_get_object
        get_graph.return_value = mock_graph

        with pytest.raises(res_exc.UnableToCompleteError):
            FacebookService.get_user_details_by_token('test-token')
