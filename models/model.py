"""
Module for the User class, this class interacts
with the database via SQLAlchemy.
"""
from db import db
from passlib.hash import pbkdf2_sha256

from models.mixins import Base

# http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-object

class UserGrant(db.Model, Base):
    __tablename__ = 'user_grants'

    uid = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    grant_id = db.Column(db.Integer, db.ForeignKey('grants.id'), primary_key=True)

    user = db.relationship('User', back_populates='users')
    grant = db.relationship('Grant', back_populates='grants')

class UserToken(db.Model, Base):
    __tablename__ = 'user_tokens'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    token_id = db.Column(db.Integer, db.ForeignKey('tokens.id'))
    token_value = db.Column(db.String(100), unique=True, nullable=False)
    expires_date_time = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', back_populates='users')
    token = db.relationship('Token', back_populates='tokens')

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

    grants = db.relationship(
        'Grant',
        secondary=user_grants,
        back_populates='users'
    )

    tokens = db.relationship(
        'Token',
        secondary=user_tokens,
        back_populates='users'
    )

    user_grants = db.relationship('UserGrant', back_populates='user')
    user_tokens = db.relationship('UserToken', back_populates='user')

    def __init__(self, email, first, last, password):
        self.email = email
        self.first_name = first
        self.last_name = last
        self.is_verified_email = False
        self.is_locked = False
        self.encrypt_password(password)

    def encrypt_password(self, password):
        """
        Provided with a password, set the password_hash.
        """
        self.password_hash = pbkdf2_sha256.hash(password)
        return self.password_hash

    def verify_password(self, password):
        """
        Provided with a password, verify the password_hash of this user.
        """
        return pbkdf2_sha256.verify(password, self.password_hash)

    def set_is_locked(self, is_locked=True):
        """
        Set the user's locked state.
        """
        self.is_locked = is_locked
        db.session.commit()

    @classmethod
    def find_by_email(cls, email, is_locked=False, delete_date_time=None):
        """
        Find a single User based on email address.
        """
        res = cls.query;
        res.filter_by(email=email,
                      is_locked=is_locked,
                      delete_date_time=delete_date_time)

        return res.first()

    @classmethod
    def find_by_id(cls, _id, is_locked=False, delete_date_time=None):
        """
        Find a single User based on id.
        """
        return cls.query.filter_by(id=_id,
                                   is_locked=is_locked,
                                   delete_date_time=delete_date_time).first()

    @classmethod
    def create(cls, email, first, last, password):
        """
        Create a new user in the database using the provided values.
        """
        new_user = cls(email, first, last, password)
        db.session.add(new_user)
        db.session.commit()

        return new_user.id

    @classmethod
    def update_password(cls, email, password):
        """
        Update password of user with provided email.
        """
        user = cls.find_by_email(email)

        if not user:
            return False

        user.encrypt_password(password)
        db.session.commit()
        
        return True


class Grant(db.Model, Base):
    """
    Database representation of a Grant.
    """

    # SQLAlchemy Configuration
    __tablename__ = 'grants'

    name = db.Column(db.String(100), nullable=False)
    users = db.relationship('User',
                            secondary=user_grants,
                            back_populates='grants')

    user_grants = db.relationship('UserGrant', back_populates='grant')


class Token(db.Model, Base):
    """
    Database representation of a Token.
    """

    # SQLAlchemy Configuration
    __tablename__ = 'tokens'

    name = db.Column(db.String(100), nullable=False)

    user_tokens = db.relationship('UserToken', back_populates='token')
