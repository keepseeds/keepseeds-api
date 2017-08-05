import mock
import unittest

from models.enums import TokenType
from models.token import Token
from .helpers import filter_by_first_query


@mock.patch('models.token.db.Model', return_value=None)
@mock.patch('models.token.Base', return_value=None)
class TestToken(unittest.TestCase):

    def test__token__find_by_token_type(self, *args):
        # Arrange
        mock_token = mock.MagicMock()
        Token.query = filter_by_first_query(mock_token)

        # Act
        result = Token.find_by_token_type(TokenType.ResetPassword)

        # Assert
        assert result == mock_token
        Token.query.filter_by.assert_any_call(id=int(TokenType.ResetPassword))
        Token.query.filter_by.return_value.first.assert_any_call()
