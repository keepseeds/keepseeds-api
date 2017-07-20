"""
"""
import shortuuid
from db import db
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from models import User, Token
from helpers.utilities import ValidateTokenResponse
from .enums import TokenType
from .mixins import Base


class UserToken(db.Model, Base):
    """
    Represents the relationship between a user and the user's tokens.
    Examples of this relationship include Reset Password and Verify Email.
    """
    __tablename__ = 'user_tokens'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    token_id = db.Column(db.Integer, db.ForeignKey('tokens.id'))
    token_hash = db.Column(db.String(4000), unique=True, nullable=False)
    expires_date_time = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', back_populates='tokens')
    token = db.relationship('Token', back_populates='users')

    def __init__(self, user, token, expires_date_time=None):
        """
        :param user: User to add to this UserToken
        :type user: User
        :param token: Token to add to this UserToken
        :type token: Token
        :param expires_date_time: [Optional] When the UserToken should expire,
                                  defaults to 12 hours.
        :type expires_date_time: datetime
        """
        if expires_date_time is None:
            expires_date_time = datetime.utcnow() + timedelta(hours=12)

        self.user = user
        self.token = token
        self.expires_date_time = expires_date_time

    def generate_encrypt_token(self):
        """
        Generate a new token for this object and return the plain
        text version.

        :returns: [SENSITIVE] Plain text token.
        :rtype: str
        """
        token = shortuuid.ShortUUID().random(length=22)  # type: str

        self.token_hash = pbkdf2_sha256.hash(token)
        return token

    def verify_token(self, token):
        """
        Verify that the provided token matches the token_hash.
        :param token: Plain text string to validate against the token_hash
        :type token: str
        :return:
        :rtype: bool
        """
        return pbkdf2_sha256.verify(token, self.token_hash)

    def expire(self):
        """
        Set the delete_date_time of this UserToken.
        """
        self.delete_date_time = datetime.utcnow()
        db.session.commit()

    #
    # CLASS METHODS
    #

    @classmethod
    def validate_token(cls, user_id, token, token_type):
        """
        Look up user tokens for this user of the specific token_type
        and validate the provided token against it.

        :param user_id:
        :type user_id: int
        :param token:
        :type token: str
        :param token_type:
        :type token_type: TokenType
        :return:
        :rtype: ValidateTokenResponse
        """
        ut = cls.query.filter_by(user_id=user_id,
                                 delete_date_time=None,
                                 token_id=int(token_type))\
                      .filter(UserToken.expires_date_time > datetime.utcnow())\
                      .first()  # type: UserToken

        return ValidateTokenResponse(ut and ut.verify_token(token), ut)

    @classmethod
    def expire_existing_tokens(cls, user_id, token_id):
        """
        Retrieve existing tokens of the specified token_type for the provided
        user and call expire() on each.

        :param user_id: Expire tokens of token_type for this user.
        :type user_id: int
        :param token_id: Tokens of this type will be expired.
        :type token_id: int
        :return: Number of tokens expired.
        :rtype: int
        """
        existing_tokens = cls.query.filter_by(user_id=user_id,
                                              token_id=token_id,
                                              delete_date_time=None
                                              ).all()  # type: list[UserToken]

        remove_count = 0
        for token in existing_tokens:
            token.expire()
            remove_count += 1

        return remove_count

    @classmethod
    def create(cls, user, token, expires_date_time=None):
        """
        Create a new UserToken entry in to user_tokens for the provided
        user and token relationship.
        :param user: User to associate this UserToken with.
        :type user: User
        :param token: Token type to associate with this UserToken
        :type token: Token
        :param expires_date_time: [Optional] Expiry date of token.
        :type expires_date_time: datetime
        :rtype: str
        """
        new_user_token = cls(user, token, expires_date_time)
        token_value = new_user_token.generate_encrypt_token()

        cls.expire_existing_tokens(user.id, token.id)

        db.session.add(new_user_token)
        db.session.commit()

        return token_value
