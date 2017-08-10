"""
Module for the TokenType enumeration.
"""
from enum import IntEnum


class TokenType(IntEnum):
    """
    Enumeration on Token types.
    """
    ResetPassword = 1
    VerifyEmail = 2
