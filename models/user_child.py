"""
Module for UserChild model.
"""
from db import db

from .mixins import Base


class UserChild(db.Model, Base):
    """
    Represents the children corresponding to users in the database.
    """

    # SQLAlchemy Configuration
    __tablename__ = 'child_users'

    is_primary = db.Column(db.Boolean, nullable=False)

    # Foreign Keys
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Entity Lookups
    user = db.relationship('User', back_populates='children')
    child = db.relationship('Child', back_populates='users')
