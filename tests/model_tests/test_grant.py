import mock
import unittest

from models.grant import Grant
from .helpers import filter_by_first_query



@mock.patch('models.grant.db.Model', return_value=None)
@mock.patch('models.grant.Base', return_value=None)
class TestGrant(unittest.TestCase):

    def test__grant__find_by_name(self, *args):
        mock_grant = mock.MagicMock()
        Grant.query = filter_by_first_query(mock_grant)

        # Act
        grant = Grant.find_by_name('facebook')

        # Assert
        assert grant == mock_grant, 'should return mock object'
        Grant.query.filter_by.assert_any_call(name='facebook',
                                              is_enabled=True,
                                              delete_date_time=None), 'should filter db'

        Grant.query.filter_by.return_value.first.assert_any_call(), 'should get the first entity'
