"""Module containing the ChildService definition."""

from models import Child, UserChild, User, Gender
from helpers import resource_exceptions as res_exc
from .mixins import BaseService


class ChildService(BaseService):
    """
    Service for Child actions.
    """

    @staticmethod
    def create(first, last, dob, gender_id, created_by, middle=None):
        """
        Add a new child.

        :param first: First name of child.
        :type first: str
        :param last: Last name of child.
        :type last: str
        :param dob: Date of Birth of child.
        :type dob: datetime.datetime
        :param gender_id: Gender of child.
        :type gender_id: int
        :param created_by: User ID of creating user.
        :type created_by: int
        :param middle: [Optional] Middle name of user.
        :type middle: Optional[str]
        :return:
        """
        # Check created_by user is valid.
        user = User.find_by_id(created_by)
        if not user:
            raise res_exc.UserNotFoundError

        # Check gender provided is valid.
        gender = Gender.find_by_id(gender_id)
        if not gender:
            raise res_exc.GenderNotFoundError(gender_id)

        # Create new child
        new_child = Child.create(first, last, dob, gender_id, created_by, middle)

        # Create ChildUser entity using user and child objects, is_primary=True
        new_uc = UserChild.create(user, new_child, True)

        if not new_uc:
            raise res_exc.UnableToCompleteError

        return new_child

    @classmethod
    def delete_child(cls, identifier, user_id):
        """
        Provided with a child id and user id, mark the child as deleted.

        :param identifier:
        :param user_id:
        :return:
        """
        child = cls.find_child(identifier, user_id)

        if not child.created_by == user_id:
            raise res_exc.PermissionDeniedError('delete', 'child', identifier)

        child.soft_delete()

        return child.delete_date_time is not None

    @staticmethod
    def find_child(identifier, user_id):
        """
        Provided with a child id and user id, find the child.

        :param identifier: ID of child.
        :type identifier: int
        :param user_id: ID of User.
        :type user_id: int
        :rtype: Child
        """
        child = Child.find_by_id(identifier)

        if not child:
            raise res_exc.ChildNotFoundError({'id': identifier})

        if not any(u for u in child.users if u.user_id == user_id):
            raise res_exc.PermissionDeniedError('find', 'child', identifier)

        return child

    @staticmethod
    def find_users_children(user_id):
        """
        Provided with a user_id, look up the children either owned or granted
        access to.

        :param user_id: User's ID to query for children.
        :type user_id: int
        :rtype: list[UserChild]
        """
        user_child_refs = UserChild.find_by_user(user_id)

        return user_child_refs

    @classmethod
    def update(cls, child_id, user_id, updated):

        if not updated:
            raise res_exc.NothingChangedError

        child = cls.find_child(child_id, user_id)

        if 'first_name' in updated:
            child.first_name = updated['first_name']

        if 'last_name' in updated:
            child.last_name = updated['last_name']

        if 'gender_id' in updated:
            gender = Gender.find_by_id(updated['gender_id'])
            if not gender:
                raise res_exc.GenderNotFoundError(updated['gender_id'])
            child.gender = gender

        if 'date_of_birth' in updated:
            child.date_of_birth = updated['date_of_birth']

        if 'middle_name' in updated:
            child.middle_name = updated['middle_name']

        child.save()

        return child
