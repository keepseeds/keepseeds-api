"""
Module for the Grant class, this class interacts
with the database via SQLAlchemy.
"""

# from db import db
# from models.mixins.base import Base
# from models.user_grant import user_grants
# 
# class Grant(db.Model, Base):
#     """
#     Database representation of a Grant.
#     """
# 
#     # SQLAlchemy Configuration
#     __tablename__ = 'grants'
# 
#     name = db.Column(db.String(100), nullable=False)
#     users = db.relationship('User', 
#     secondary=user_grants,
#     back_populates='grants'
#     )