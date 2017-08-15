"""
Module for UserChild model.
"""
from db import db

from .mixins import Base


class UserChild(db.Model, Base):
    """
    Represents the children corresponding to users in the database.
    """

    # SQLAlchemy Configuration
    __tablename__ = 'user_children'

    is_primary = db.Column(db.Boolean, nullable=False)

    # Foreign Keys
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Entity Lookups
    user = db.relationship('User', back_populates='children')
    child = db.relationship('Child', back_populates='users')

    def __init__(self, user, child, is_primary=False):
        self.user = user
        self.child = child
        self.is_primary = is_primary

    @classmethod
    def create(cls, user, child, is_primary=False):
        """

        :param user:
        :param child:
        :param is_primary:
        :return:
        """
        new_user_child = cls(user, child, is_primary)

        cls.add(new_user_child)

        return new_user_child

    @classmethod
    def find_by_user(cls, user_id):
        """
        Provided with a user_id, look up the UserChild entities belonging to this user.

        :param user_id:
        :rtype: list[UserChild]
        """
        return cls.query.filter_by(
            user_id=user_id,
            delete_date_time=None
        ).all()
