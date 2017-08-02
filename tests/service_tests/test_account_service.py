"""
Tests relating to AccountService.
"""
import unittest
import pytest
import mock

from models.enums import TokenType
from services.account_service import AccountService
from helpers import resource_exceptions as res_exc


class TestAccountService(unittest.TestCase):
    @mock.patch('services.account_service.User')
    def test__register__new_user(self, user):
        """
        Should return the mocked token.
        """
        # Arrange
        user.find_by_email.return_value = None
        user.create.return_value = 'test-token'

        # Act
        result = AccountService.register_user(
            email='test@test.com',
            first='Test',
            last='User',
            password='Testing1!',
            password_confirm='Testing1!')

        # Assert
        assert result == 'test-token'
        user.find_by_email.assert_any_call('test@test.com')
        user.create('test@test.com', 'Test', 'User', 'Testing1!')

    @mock.patch('services.account_service.User')
    def test__register__existing_user(self, user):
        """
        Should throw an EmailAlreadyExistsError
        """
        # Arrange
        mock_user = mock.MagicMock()
        user.find_by_email.return_value = mock_user

        # Act
        with pytest.raises(res_exc.EmailAlreadyExistsError):
            AccountService.register_user(
                email='test@test.com',
                first='Test',
                last='User',
                password='Testing1!',
                password_confirm='Testing1!')

        # Assert
        user.find_by_email.assert_any_call('test@test.com')

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.UserToken')
    def test__verify_email__valid(self, user_token, user):
        """
        Should return True
        """
        # Arrange
        mock_user = mock.MagicMock()
        mock_user.set_is_verified_email.return_value = True
        mock_user.id.return_value = 1
        user.find_by_email.return_value = mock_user
        mock_user_token = mock.MagicMock()
        mock_user_token.expire.return_value = True
        mock_user_token.verify_token.return_value = True
        user_token.find_by_user_and_type.return_value = mock_user_token

        # Act
        result = AccountService.verify_email('test@test.com', 'test-token')

        # Assert
        assert result
        mock_user.set_is_verified_email.assert_any_call()
        user.find_by_email.assert_any_call('test@test.com')
        mock_user_token.expire.assert_any_call()
        mock_user_token.verify_token.assert_any_call('test-token')
        user_token.find_by_user_and_type.assert_any_call(
            user_id=mock_user.id,
            token_type=TokenType.VerifyEmail
        )

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.UserToken')
    def test__verify_email__invalid_token(self, user_token, user):
        """
        Should raise InvalidTokenError
        """
        # Arrange
        mock_user = mock.MagicMock()
        mock_user.id.return_value = 1
        user.find_by_email.return_value = mock_user
        mock_user_token = mock.MagicMock()
        mock_user_token.verify_token.return_value = False
        user_token.find_by_user_and_type.return_value = mock_user_token

        # Act
        with pytest.raises(res_exc.InvalidTokenError):
            AccountService.verify_email('test@test.com', 'test-token')

        # Assert
        user.find_by_email.assert_any_call('test@test.com')
        mock_user_token.verify_token.assert_any_call('test-token')
        user_token.find_by_user_and_type.assert_any_call(
            user_id=mock_user.id,
            token_type=TokenType.VerifyEmail
        )

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.UserToken')
    def test__verify_email__user_update_fails(self, user_token, user):
        """
        Should raise UnableToCompleteError
        """
        # Arrange
        mock_user = mock.MagicMock()
        mock_user.set_is_verified_email.return_value = False
        mock_user.id.return_value = 1
        user.find_by_email.return_value = mock_user
        mock_user_token = mock.MagicMock()
        mock_user_token.verify_token.return_value = True
        user_token.find_by_user_and_type.return_value = mock_user_token

        # Act
        with pytest.raises(res_exc.UnableToCompleteError):
            AccountService.verify_email('test@test.com', 'test-token')

        # Assert
        mock_user.set_is_verified_email.assert_any_call()
        user.find_by_email.assert_any_call('test@test.com')
        mock_user_token.verify_token.assert_any_call('test-token')
        user_token.find_by_user_and_type.assert_any_call(
            user_id=mock_user.id,
            token_type=TokenType.VerifyEmail
        )

    @mock.patch('services.account_service.User')
    def test__verify_email__invalid_user(self, mock_user):
        """
        Should throw UserNotFoundError
        """
        # Arrange
        mock_user.find_by_email.return_value = None

        # Act
        with pytest.raises(res_exc.UserNotFoundError):
            AccountService.verify_email('test@test.com', 'test-token')

        # Assert
        mock_user.find_by_email.assert_any_call('test@test.com')

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.get_jwt_identity')
    def test__change_password__valid(self, get_jwt_identity, user):
        """
        Should return True
        """
        # Arrange
        mock_user_id = 1
        get_jwt_identity.return_value = mock_user_id
        mock_user = mock.MagicMock()
        mock_user.email = 'test@test.com'
        mock_user.verify_password.return_value = True
        mock_user.update_password.return_value = True
        user.find_by_id.return_value = mock_user

        # Act
        assert AccountService.change_password(
            password='Password1!',
            password_confirm='Password1!',
            old_password='Password0!')

        # Assert
        mock_user.verify_password.assert_any_call('Password0!')
        mock_user.update_password.assert_any_call('Password1!')
        user.find_by_id.assert_any_call(mock_user_id)

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.get_jwt_identity')
    def test__change_password__invalid_email(self, get_jwt_identity, user):
        """
        Should raise a UserNotFoundError
        """
        # Arrange
        get_jwt_identity.return_value = 1
        user.find_by_id.return_value = None

        # Act
        with pytest.raises(res_exc.UserNotFoundError):
            AccountService.change_password(
                password='Password1!',
                password_confirm='Password1!',
                old_password='Password0!')

        # Assert
        get_jwt_identity.assert_any_call()
        user.find_by_id.assert_any_call(1)

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.get_jwt_identity')
    def test__change_password__bad_password(self, get_jwt_identity, user):
        """
        Should raise an UnableToCompleteError
        """
        # Arrange
        mock_user_id = 1
        get_jwt_identity.return_value = mock_user_id
        mock_user = mock.MagicMock()
        mock_user.verify_password.return_value = False
        user.find_by_id.return_value = mock_user

        # Act
        with pytest.raises(res_exc.UnableToCompleteError):
            AccountService.change_password(
                password='Password1!',
                password_confirm='Password1!',
                old_password='Password0!')

        # Assert
        get_jwt_identity.assert_any_call()
        mock_user.verify_password.assert_any_call('Password0!')
        user.find_by_id.assert_any_call(mock_user_id)

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.get_jwt_identity')
    def test__change_password__unable_to_update(self, get_jwt_identity, user):
        """
        Should raise an UnableToCompleteError
        """
        # Arrange
        mock_user_id = 1
        get_jwt_identity.return_value = mock_user_id
        mock_user = mock.MagicMock()
        mock_user.verify_password.return_value = True
        mock_user.update_password.return_value = False
        user.find_by_id.return_value = mock_user

        # Act
        with pytest.raises(res_exc.UnableToCompleteError):
            AccountService.change_password(
                password='Password1!',
                password_confirm='Password1!',
                old_password='Password0!')

        # Assert
        get_jwt_identity.assert_any_call()
        mock_user.verify_password.assert_any_call('Password0!')
        mock_user.update_password.assert_any_call('Password1!')
        user.find_by_id.assert_any_call(mock_user_id)

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.Token')
    @mock.patch('services.account_service.UserToken')
    def test__request_password_reset__valid(self, user_token, token, user):
        """
        Should return True
        """
        # Arrange
        mock_user = mock.MagicMock()
        user.find_by_email.return_value = mock_user
        mock_token = mock.MagicMock()
        token.find_by_token_type.return_value = mock_token
        user_token.create.return_value = 'test-token'

        # Act
        result = AccountService.request_password_reset('test@test.com')

        # Assert
        assert result['userTokenId'] == 'test-token'
        user.find_by_email.assert_any_call('test@test.com')
        token.find_by_token_type.assert_any_call(TokenType.ResetPassword)
        user_token.create.assert_any_call(mock_user, mock_token)

    @mock.patch('services.account_service.User')
    def test__request_password_reset__invalid_email(self, user):
        """
        Should raise a UserNotFoundError
        """
        # Arrange
        user.find_by_email.return_value = None

        # Act
        with pytest.raises(res_exc.UserNotFoundError):
            AccountService.request_password_reset('test@test.com')

        # Assert
        user.find_by_email.assert_any_call('test@test.com')

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.Token')
    def test__request_password_reset__invalid_token(self, token, user):
        """
        Should raise a UnableToCompleteError
        """
        # Arrange
        mock_user = mock.MagicMock()
        user.find_by_email.return_value = mock_user
        token.find_by_token_type.return_value = None

        # Act
        with pytest.raises(res_exc.UnableToCompleteError):
            AccountService.request_password_reset('test@test.com')

        # Assert
        user.find_by_email.assert_any_call('test@test.com')
        token.find_by_token_type.assert_any_call(TokenType.ResetPassword)

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.Token')
    @mock.patch('services.account_service.UserToken')
    def test__request_password_reset__create_token_failure(self, user_token, token, user):
        """
        Should raise an UnableToCompleteError
        """
        mock_user = mock.MagicMock()
        user.find_by_email.return_value = mock_user

        mock_token = mock.MagicMock()
        token.find_by_token_type.return_value = mock_token

        user_token.create.return_value = None

        with pytest.raises(res_exc.UnableToCompleteError):
            AccountService.request_password_reset('test@test.com')

        user.find_by_email.assert_any_call('test@test.com')
        token.find_by_token_type.assert_any_call(TokenType.ResetPassword)
        user_token.create.assert_any_call(mock_user, mock_token)

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.UserToken')
    def test__resolve_password_reset__valid(self, user_token, user):
        """
        Should return True
        """
        mock_user = mock.MagicMock()
        mock_user.id = 1
        mock_user.update_password.return_value = True
        user.find_by_email.return_value = mock_user

        mock_user_token = mock.MagicMock()
        mock_user_token.verify_token.return_value = True
        mock_user_token.expire.return_value = True
        user_token.find_by_user_and_type.return_value = mock_user_token

        assert AccountService.resolve_password_reset(
            email='test@test.com',
            password='Password1!',
            password_confirm='Password1!',
            token='test-token'
        )

        mock_user.update_password.assert_any_call('Password1!')
        user.find_by_email.assert_any_call('test@test.com')
        mock_user_token.verify_token.assert_any_call('test-token')
        mock_user_token.expire.assert_any_call()
        user_token.find_by_user_and_type.assert_any_call(
            user_id=mock_user.id,
            token_type=TokenType.ResetPassword)

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.UserToken')
    def test__resolve_password_reset__update_password_fail(self, user_token, user):
        """
        Should raise a UnableToCompleteError
        """
        mock_user = mock.MagicMock()
        mock_user.id = 1
        mock_user.update_password.return_value = False
        user.find_by_email.return_value = mock_user

        mock_user_token = mock.MagicMock()
        mock_user_token.verify_token.return_value = True
        user_token.find_by_user_and_type.return_value = mock_user_token

        with pytest.raises(res_exc.UnableToCompleteError):
            AccountService.resolve_password_reset(
                email='test@test.com',
                password='Password1!',
                password_confirm='Password1!',
                token='test-token'
            )

        mock_user.update_password.assert_any_call('Password1!')
        user.find_by_email.assert_any_call('test@test.com')
        mock_user_token.verify_token.assert_any_call('test-token')
        user_token.find_by_user_and_type.assert_any_call(
            user_id=mock_user.id,
            token_type=TokenType.ResetPassword
        )

    @mock.patch("services.account_service.User")
    @mock.patch('services.account_service.UserToken')
    def test__resolve_password_reset__bad_password(self, user_token, user):
        """
        Should raise a UnableToCompleteError
        """
        mock_user = mock.MagicMock()
        mock_user.id = 1
        mock_user.update_password.return_value = False
        user.find_by_email.return_value = mock_user

        mock_user_token = mock.MagicMock()
        mock_user_token.verify_token.return_value = True
        mock_user_token.expire.return_value = True
        user_token.find_by_user_and_type.return_value = mock_user_token

        with pytest.raises(res_exc.UnableToCompleteError):
            AccountService.resolve_password_reset(
                email='test@test.com',
                password='Password1!',
                password_confirm='Password1!',
                token='test-token'
            )
        pass

    @mock.patch("services.account_service.User")
    @mock.patch('services.account_service.UserToken')
    def test__resolve_password_reset__invalid_user_token(self, user_token, user):
        """
        Should raise a InvalidTokenError
        """
        mock_user = mock.MagicMock()
        mock_user.id = 1
        user.find_by_email.return_value = mock_user

        mock_user_token = mock.MagicMock()
        mock_user_token.verify_token.return_value = False
        mock_user_token.expire.return_value = True
        user_token.find_by_user_and_type.return_value = mock_user_token

        with pytest.raises(res_exc.InvalidTokenError):
            AccountService.resolve_password_reset(
                email='test@test.com',
                password='Password1!',
                password_confirm='Password1!',
                token='test-token'
            )
        pass

    @mock.patch("services.account_service.User")
    @mock.patch('services.account_service.UserToken')
    def test__resolve_password_reset__no_user_token(self, user_token, user):
        """
        Should raise a InvalidTokenError
        """
        # Arrange
        mock_user = mock.MagicMock()
        mock_user.id = 1
        user.find_by_email.return_value = mock_user
        user_token.find_by_user_and_type.return_value = None

        # Act
        with pytest.raises(res_exc.InvalidTokenError):
            AccountService.resolve_password_reset(
                email='test@test.com',
                password='Password1!',
                password_confirm='Password1!',
                token='test-token'
            )

        # Assert
        user.find_by_email.assert_any_call('test@test.com')
        user_token.find_by_user_and_type.assert_any_call(
            user_id=mock_user.id,
            token_type=TokenType.ResetPassword
        )

    @mock.patch("services.account_service.User")
    def test__resolve_password_reset__user_not_found(self, user):
        """
        Should raise a UserNotFoundError
        """
        # Arrange
        user.find_by_email.return_value = None

        # Act
        with pytest.raises(res_exc.UserNotFoundError):
            AccountService.resolve_password_reset(
                email='test@test.com',
                password='Password1!',
                password_confirm='Password1!',
                token='test-token'
            )

        # Assert
        user.find_by_email.assert_any_call('test@test.com')

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.get_access_token')
    def test__authenticate_user__valid(self, get_access_token, user):
        """
        """
        # Arrange
        mock_user = mock.MagicMock()
        mock_user.verify_password.return_value = True
        mock_user.is_verified_email = True
        mock_user.id = 1
        user.find_by_email.return_value = mock_user
        get_access_token.return_value = {'accessToken': 'test-token'}

        # Act
        result = AccountService.authenticate_user('test@test.com', 'Password1!')

        assert result['accessToken'] == 'test-token'
        get_access_token.assert_any_call(1)

    @mock.patch('services.account_service.User')
    def test__authenticate_user__no_user(self, user):
        """
        """
        # Arrange
        user.find_by_email.return_value = None

        # Act
        with pytest.raises(res_exc.InvalidCredentialsError):
            AccountService.authenticate_user('test@test.com', 'Password1!')

        user.find_by_email.assert_any_call('test@test.com')

    @mock.patch('services.account_service.User')
    def test__authenticate_user__not_validated(self, user):
        """
        """
        # Arrange
        mock_user = mock.MagicMock()
        mock_user.verify_password.return_value = True
        mock_user.is_verified_email = False
        mock_user.id = 1
        user.find_by_email.return_value = mock_user

        # Act
        with pytest.raises(res_exc.EmailNotVerifiedError):
            AccountService.authenticate_user('test@test.com', 'Password1!')

        user.find_by_email.assert_any_call('test@test.com')

    @mock.patch('services.account_service.Grant')
    def test__authenticate_oauth__invalid_grant(self, grant):
        grant.find_by_name.return_value = None

        with pytest.raises(res_exc.UnableToCompleteError):
            AccountService.authenticate_oauth('google', 'test-token')
