import mock
import unittest
import datetime

from models.enums import TokenType
from models.user_token import UserToken
from .helpers import filter_by_filter_first_query, filter_by_filter_all_query


@mock.patch('models.user_token.db.Model', return_value=None)
@mock.patch('models.user_token.Base', return_value=None)
class TestUserToken(unittest.TestCase):

    @mock.patch('models.user_token.shortuuid')
    @mock.patch('models.user_token.pbkdf2_sha256')
    def test__user_token__generate_encrypt_token(self, pbkdf2_sha256, shortuuid, *args):
        # Arrange
        mock_user = mock.MagicMock()
        mock_token = mock.MagicMock()
        mock_shortuuid = mock.MagicMock()
        mock_shortuuid.random.return_value = 'this_is_a_test_short_uuid'
        shortuuid.ShortUUID.return_value = mock_shortuuid
        pbkdf2_sha256.hash.return_value = 'this_is_a_test_hash_token'
        user_token = UserToken(mock_user, mock_token)

        # Act
        result = user_token.generate_encrypt_token()

        # Assert
        assert result == 'this_is_a_test_short_uuid', 'should return the uuid'
        mock_shortuuid.random.assert_any_call(length=22), 'should be called with length 22 for security reasons'
        shortuuid.ShortUUID.assert_any_call(), 'should call shortuuid library'
        pbkdf2_sha256.hash.assert_any_call('this_is_a_test_short_uuid'), 'should be called to encrypt uuid'

    @mock.patch('models.user_token.pbkdf2_sha256')
    def test__user_token__verify_token(self, pbkdf2_sha256, *args):
        # Arrange
        mock_user = mock.MagicMock()
        mock_token = mock.MagicMock()
        pbkdf2_sha256.verify.return_value = True
        user_token = UserToken(mock_user, mock_token)
        user_token.token_hash = 'token-hash'

        # Act
        result = user_token.verify_token('test-token')

        # Assert
        assert result, 'should return True'
        pbkdf2_sha256.verify.assert_any_call('test-token', 'token-hash'), 'should verify with pbkdf2_sha256'

    @mock.patch('models.user_token.db.session.commit')
    def test__user_token__expire(self, commit, *args):
        # Arrange
        mock_user = mock.MagicMock()
        mock_token = mock.MagicMock()
        commit.return_value = None
        expires_date_time = datetime.datetime.utcnow() + datetime.timedelta(hours=12)
        user_token = UserToken(mock_user, mock_token, expires_date_time)

        assert user_token.expires_date_time == expires_date_time, 'should expire at the datetime provided'
        assert not user_token.delete_date_time, 'should not have delete_date_time set'

        # Act
        user_token.expire()

        # Assert
        assert user_token.delete_date_time, 'should set delete_date_time after expire() is called'

    def test__user_token__find_by_user_and_type(self, *args):
        # Arrange
        mock_user_token = mock.MagicMock()
        UserToken.query = filter_by_filter_first_query(mock_user_token)

        # Act
        result = UserToken.find_by_user_and_type(1, TokenType.VerifyEmail)

        # Assert
        assert result == mock_user_token
        UserToken.query.filter_by.return_value.filter.return_value.first.assert_any_call()
        UserToken.query.filter_by.return_value.filter.assert_any_call(mock.ANY)
        UserToken.query.filter_by.assert_any_call(user_id=1,
                                                  delete_date_time=None,
                                                  token_id=int(TokenType.VerifyEmail))

    def test__user_token__expire_existing_tokens(self, *args):
        first_token = mock.MagicMock()
        first_token.expire.return_value = None
        second_token = mock.MagicMock()
        second_token.expire.return_value = None

        UserToken.query = filter_by_filter_all_query([first_token, second_token])

        # Act
        count = UserToken.expire_existing_tokens(2, 1, 1)

        # Assert
        filter_by_part = UserToken.query.filter_by
        filter_part = filter_by_part.return_value.filter
        all_part = filter_part.return_value.all

        assert count == 2, 'should iterate over both tokens'
        first_token.expire.assert_any_call(), 'should expire the first token'
        second_token.expire.assert_any_call(), 'should expire the second token'
        all_part.assert_any_call(), 'should query a collection'
        filter_part.assert_any_call(mock.ANY), 'should filter'
        filter_by_part.assert_any_call(user_id=2,
                                       token_id=1,
                                       delete_date_time=None), 'should filter by'

    @mock.patch('models.user_token.UserToken.generate_encrypt_token')
    @mock.patch('models.user_token.db.session.add', return_value=None)
    @mock.patch('models.user_token.db.session.commit', return_value=None)
    @mock.patch('models.user_token.UserToken.expire_existing_tokens', return_value=None)
    def test__user_token__create(self, expire_existing_tokens, commit, add, generate_encrypt_token, *args):
        # Arrange
        generate_encrypt_token.return_value = 'test-token'
        mock_user = mock.MagicMock()
        mock_user.id = 1
        mock_token = mock.MagicMock()
        mock_token.id = 2
        expires_date_time = datetime.datetime.utcnow() + datetime.timedelta(hours=12)

        # Act
        token_value = UserToken.create(mock_user, mock_token, expires_date_time)

        # Assert
        assert token_value == 'test-token', 'token should match generate_encrypt_token'

        generate_encrypt_token.assert_any_call(), 'should call generate_encrypt_token'
        add.assert_any_call(mock.ANY), 'should add to db'
        commit.assert_any_call(), 'should commit change to db'
        expire_existing_tokens.assert_any_call(1, 2, None), 'should expire existing'
