
import unittest
import pytest

from helpers import resource_exceptions as res_exc

from services.utils.validate_password_utils import validate_password

class TestValidatePasswordUtils(unittest.TestCase):

    def test__validate_password__valid(self):
        result = validate_password('Password1!', 'Password1!')

        assert result

    def test__validate_password__length_error(self):
        with pytest.raises(res_exc.UnmetPasswordRequirementsError) as excinf:
            validate_password('P1!', 'P1!')

        assert get_exception_value(excinf, 'length_error')

    def test__validate_password__digit_error(self):
        with pytest.raises(res_exc.UnmetPasswordRequirementsError) as excinf:
            validate_password('Password!!', 'Password!!')

        assert get_exception_value(excinf, 'digit_error')

    def test__validate_password__uppercase_error(self):
        with pytest.raises(res_exc.UnmetPasswordRequirementsError) as excinf:
            validate_password('password1!', 'password1!')

        assert get_exception_value(excinf, 'uppercase_error')

    def test__validate_password__lowercase_error(self):
        with pytest.raises(res_exc.UnmetPasswordRequirementsError) as excinf:
            validate_password('PASSWORD1!', 'PASSWORD1!')

        assert get_exception_value(excinf, 'lowercase_error')

    def test__validate_password__symbol_error(self):
        with pytest.raises(res_exc.UnmetPasswordRequirementsError) as excinf:
            validate_password('Password11', 'Password11')

        assert get_exception_value(excinf, 'symbol_error')

    def test__validate_password__comparison_error(self):
        with pytest.raises(res_exc.UnmetPasswordRequirementsError) as excinf:
            validate_password('Password1!', 'Password2!')

        assert get_exception_value(excinf, 'comparison_error')


def get_exception_value(exc, value):
    return exc.value.data['error_data'][value]
