"""
Module for the User class, this class interacts
with the database via SQLAlchemy.
"""
from db import db
from sqlalchemy import String, Boolean, Column
from flask_sqlalchemy import Model
from models.mixins.base import Base
from passlib.hash import pbkdf2_sha256

class User(Model, Base):
    """
    Represents a User in the database.
    """

    # SQLAlchemy Configuration
    __table__ = "users"

    email = Column(String(300), unique=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    password_hash = Column(String(4000))
    is_verified_email = Column(Boolean)

    grants = db.relationship('UserGrant', backref='users', lazy='dynamic')

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

    @classmethod
    def find_by_email(cls, email):
        """
        Find a single User based on email address.
        """
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        """
        Find a single User based on id.
        """
        return cls.query.filter_by(id=_id).first()
