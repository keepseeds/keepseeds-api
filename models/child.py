from db import db
from .mixins import Base

class Child(db.Model, Base):
    """
    Represents a Child in the database.
    """

    # SQLAlchemy Configuration
    __tablename__ = "children"

    first_name = db.Column(db.String(300))
    middle_name = db.Column(db.String(300))
    last_name = db.Column(db.String(300))
    date_of_birth = db.Column(db.DateTime)
    gender = db.Column(db.Integer)

    def __init__(self, first_name, last_name, date_of_birth, gender, middle_name=None):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.middle_name = middle_name
