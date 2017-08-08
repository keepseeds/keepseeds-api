
from db import db
from models import Child
from .mixins import BaseService

class ChildService(BaseService):
    """
    Service for Child actions.
    """

    @classmethod
    def create(cls, first, last, dob, gender, middle):
        new_child = Child(first, last, dob, gender, middle)

        cls.add(new_child, True)

        return new_child
