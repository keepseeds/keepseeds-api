import mock
import unittest
import datetime

from models.child import Child

@mock.patch('models.user.db.Model', return_value=None)
@mock.patch('models.user.Base', return_value=None)
class TestChild(unittest.TestCase):

    @mock.patch('models.child.db.session.commit', return_value=None)
    @mock.patch('models.child.db.session.add', return_value=None)
    def test__child__create(self, add, commit, *args):

        new_child = Child.create('Test', 'Child', datetime.datetime, 1, 1, None)

        assert new_child
        add.assert_any_call(mock.ANY)
        commit.assert_any_call()
