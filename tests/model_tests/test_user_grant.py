import mock
import unittest

from models.user_grant import UserGrant
from .helpers import filter_by_first_query


@mock.patch('models.user_grant.db.Model', return_value=None)
@mock.patch('models.user_grant.Base', return_value=None)
class TestUserGrant(unittest.TestCase):

    def test__user_grant__find_by_uid(self, *args):
        # Arrange
        mock_user_grant = mock.MagicMock()
        UserGrant.query = filter_by_first_query(mock_user_grant)

        # Act
        result = UserGrant.find_by_uid(1, 'test-uid')

        # Assert
        assert result == mock_user_grant
        UserGrant.query.filter_by.return_value.first.assert_any_call()
        UserGrant.query.filter_by.assert_any_call(grant_id=1, uid='test-uid')

    @mock.patch('models.user_grant.db.session.commit', return_value=None)
    @mock.patch('models.user_grant.db.session.add', return_value=None)
    def test__user_grant__create(self, add, commit, *args):
        # Arrange
        mock_user = mock.MagicMock()
        mock_grant = mock.MagicMock()

        # Act
        UserGrant.create(mock_user, mock_grant, 'test-uid')

        # Assert
        add.assert_any_call(mock.ANY)
        commit.assert_any_call()
