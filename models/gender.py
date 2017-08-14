"""
Module for Gender model.
"""
from db import db
from .mixins import Base


class Gender(db.Model, Base):

    __tablename__ = 'genders'

    name = db.Column(db.String(100), nullable=False)
    is_enabled = db.Column(db.Boolean, nullable=False)

    @classmethod
    def find_by_id(cls, gender_id):
        return cls.query.filter_by(
            id=gender_id,
            delete_date_time=None,
            is_enabled=True).first()
