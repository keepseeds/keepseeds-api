
from db import db
from models import Child, UserChild
from helpers import resource_exceptions as res_exc
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

    @staticmethod
    def find_child(_id, user_id):
        child = Child.query\
            .filter_by(
                id=_id,
                delete_date_time=None
            ).first()  # type: Child

        if not child:
            raise res_exc.ChildNotFoundError({'id': _id})

        if not any(u for u in child.users if u.id == user_id):
            raise res_exc.PermissionDeniedError({'id': _id})

        return child

    @staticmethod
    def find_children(user_id):
        uc_result = UserChild.query.filter_by(user_id=user_id, delete_date_time=None).all()
        return [uc.child for uc in uc_result]
