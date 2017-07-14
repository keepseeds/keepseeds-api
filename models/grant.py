"""
Module for the Grant class, this class interacts
with the database via SQLAlchemy.
"""
from db import db
from sqlalchemy import String, Column
from flask_sqlalchemy import Model
from models.mixins.base import Base

class Grant(Model, Base):
    """
    Database representation of a Grant.
    """

    # SQLAlchemy Configuration
    __table__ = 'grants'
    name = Column(String(100), nullable=False)
    user_grants = db.relationship('UserGrant', backref='grants',
                                  lazy='dynamic')
