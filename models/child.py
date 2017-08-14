"""
Module for Child model.
"""
from db import db
from .mixins import Base


class Child(db.Model, Base):
    """
    Represents a Child in the database.
    """

    # SQLAlchemy Configuration
    __tablename__ = "children"

    first_name = db.Column(db.String(300), nullable=False)
    middle_name = db.Column(db.String(300))
    last_name = db.Column(db.String(300), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)

    # Foreign Keys
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    gender_id = db.Column(db.ForeignKey('genders.id'))

    # Entity Lookups
    users = db.relationship('UserChild', back_populates='child')
    gender = db.relationship('Gender')

    def __init__(self, first_name, last_name, date_of_birth, gender_id, created_by, middle_name=None):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender_id = gender_id
        self.created_by = created_by
        self.middle_name = middle_name

    @classmethod
    def create(cls, first, last, dob, gender_id, created_by, middle_name=None):
        new_child = cls(first, last, dob, gender_id, created_by, middle_name)
        cls.add(new_child)

        return new_child
