"""
Module for UserGrant model.
"""
from db import db

from .mixins import Base


class UserGrant(db.Model, Base):
    """
    Represents the grants corresponding to users in the database.
    """

    # SQLAlchemy Configuration
    __tablename__ = 'user_grants'

    uid = db.Column(db.String)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    grant_id = db.Column(db.Integer, db.ForeignKey('grants.id'))

    # Entity Lookups
    user = db.relationship('User', back_populates='grants')
    grant = db.relationship('Grant', back_populates='users')

    def __init__(self, user, grant, uid):
        self.user = user
        self.grant = grant
        self.uid = uid

    @classmethod
    def find_by_uid(cls, grant_id, uid):
        """
        Find a UserGrant based on the provided uid and grant_id.

        :param grant_id: Identifier of grant type.
        :type grant_id: int
        :param uid: Third party ID for user.
        :type uid: str
        :rtype: UserGrant
        """
        return cls.query.filter_by(grant_id=grant_id, uid=uid).first()

    @classmethod
    def create(cls, user, grant, uid):
        """
        Create a new UserGrant entity.

        :param user: User to associate with the UserGrant
        :type user: models.User
        :param grant: Grant type to associate with the UserGrant
        :type grant: models.Grant
        :param uid: Identifier for this user on the third party system.
        :type uid: str
        :rtype: UserGrant
        """
        new_user_grant = cls(user, grant, uid)
        cls.add(new_user_grant)
        return new_user_grant
