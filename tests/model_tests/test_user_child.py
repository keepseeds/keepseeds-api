import mock
import unittest

from models.user_child import UserChild


class TestUserChild(unittest.TestCase):
    @mock.patch('models.child.db.session.commit', return_value=None)
    @mock.patch('models.child.db.session.add', return_value=None)
    def test__user_child__create(self, add, commit, *args):
        mock_user = mock.MagicMock()
        mock_child = mock.MagicMock()

        # Act
        new_user_child = UserChild.create(mock_user, mock_child, True)

        # Assert
        assert new_user_child
        add.assert_any_call(mock.ANY)
        commit.assert_any_call()
