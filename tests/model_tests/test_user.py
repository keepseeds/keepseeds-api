import mock
import unittest
import pytest
from werkzeug.security import safe_str_cmp

from models.user import User

@mock.patch('models.user.db.Model', return_value=None)
@mock.patch('models.user.Base', return_value=None)
@mock.patch('models.user.pbkdf2_sha256')
class TestUser(unittest.TestCase):
    
    def test__user__encrypt_password(self, pbkdf2_sha256, base, model):
        pbkdf2_sha256.hash.return_value = 'test-hash'
        user = User('test@test.com', 'Test', 'User')
        assert user.password_hash is None
        user.encrypt_password('Password1!')

        assert user.password_hash is not None
        assert user.password_hash != 'Password1!'
        pbkdf2_sha256.hash.assert_any_call('Password1!')

    def test__user__validate_password(self, pbkdf2_sha256, base, model):
        pbkdf2_sha256.hash.return_value = 'test-hash'
        pbkdf2_sha256.verify.return_value = True
        user = User('test@test.com', 'Test', 'User')
        user.encrypt_password('Password1!')

        assert user.verify_password('Password1!')
        pbkdf2_sha256.verify.assert_any_call('Password1!', 'test-hash')

    @mock.patch('models.user.db.session.commit', return_value=None)
    def test__user__set_is_locked(self, commit, pbkdf2_sha256, base, model):
        user = User('test@test.com', 'Test', 'User')
        user.is_locked = False
        assert not user.is_locked

        user.set_is_locked()
        assert user.is_locked

    @mock.patch('models.user.db.session.commit', return_value=None)
    def test__user__set_is_locked_false(self, commit, pbkdf2_sha256, base, model):
        user = User('test@test.com', 'Test', 'User')
        user.set_is_locked(False)

        assert not user.is_locked
