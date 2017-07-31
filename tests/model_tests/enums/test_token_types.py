from models.enums import TokenType


def test__types__exist():
    assert 'VerifyEmail' in TokenType.__members__
    assert 'ResetPassword' in TokenType.__members__
