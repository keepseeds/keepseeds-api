
import re
from werkzeug.security import safe_str_cmp
from helpers.errors import UnmetPasswordRequirementsError

def validate_password(password, password_confirm):
    """
    Validate the provided password, optional password_confirm to
    ensure password is entered correctly twice.
    """
    RE_SYMBOL = r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]'

    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(RE_SYMBOL, password) is None
    comparison_error = (
        password_confirm
        and not safe_str_cmp(password, password_confirm)
    )

    is_password_valid = not (
        length_error or
        digit_error or
        uppercase_error or
        lowercase_error or
        symbol_error or
        comparison_error
    )

    if not is_password_valid:
        data = {
            'length_error': length_error,
            'digit_error': digit_error,
            'uppercase_error': uppercase_error,
            'lower_error': lowercase_error,
            'symbol_error': symbol_error,
            'comparison_error': comparison_error
        }
        raise UnmetPasswordRequirementsError(data)

    return True
