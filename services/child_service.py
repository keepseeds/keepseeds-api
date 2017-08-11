"""Module containing the ChildService definition."""

from db import db
from models import Child, UserChild
from helpers import resource_exceptions as res_exc
from .mixins import BaseService


class ChildService(BaseService):
    """
    Service for Child actions.
    """

    @classmethod
    def create(cls, first, last, dob, gender, created_by, middle):
        new_child = Child(first, last, dob, gender, created_by, middle)
        Child.add(new_child)
        return new_child

    @staticmethod
    def find_child(_id, user_id):
        """
        Provided with a child id and user id, find the child.
        """
        child = Child.query\
            .filter_by(
                id=_id,
                delete_date_time=None
            ).first()  # type: Child

        if not child:
            raise res_exc.ChildNotFoundError({'id': _id})

        if not any(u for u in child.users if u.user_id == user_id):
            raise res_exc.PermissionDeniedError({'id': _id})

        return child

    @staticmethod
    def find_users_children(user_id):
        """
        Provided with a user_id, look up the children either owned or granted
        access to.

        :param user_id: User's ID to query for children.
        :type user_id: int
        :rtype: dict
        """
        uc_result = UserChild.query\
            .filter_by(
                user_id=user_id,
                delete_date_time=None
            ).all()  # type: models.UserChild

        return {
            'owned': [uc.child for uc in uc_result if uc.is_primary],
            'included': [uc.child for uc in uc_result if not uc.is_primary]
        }
