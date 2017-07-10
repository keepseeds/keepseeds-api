"""
Module for the UserProviders class, this class interacts
with the database via SQLAlchemy.
"""
from sqlalchemy import String, Boolean, Column, Integer, DateTime, ForeignKey
from flask_sqlalchemy import Model
from models.mixins.base import Base

class UserProviders(Model, Base):
    """
    Database representation of the User's Providers
    """

    # SQLAlchemy Configuration
    __table__ = 'user_providers'

    user_id = Column(String(5000), ForeignKey('users.id'))
    provider_id = Column(Integer(), ForeignKey('providers.id'))
    provider_user_id = Column(Integer(), nullable=True)
    last_login = Column(DateTime())
