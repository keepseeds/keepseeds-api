import unittest
import mock
import pytest

from datetime import datetime

from helpers import resource_exceptions as res_exc
from services.child_service import ChildService


class TestChildService(unittest.TestCase):

    @mock.patch('services.child_service.User')
    @mock.patch('services.child_service.Gender')
    @mock.patch('services.child_service.Child')
    @mock.patch('services.child_service.UserChild')
    def test__create__valid(self, user_child, child, gender, user):
        """
        Test create call as expected.
        """
        # Arrange
        mock_user = mock.MagicMock()
        user.find_by_id.return_value = mock_user

        gender.find_by_id.return_value = mock.MagicMock()

        mock_child = mock.MagicMock()
        child.create.return_value = mock_child

        mock_user_child = mock.MagicMock()
        user_child.create.return_value = mock_user_child

        dob = datetime.utcnow()

        # Act
        result = ChildService.create('first', 'last', dob, 1, 1)

        # Assign
        assert result == mock_child
        assert user.find_by_id.has_any_call(1)
        assert gender.find_by_id.has_any_call(1)
        assert child.create.has_any_call('first', 'last', dob, 1, 1, None)
        assert user_child.create.has_any_call(mock_user, mock_child, True)

    @mock.patch('services.child_service.User')
    @mock.patch('services.child_service.Gender')
    @mock.patch('services.child_service.Child')
    @mock.patch('services.child_service.UserChild')
    def test__create__no_user_child(self, user_child, child, gender, user):
        """
        Test create call as expected.
        """
        # Arrange
        mock_user = mock.MagicMock()
        user.find_by_id.return_value = mock_user

        gender.find_by_id.return_value = mock.MagicMock()

        mock_child = mock.MagicMock()
        child.create.return_value = mock_child

        mock_user_child = None
        user_child.create.return_value = mock_user_child

        dob = datetime.utcnow()

        # Act
        with pytest.raises(res_exc.UnableToCompleteError):
            ChildService.create('first', 'last', dob, 1, 1)

        # Assign
        assert user.find_by_id.has_any_call(1)
        assert gender.find_by_id.has_any_call(1)
        assert child.create.has_any_call('first', 'last', dob, 1, 1, None)
        assert user_child.create.has_any_call(mock_user, mock_child, True)

    @mock.patch('services.child_service.User')
    @mock.patch('services.child_service.Gender')
    def test__create__no_gender_found(self, gender, user):
        """
        Test create call as expected.
        """
        # Arrange
        mock_user = mock.MagicMock()
        user.find_by_id.return_value = mock_user

        gender.find_by_id.return_value = None

        dob = datetime.utcnow()

        # Act
        with pytest.raises(res_exc.GenderNotFoundError):
            ChildService.create('first', 'last', dob, 1, 1)

        # Assign
        assert user.find_by_id.has_any_call(1)
        assert gender.find_by_id.has_any_call(1)

    @mock.patch('services.child_service.User')
    def test__create__no_user_found(self, user):
        """
        Test create call as expected.
        """
        # Arrange
        user.find_by_id.return_value = None

        dob = datetime.utcnow()

        # Act
        with pytest.raises(res_exc.UserNotFoundError):
            ChildService.create('first', 'last', dob, 1, 1)

        # Assign
        assert user.find_by_id.has_any_call(1)

    @mock.patch('services.child_service.ChildService.find_child')
    def test__delete_child__valid(self, find_child):
        """
        Test delete_child call as expected.
        """
        # Arrange
        mock_child = mock.MagicMock()
        mock_child.created_by = 1
        mock_child.soft_delete.return_value = None
        mock_child.delete_date_time = datetime.utcnow()
        find_child.return_value = mock_child

        # Act
        result = ChildService.delete_child(1, 1)

        # Assert
        assert result
        assert find_child.has_any_call(1, 1)
        assert mock_child.soft_delete.has_any_call()

    @mock.patch('services.child_service.ChildService.find_child')
    def test__delete_child__wrong_user(self, find_child):
        """
        Test delete_child call as expected.
        """
        # Arrange
        mock_child = mock.MagicMock()
        mock_child.created_by = 1
        mock_child.soft_delete.return_value = None
        mock_child.delete_date_time = datetime.utcnow()
        find_child.return_value = mock_child

        # Act
        with pytest.raises(res_exc.PermissionDeniedError):
            ChildService.delete_child(1, 2)

        # Assert
        assert find_child.has_any_call(1, 2)
        assert not mock_child.soft_delete.called
