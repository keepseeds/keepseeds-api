"""
Module for the User class, this class interacts
with the database via SQLAlchemy.
"""
from datetime import datetime, timedelta
from db import db
from passlib.hash import pbkdf2_sha256

from .mixins import Base
from .enums import TokenType
from .user_token import UserToken
from .token import Token


class User(db.Model, Base):
    """
    Represents a User in the database.
    """

    # SQLAlchemy Configuration
    __tablename__ = "users"

    email = db.Column(db.String(300), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password_hash = db.Column(db.String(4000))
    is_verified_email = db.Column(db.Boolean)
    is_locked = db.Column(db.Boolean)

    grants = db.relationship('UserGrant', back_populates='user')
    tokens = db.relationship('UserToken', back_populates='user')

    def __init__(self, email, first, last, password):
        """
        :param email: Email address of user, should be unique.
        :type email: str
        :param first: First name of user.
        :type first: str
        :param last: Last name of user.
        :type last: str
        :param password: Password of user, to be converted in to hash.
        :type password: str
        """
        self.email = email
        self.first_name = first
        self.last_name = last
        self.is_verified_email = False
        self.is_locked = False
        self.encrypt_password(password)

    def encrypt_password(self, password):
        """
        Provided with a password, set the password_hash.

        :param password: Password to set as password_hash.
        :type password: str

        :rtype str
        """
        self.password_hash = pbkdf2_sha256.hash(password)
        return self.password_hash

    def verify_password(self, password):
        """
        Provided with a password, verify the password_hash of this user.

        :param password: Password to validate against the db hash.
        :type password: str
        :rtype bool
        """
        return pbkdf2_sha256.verify(password, self.password_hash)

    def set_is_locked(self, is_locked=True):
        """
        Set the user's locked state.

        :param is_locked: Requested value of this users is_locked property.
        :type is_locked: bool

        :rtype None
        """
        self.is_locked = is_locked
        db.session.commit()

    def set_is_verified_email(self, is_verified_email=True):
        """
        Set the user's verified email state.
        :param is_verified_email:
        :return:
        """
        self.is_verified_email = is_verified_email
        db.session.commit()

        return True

    @classmethod
    def find_by_email(cls, email, is_locked=False, delete_date_time=None):
        """
        Find a single User based on email address.

        :param email: User's email to find in database.
        :type email: str

        :param is_locked: Whether to return locked or unlocked accounts.
        :type is_locked: bool

        :param delete_date_time: Date at which the user has been deleted.
        :type delete_date_time: datetime

        :rtype: User
        """
        res = cls.query.filter_by(email=email,
                   is_locked=is_locked,
                   delete_date_time=delete_date_time)

        return res.first()

    @classmethod
    def find_by_id(cls, _id, is_locked=False, delete_date_time=None):
        """
        Find a single User based on id.
        :param _id:
        :type _id: int

        :param is_locked:
        :type is_locked: bool

        :param delete_date_time:
        :type delete_date_time: datetime

        :rtype User
        """
        return cls.query.filter_by(id=_id,
                                   is_locked=is_locked,
                                   delete_date_time=delete_date_time).first()

    @classmethod
    def create(cls, email, first, last, password):
        """
        Create a new user in the database using the provided values.

        :param email: Email address to assign to new user, should be unique.
        :type email: str

        :param first: First name of new user.
        :type first: str

        :param last: Last name of new user.
        :type last: str

        :param password: Password to assign to user.
        :type password: str

        :rtype: dict
        """
        new_user = cls(email, first, last, password)
        db.session.add(new_user)
        db.session.commit()

        token = Token.find_by_token_type(TokenType.VerifyEmail)
        token_expiry = datetime.utcnow() + timedelta(hours=72)

        verify_email_token = UserToken.create(new_user, token, token_expiry)

        return {"userId": new_user.id, "token": verify_email_token}

    @classmethod
    def update_password(cls, email, password):
        """

        :param email: Email address of user to update.
        :type email: str
        :param password: New password to set for user.
        :type password: str
        :rtype bool
        """
        user = cls.find_by_email(email)

        if not user:
            return False

        user.encrypt_password(password)
        db.session.commit()

        return True
