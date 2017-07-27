
import mock
import pytest

from models import User
from services.account_service import AccountService
from helpers import EmailAlreadyExistsError, UserNotFoundError


@mock.patch('services.account_service.User')
@mock.patch('helpers.password_validator')
def test__register__new_user(mock_password_validator, mock_user):
    """
    Should return the mocked token.
    """

    # Arrange
    mock_password_validator.return_value = True
    mock_user.find_by_email.return_value = None
    mock_user.create.return_value = 'test-token'
    srv = AccountService()

    # Act, Assert
    assert srv.register_user(
        email='test@test.com',
        first='Test',
        last='User',
        password='Testing1!',
        password_confirm='Testing1!') == 'test-token'


@mock.patch('services.account_service.User')
def test__register__existing_user(mock_user):
    """
    Should throw an EmailAlreadyExistsError
    """

    # Arrange
    mock_user.find_by_email.return_value = User(
        email='test@test.com',
        first='Test',
        last='User',
        password='Testing1!')
    srv = AccountService()

    # Act, Assert
    with pytest.raises(EmailAlreadyExistsError):
        srv.register_user(None, None, None, None, None)


@mock.patch('services.account_service.User')
def test__verify_email__invalid_user(mock_user):
    """
    Should throw an Invalid
    """

    # Arrange
    mock_user.find_by_email.return_value = None
    srv = AccountService()

    # Act, Assert
    with pytest.raises(UserNotFoundError):
        srv.verify_email('test@test.com', 'test-token')
