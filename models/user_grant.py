"""
Module for the UserProvider class, this class interacts
with the database via SQLAlchemy.
"""
from db import db
from sqlalchemy import String, Column, Integer, DateTime, ForeignKey
from flask_sqlalchemy import Model
from models.mixins.base import Base

class UserGrant(Model, Base):
    """
    Database representation of the User's Grants
    """

    # SQLAlchemy Configuration
    __table__ = 'user_grants'

    user_id = Column(String(5000), ForeignKey('users.id'))
    grant_id = Column(Integer(), ForeignKey('grants.id'))
    grant_user_id = Column(Integer(), nullable=False)
    last_login = Column(DateTime())

    grant = db.relationship('Grant')
    user = db.relationship('User')

    @classmethod
    def find_by_details(cls, grant_id, grant_user_id):
        cls.query.filter_by(grant_id=grant_id,
                            grant_user_id=grant_user_id).first()
