
from db import db

from .mixins import Base


class UserGrant(db.Model, Base):
    __tablename__ = 'user_grants'

    uid = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    grant_id = db.Column(db.Integer, db.ForeignKey('grants.id'))

    user = db.relationship('User', back_populates='grants')
    grant = db.relationship('Grant', back_populates='users')

    def __init__(self, user, grant, uid):
        self.user = user
        self.grant = grant
        self.uid = uid

    @classmethod
    def find_by_uid(cls, grant_id, uid):
        return cls.query.filter_by(grant_id=grant_id, uid=uid).first()

    @classmethod
    def create(cls, user, grant, uid):
        new_user_grant = cls(user, grant, uid)
        db.session.add(new_user_grant)
        db.session.commit()
        return new_user_grant
