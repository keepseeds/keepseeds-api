
from db import db

from .mixins import Base

class UserGrant(db.Model, Base):
    __tablename__ = 'user_grants'

    uid = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    grant_id = db.Column(db.Integer, db.ForeignKey('grants.id'), primary_key=True)

    user = db.relationship('User', back_populates='grants')
    grant = db.relationship('Grant', back_populates='users')