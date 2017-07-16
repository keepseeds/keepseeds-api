"""
Module for the User class, this class interacts
with the database via SQLAlchemy.
"""
# from db import db
# from models.mixins.base import Base
# from models.user_grant import user_grants
# from passlib.hash import pbkdf2_sha256
# 
# class User(db.Model, Base):
#     """
#     Represents a User in the database.
#     """
# 
#     # SQLAlchemy Configuration
#     __tablename__ = "users"
# 
#     email = db.Column(db.String(300), unique=True)
#     first_name = db.Column(db.String(100))
#     last_name = db.Column(db.String(100))
#     password_hash = db.Column(db.String(4000))
#     is_verified_email = db.Column(db.Boolean())
# 
#     grants = db.relationship(
#         'Grant',
#         secondary=user_grants,
#         back_populates='users'
#     )
#     def encrypt_password(self, password):
#        """
#        Provided with a password, set the password_hash.
#        """
#        self.password_hash = pbkdf2_sha256.hash(password)
#        return self.password_hash
#
#    def verify_password(self, password):
#        """
#        Provided with a password, verify the password_hash of this user.
#        """
#        return pbkdf2_sha256.verify(password, self.password_hash)
#
#    @classmethod
#    def find_by_email(cls, email):
#        """
#        Find a single User based on email address.
#        """
#        print(cls)
#        print(cls.query)
#        return cls.query.filter_by(email=email).first()
#
#    @classmethod
#    def find_by_id(cls, _id):
#        """
#        Find a single User based on id.
#        """
#        return cls.query.filter_by(id=_id).first()
