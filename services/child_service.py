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

    @staticmethod
    def find_child(_id, user_id):
        """
        Provided with a child id and user id, find the child.

        :param _id: ID of child.
        :type _id: int
        :param user_id: ID of User.
        :type user_id: int
        :rtype: Child
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
            ).all()  # type: list[UserChild]

        return {
            'owned': [uc.child for uc in uc_result if uc.is_primary],
            'included': [uc.child for uc in uc_result if not uc.is_primary]
        }
