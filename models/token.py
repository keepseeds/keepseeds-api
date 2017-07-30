
from db import db
from .enums import TokenType
from .mixins import Base


class Token(db.Model, Base):
    """
    Database representation of a Token.
    """

    # SQLAlchemy Configuration
    __tablename__ = 'tokens'

    name = db.Column(db.String(100), nullable=False)
    users = db.relationship('UserToken', back_populates='token')

    def __init__(self, name):
        self.name = name

    @classmethod
    def find_by_token_type(cls, token_type):
        """
        Find a token using the provided TokenType.

        :param token_type: Type of token to
        :type token_type: TokenType
        :return:
        """
        return cls.query.filter_by(id=int(token_type)).first()
