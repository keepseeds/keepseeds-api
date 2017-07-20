"""
"""
import shortuuid
from db import db
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from models import User, Token
from helpers.utilities import ValidateTokenResponse
from enums import TokenType
from .mixins import Base


class UserToken(db.Model, Base):
    """
    """
    __tablename__ = 'user_tokens'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    token_id = db.Column(db.Integer, db.ForeignKey('tokens.id'))
    token_hash = db.Column(db.String(4000), unique=True, nullable=False)
    expires_date_time = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', back_populates='tokens')
    token = db.relationship('Token', back_populates='users')

    def __init__(self, user, token, expires_date_time=None):
        if expires_date_time is None:
            expires_date_time = datetime.utcnow() + timedelta(hours=12)

        self.user = user
        self.token = token
        self.expires_date_time = expires_date_time

    def generate_encrypt_token(self):
        """
        Generate a new token for this object and return the plain text version.
        :returns: [SENSITIVE] Plain text token.
        :rtype str
        """
        token = shortuuid.ShortUUID().random(length=22)

        self.token_hash = pbkdf2_sha256.hash(token)
        return token

    def verify_token(self, token):
        return pbkdf2_sha256.verify(token, self.token_hash)

    def expire(self):
        self.delete_date_time = datetime.utcnow()
        db.session.commit()

    @classmethod
    def validate_token(cls, user_id, token):
        """

        :param user_id:
        :type user_id: int
        :param token:
        :type token: str
        :return:
        :rtype: ValidateTokenResponse
        """
        ut = cls.query.filter_by(user_id=user_id,
                                 delete_date_time=None,
                                 token_id=int(TokenType.ResetPassword))\
                      .filter(UserToken.expires_date_time > datetime.utcnow())\
                      .first()

        return ValidateTokenResponse(ut and ut.verify_token(token), ut)

    @classmethod
    def create(cls, user, token, expires_date_time=None):
        """

        :param user:
        :type user: User
        :param token:
        :type token: Token
        :param expires_date_time:
        :type expires_date_time: datetime
        :rtype: str
        """
        new_user_token = cls(user, token, expires_date_time)
        token_value = new_user_token.generate_encrypt_token()

        db.session.add(new_user_token)
        db.session.commit()

        return token_value
