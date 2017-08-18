import unittest
import mock
import pytest
import facebook
import yaml

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

no_email_permission_object = [{
    'data': {
        'user_id': 1425125215,
        'is_valid': True
    }
}, {
    'id': 1425125215,
    'first_name': 'Test',
    'last_name': 'User'
}]


def raise_graph_api_error(id, input_token):
    raise facebook.GraphAPIError(None)

def raise_yaml_error(input):
    raise yaml.YAMLError(None)

def os_get_environ(key, default):
    if key == 'FACEBOOK_APP_ID':
        return 'facebook-app-id'

    if key == 'FACEBOOK_APP_SECRET':
        return 'facebook-app-secret'

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

        # Act
        with pytest.raises(res_exc.InvalidCredentialsError):
            FacebookService.get_user_details_by_token('test-token')

        # Assert
        assert mock_get_object.has_any_call(
            'debug_token',
            input_token='test-token'),\
            'should debug the token'

    @mock.patch('services.facebook_service.FacebookService.get_graph')
    def test__get_user_details_by_token__graph_error(self, get_graph):
        """
        Should raise UnableToCompleteError when GraphAPI throws an error.
        """
        # Arrange
        mock_get_object = mock.MagicMock(side_effect=raise_graph_api_error)
        mock_graph = mock.MagicMock()
        mock_graph.get_object = mock_get_object
        get_graph.return_value = mock_graph

        # Act, Assert
        with pytest.raises(res_exc.UnableToCompleteError):
            FacebookService.get_user_details_by_token('test-token')

        assert mock_get_object.has_any_call('debug_token', input_token='test-token'),\
            'should debug the token'

    @mock.patch('services.facebook_service.FacebookService.get_graph')
    def test__get_user_details_by_token__no_email_permission(self, get_graph):
        mock_get_object = mock.MagicMock(side_effect=no_email_permission_object)
        mock_graph = mock.MagicMock()
        mock_graph.get_object = mock_get_object
        get_graph.return_value = mock_graph

        # Act, Assert
        with pytest.raises(res_exc.FacebookInvalidPermissionsError):
            FacebookService.get_user_details_by_token('test-token')

        assert mock_get_object.has_any_call('debug_token', input_token='test-token')
        assert mock_get_object.has_any_call(id=1425125215,fields='first_name,last_name,email')

    @mock.patch('services.facebook_service.os.environ.get', side_effect=os_get_environ)
    @mock.patch('services.facebook_service.facebook.GraphAPI', return_value='graph-api')
    def test__get_graph__environ_variables(self, graph_api, get):

        result = FacebookService.get_graph()

        assert result == 'graph-api'
        assert graph_api.has_any_call(
            access_token='facebook-app-id|facebook-app-secret',
            timeout=1000,
            version='2.7')
        assert get.has_any_call('FACEBOOK_APP_ID', None)
        assert get.has_any_call('FACEBOOK_APP_SECRET', None)

    @mock.patch('services.facebook_service.os.environ.get', return_value=None)
    @mock.patch('services.facebook_service.facebook.GraphAPI', return_value='graph-api')
    def test__get_graph__from_config(self, graph_api, get):
        """
        Test call from config.
        """
        result = FacebookService.get_graph()

        assert result == 'graph-api'
        assert graph_api.has_any_call(
            access_token='facebook-app-id|facebook-app-secret',
            timeout=1000,
            version='2.7')
        assert get.has_any_call('FACEBOOK_APP_ID', None)
        assert get.has_any_call('FACEBOOK_APP_SECRET', None)

    @mock.patch('services.facebook_service.os.environ.get', return_value=None)
    @mock.patch('services.facebook_service.facebook.GraphAPI', return_value='graph-api')
    @mock.patch('services.facebook_service.yaml.load', side_effect=raise_yaml_error)
    def test__get_graph__from_config_error(self, load, graph_api, get):
        """
        Test call from config throws error
        """
        with pytest.raises(res_exc.UnableToCompleteError):
            result = FacebookService.get_graph()

        assert not graph_api.called
        assert get.has_any_call('FACEBOOK_APP_ID', None)
        assert get.has_any_call('FACEBOOK_APP_SECRET', None)
        assert load.has_any_call(mock.ANY)
