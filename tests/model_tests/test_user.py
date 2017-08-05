import mock
import unittest

from models.enums import TokenType
from models.user import User


@mock.patch('models.user.db.Model', return_value=None)
@mock.patch('models.user.Base', return_value=None)
@mock.patch('models.user.pbkdf2_sha256')
class TestUser(unittest.TestCase):
    
    def test__user__encrypt_password(self, pbkdf2_sha256, *args):
        # Arrange
        pbkdf2_sha256.hash.return_value = 'test-hash'
        user = User('test@test.com', 'Test', 'User')
        assert user.password_hash is None

        # Act
        user.encrypt_password('Password1!')

        # Assert
        assert user.password_hash, 'should not be None'
        assert user.password_hash != 'Password1!', 'should not be the input password'
        pbkdf2_sha256.hash.assert_any_call('Password1!'), 'should have called the hash function'

    def test__user__validate_password(self, pbkdf2_sha256, *args):
        # Arrange
        pbkdf2_sha256.hash.return_value = 'test-hash'
        pbkdf2_sha256.verify.return_value = True
        user = User('test@test.com', 'Test', 'User', 'Password1!')

        # Act
        result = user.verify_password('Password1!')

        # Assert
        assert result, 'should not be None'
        pbkdf2_sha256.verify.assert_any_call('Password1!', 'test-hash'), 'should set password to hash result'

    @mock.patch('models.user.db.session.commit', return_value=None)
    def test__user__set_is_locked(self, *args):
        # Arrange
        user = User('test@test.com', 'Test', 'User')

        # Act
        user.set_is_locked()

        # Assert
        assert user.is_locked, 'should be locked'

    @mock.patch('models.user.db.session.commit', return_value=None)
    def test__user__set_is_locked_false(self, *args):
        # Arrange
        user = User('test@test.com', 'Test', 'User')
        user.is_locked = True

        # Act
        user.set_is_locked(False)

        # Assert
        assert not user.is_locked, 'should not be locked'

    @mock.patch('models.user.db.session.commit', return_value=None)
    def test__user__update_password(self, commit, pbkdf2_sha256, *args):
        # Arrange
        pbkdf2_sha256.hash.return_value = 'test-hash-one'
        user = User('test@test.com', 'Test', 'User', 'Password1!')
        initial_hash = user.password_hash
        pbkdf2_sha256.hash.return_value = 'test-hash-two'

        # Act
        result = user.update_password('Password2!'), "should return True"

        # Assert
        assert result, "should not be None"
        assert initial_hash != user.password_hash, "hashes must be different"
        pbkdf2_sha256.hash.assert_any_call('Password1!'), "must be called with initial pw"
        pbkdf2_sha256.hash.assert_any_call('Password2!'), "must be called with update pw"
        commit.assert_any_call(), "must be called to save changes to db"

    @mock.patch('models.user.db.session.commit', return_value=None)
    def test__user__set_is_verified_email(self, commit, *args):
        user = User('test@test.com', 'Test', 'User')
        assert not user.is_verified_email

        # Act
        user.set_is_verified_email()

        assert user.is_verified_email
        commit.assert_any_call()

    @mock.patch('models.user.db.session.commit', return_value=None)
    def test__user__set_is_verified_email_false(self, commit, *args):
        user = User('test@test.com', 'Test', 'User')
        user.is_verified_email = True
        assert user.is_verified_email

        # Act
        user.set_is_verified_email(False)

        # Assert
        assert not user.is_verified_email
        commit.assert_any_call()

    def test__user__find_by_email(self, *args):
        # Arrange
        mock_user = mock.MagicMock()
        mock_user.email = 'test@test.com'
        mock_query = mock.MagicMock()
        mock_query.first.return_value = mock_user
        User.query = mock.MagicMock()
        User.query.filter_by.return_value = mock_query

        # Act
        result = User.find_by_email('test@test.com')

        # Assert
        assert result, "should not be None"
        User.query.filter_by.assert_any_call(
            email='test@test.com',
            is_locked=False,
            delete_date_time=None), "should call filter_by"
        mock_query.first.assert_any_call(), "should return first"

    def test__user__find_by_id(self, *args):
        # Arrange
        mock_user = mock.MagicMock()
        mock_user.email = 'test@test.com'
        mock_query = mock.MagicMock()
        mock_query.first.return_value = mock_user
        User.query = mock.MagicMock()
        User.query.filter_by.return_value = mock_query

        # Act
        result = User.find_by_id(1)

        # Assert
        assert result, "should return not None"
        User.query.filter_by.assert_any_call(
            id=1,
            is_locked=False,
            delete_date_time=None), "should call db query"

        mock_query.first.assert_any_call(), "should retrieve first"

    @mock.patch('models.user.db.session.commit', return_value=None)
    @mock.patch('models.user.db.session.add', return_value=None)
    @mock.patch('models.user.Token')
    @mock.patch('models.user.UserToken')
    def test__user__create(self, user_token, token, *args):
        # Arrange
        mock_token = mock.MagicMock()
        token.find_by_token_type.return_value = mock_token
        user_token.create.return_value = 'test-token'

        # Act
        verify_token = User.create('test@test.com', 'Test', 'User', 'Password1!')

        # Assert
        assert verify_token['token'] == 'test-token', "should return provided token"
        token.find_by_token_type.assert_any_call(TokenType.VerifyEmail), "should look up token type"
        user_token.create.assert_any_call(mock.ANY, mock_token, mock.ANY), "should create a new UserToken"

    @mock.patch('models.user.db.session.commit', return_value=None)
    @mock.patch('models.user.db.session.add', return_value=None)
    def test__user__create_oauth(self, add, commit, *args):
        # Arrange

        # Act
        new_user = User.create_oauth('test@test.com', 'Test', 'User')

        # Assert
        assert new_user
        add.assert_any_call(mock.ANY), 'should call add with object'
        commit.assert_any_call(), 'should call commit'
