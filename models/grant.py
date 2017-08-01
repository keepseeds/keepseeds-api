"""
Module for the Grant class, this class interacts
with the database via SQLAlchemy.
"""
from db import db

from .mixins import Base


class Grant(db.Model, Base):
    """
    Database representation of a Grant.
    """

    # SQLAlchemy Configuration
    __tablename__ = 'grants'

    name = db.Column(db.String(100), nullable=False)
    is_enabled = db.Column(db.Boolean, nullable=False)

    users = db.relationship('UserGrant', back_populates='grant')

    @classmethod
    def find_by_name(cls, grant_name, is_enabled=True, delete_date_time=None):
        """
        Find the type of grant based on the name.
        """
        return cls.query.filter_by(
            name=grant_name,
            is_enabled=is_enabled,
            delete_date_time=delete_date_time
        ).first()
