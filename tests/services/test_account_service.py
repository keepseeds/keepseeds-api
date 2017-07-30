
import unittest
import pytest
import mock

from services.account_service import AccountService
from helpers import resource_exceptions as res_exc


class TestAccountService(unittest.TestCase):
    @mock.patch('services.account_service.User')
    @mock.patch('helpers.password_validator')
    def test__register__new_user(self, mock_password_validator, mock_user):
        """
        Should return the mocked token.
        """

        # Arrange
        mock_password_validator.return_value = True
        mock_user.find_by_email.return_value = None
        mock_user.create.return_value = 'test-token'

        # Act, Assert
        assert AccountService.register_user(
            email='test@test.com',
            first='Test',
            last='User',
            password='Testing1!',
            password_confirm='Testing1!') == 'test-token'

    @mock.patch('services.account_service.User')
    def test__register__existing_user(self, mock_user):
        """
        Should throw an EmailAlreadyExistsError
        """

        import models
        # Arrange
        mock_user.find_by_email.return_value = models.User(
            email='test@test.com',
            first='Test',
            last='User',
            password='Testing1!')

        # Act, Assert
        with pytest.raises(res_exc.EmailAlreadyExistsError):
            AccountService.register_user(
                email='test@test.com',
                first='Test',
                last='User',
                password='Testing1!',
                password_confirm='Testing1!')

        mock_user.find_by_email.assert_called_once_with('test@test.com')

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.UserToken')
    def test__verify_email__valid(self, user_token, user):
        """
        Should return True
        """
        mock_user = mock.MagicMock()
        mock_user.set_is_verified_email.return_value = True
        mock_user.id.return_value = 1
        user.find_by_email.return_value = mock_user

        mock_user_token = mock.MagicMock()
        mock_user_token.expire.return_value = True
        mock_user_token.verify_token.return_value = True
        user_token.find_by_user_and_type.return_value = mock_user_token

        assert AccountService.verify_email('test@test.com', 'test-token')

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.UserToken')
    def test__verify_email__invalid_token(self, user_token, user):
        """
        Should raise InvalidTokenError
        """
        mock_user = mock.MagicMock()
        mock_user.set_is_verified_email.return_value = True
        mock_user.id.return_value = 1
        user.find_by_email.return_value = mock_user

        mock_user_token = mock.MagicMock()
        mock_user_token.expire.return_value = True
        mock_user_token.verify_token.return_value = False
        user_token.find_by_user_and_type.return_value = mock_user_token

        with pytest.raises(res_exc.InvalidTokenError):
            AccountService.verify_email('test@test.com', 'test-token')

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.UserToken')
    def test__verify_email__user_update_fails(self, user_token, user):
        """
        Should raise UnableToCompleteError
        """
        mock_user = mock.MagicMock()
        mock_user.set_is_verified_email.return_value = False
        mock_user.id.return_value = 1
        user.find_by_email.return_value = mock_user

        mock_user_token = mock.MagicMock()
        mock_user_token.verify_token.return_value = True
        user_token.find_by_user_and_type.return_value = mock_user_token

        with pytest.raises(res_exc.UnableToCompleteError):
            AccountService.verify_email('test@test.com', 'test-token')

    @mock.patch('services.account_service.User')
    def test__verify_email__invalid_user(self, mock_user):
        """
        Should throw UserNotFoundError
        """

        # Arrange
        mock_user.find_by_email.return_value = None

        # Act, Assert
        with pytest.raises(res_exc.UserNotFoundError):
            AccountService.verify_email('test@test.com', 'test-token')

    @mock.patch('services.account_service.User')
    @mock.patch('helpers.password_validator')
    def test__change_password__valid(self, password_validator, user):
        """
        Should return True
        """
        mock_user = mock.MagicMock()
        mock_user.verify_password.return_value = True
        user.find_by_email.return_value = mock_user
        user.update_password.return_value = True

        password_validator.return_value = True

        assert AccountService.change_password(
            email='test@test.com',
            password='Password1!',
            password_confirm='Password1!',
            old_password='Password0!')

    @mock.patch('services.account_service.User')
    def test__change_password__invalid_email(self, user):
        """
        Should raise a UserNotFoundError
        """
        user.find_by_email.return_value = None

        with pytest.raises(res_exc.UserNotFoundError):
            AccountService.change_password(
                email='test@test.com',
                password='Password1!',
                password_confirm='Password1!',
                old_password='Password0!')

    @mock.patch('services.account_service.User')
    def test__change_password__bad_password(self, user):
        """
        Should raise an UnableToCompleteError
        """
        mock_user = mock.MagicMock()
        mock_user.verify_password.return_value = False
        user.find_by_email.return_value = mock_user

        with pytest.raises(res_exc.UnableToCompleteError):
            AccountService.change_password(
                email='test@test.com',
                password='Password1!',
                password_confirm='Password1!',
                old_password='Password0!')

    @mock.patch('services.account_service.User')
    def test__change_password__unable_to_update(self, user):
        """
        Should raise an UnableToCompleteError
        """
        mock_user = mock.MagicMock()
        mock_user.verify_password.return_value = True
        user.find_by_email.return_value = mock_user
        user.update_password.return_value = False

        with pytest.raises(res_exc.UnableToCompleteError):
            AccountService.change_password(
                email='test@test.com',
                password='Password1!',
                password_confirm='Password1!',
                old_password='Password0!')

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.Token')
    @mock.patch('services.account_service.UserToken')
    def test__request_password_reset__valid(self, user_token, token, user):
        """
        Should return True
        """
        mock_user = mock.MagicMock()
        user.find_by_email.return_value = mock_user

        mock_token = mock.MagicMock()
        token.find_by_token_type.return_value = mock_token

        user_token.create.return_value = 'test-token'

        assert AccountService.request_password_reset('test@test.com')['userTokenId'] == 'test-token'

    @mock.patch('services.account_service.User')
    def test__request_password_reset__invalid_email(self, user):
        """
        Should raise a UserNotFoundError
        """
        user.find_by_email.return_value = None

        with pytest.raises(res_exc.UserNotFoundError):
            AccountService.request_password_reset('test@test.com')

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.Token')
    def test__request_password_reset__invalid_token(self, token, user):
        """
        Should raise a UnableToCompleteError
        """
        mock_user = mock.MagicMock()
        user.find_by_email.return_value = mock_user

        token.find_by_token_type.return_value = None

        with pytest.raises(res_exc.UnableToCompleteError):
            AccountService.request_password_reset('test@test.com')

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

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.UserToken')
    @mock.patch('helpers.password_validator')
    def test__resolve_password_reset__valid(self, password_validator, user_token, user):
        """
        Should return True
        """
        mock_user = mock.MagicMock()
        mock_user.id = 1
        user.find_by_email.return_value = mock_user
        user.update_password.return_value = True

        mock_user_token = mock.MagicMock()
        mock_user_token.verify_token.return_value = True
        mock_user_token.expire.return_value = True
        user_token.find_by_user_and_type.return_value = mock_user_token

        password_validator.return_value = True

        assert AccountService.resolve_password_reset(
            email='test@test.com',
            password='Password1!',
            password_confirm='Password1!',
            token='test-token'
        )

    @mock.patch('services.account_service.User')
    @mock.patch('services.account_service.UserToken')
    @mock.patch('helpers.password_validator')
    def test__resolve_password_reset__update_password_fail(self, password_validator, user_token, user):
        """
        Should raise a UnableToCompleteError
        """
        mock_user = mock.MagicMock()
        mock_user.id = 1
        user.find_by_email.return_value = mock_user
        user.update_password.return_value = False

        mock_user_token = mock.MagicMock()
        mock_user_token.verify_token.return_value = True
        mock_user_token.expire.return_value = True
        user_token.find_by_user_and_type.return_value = mock_user_token

        password_validator.return_value = True

        with pytest.raises(res_exc.UnableToCompleteError):
            AccountService.resolve_password_reset(
                email='test@test.com',
                password='Password1!',
                password_confirm='Password1!',
                token='test-token'
            )

    @mock.patch("services.account_service.User")
    @mock.patch('services.account_service.UserToken')
    def test__resolve_password_reset__bad_password(self, user_token, user):
        """
        Should raise a UnableToCompleteError
        """
        mock_user = mock.MagicMock()
        mock_user.id = 1
        user.find_by_email.return_value = mock_user
        user.update_password.return_value = False

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
        mock_user = mock.MagicMock()
        mock_user.id = 1
        user.find_by_email.return_value = mock_user

        user_token.find_by_user_and_type.return_value = None

        with pytest.raises(res_exc.InvalidTokenError):
            AccountService.resolve_password_reset(
                email='test@test.com',
                password='Password1!',
                password_confirm='Password1!',
                token='test-token'
            )
        pass

    @mock.patch("services.account_service.User")
    def test__resolve_password_reset__bad_password(self, user):
        """
        Should raise a UserNotFoundError
        :param user:
        :return:
        """
        user.find_by_email.return_value = None

        with pytest.raises(res_exc.UserNotFoundError):
            AccountService.resolve_password_reset(
                email='test@test.com',
                password='Password1!',
                password_confirm='Password1!',
                token='test-token'
            )
        pass

